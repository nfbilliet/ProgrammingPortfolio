from torch_geometric.typing import Adj, OptTensor, PairTensor
import os
import numpy as np
from h5py import File as f
import torch_geometric

import torch
from torch import Tensor
from torch.nn import Parameter
from torch_scatter import scatter_add
from torch_sparse import SparseTensor, matmul, fill_diag, sum, mul
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.utils import add_remaining_self_loops
from torch_geometric.utils.num_nodes import maybe_num_nodes


def sum_similarity_loss(inp_tensor, decoded_tensor):
    inp_tensor_norm = torch.norm(inp_tensor)
    decoded_tensor_norm = torch.norm(decoded_tensor)
    dot_product = torch.matmul(inp_tensor, decoded_tensor.T)
    return 2*inp_tensor_norm-torch.sqrt(dot_product)-decoded_tensor_norm

class Neighbourhood_Aggregator(MessagePassing):
    """
    A class that is used in the generation of a feature vector containing
    raw node features that are aggregated. This function works in a similar
    fashion to GCNConv but removes the use of any bias and weights.
    """
    def __init__(self):
        super(Neighbourhood_Aggregator, self).__init__()

    def forward(self, x: Tensor, edge_index: Adj,
                edge_weight: OptTensor = None) -> Tensor:
        out = self.propagate(edge_index, x=x, edge_weight=edge_weight,
                             size=None)
        return out

    def message(self, x_j: Tensor, edge_weight: OptTensor) -> Tensor:
        return x_j if edge_weight is None else edge_weight.view(-1, 1) * x_j

    def message_and_aggregate(self, adj_t: SparseTensor, x: Tensor) -> Tensor:
        return matmul(adj_t, x, reduce=self.aggr)

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.in_channels,
                                   self.out_channels)

class GraphAutoEncoder(torch.nn.Module):
    """
    Graph auto-encoder that utilizes the neighbourhood aggregation class.
    The encoder applies a series of unweighted graph convolutions  that construct
    aggregated representation, residually added to the original or not.
    In addition to this we als provide the option to store each aggregation step seperately and concatenate them at the end.

    After aggregation the original feature vector is passed through an encoder dense network which contracts it to a specific dimension.
    Following this contraction the encoded form is fed to the decoder dense network which will map it again to the original feature vector.

    Attributes
        :num_aggr (int): Number of neighbourhood aggregation that needs to be performed
        :layer_config (list): layer configuration for the encoder network. This configuration is reversed for the decoder dense network
        :act_fn (torch.nn): A torch module that serves as an activation for the encoder and decoder layers
        :dropout (opt, bool): A boolean that controls the employment of dropout between the layers
        :dropout_rate (opt, float): The dropout rate at which nodes are disable
        :feature_transformation (opt, torch.nn.Module): soon to be deprecated
    """
    def __init__(self, num_aggr, layer_config, act_fn, dropout=True, dropout_rate=0.1, feature_transformation=False):
        super(GraphAutoEncoder, self).__init__()
        self.aggr = Neighbourhood_Aggregator()
        self.num_aggr=num_aggr
        self.encoder_layers=torch.nn.ModuleList([torch.nn.Linear(layer_config[idx], layer_config[idx+1])
                                                             for idx in range(len(layer_config)-1)])
        self.decoder_layers=torch.nn.ModuleList([torch.nn.Linear(layer_config[-idx], layer_config[-(idx+1)])
                                                             for idx in range(1,len(layer_config))])
        if dropout:
            self.dropout = torch.nn.Dropout(p=dropout_rate)
        else:
            self.dropout = False
        if feature_transformation:
            self.feature_transformation = feature_transformation
        else:
            self.feature_transformation = False
        self.act_fn = act_fn

    def forward(self, data):
        """
        Forward phase of the encoder

        Arguments
            :data (torch_geometric.data.Data): A data object that contains the node features, edge indices and edge weights
        Returns
            :initial features, decoded_features (torch.Tensor): The initial tensor obtained after aggregation of the neighbourhood information and the decoded form of this tensor 
        """
        if self.feature_transformation:
            aggregated = self.feature_transformation(data.x)
        else:
            aggregated = data.x
        for i in range(self.num_aggr):
            aggregated = aggregated + self.aggr(aggregated,
                                                data.edge_index,
                                                edge_weight=data.edge_attr)
        embedded = self.act_fn(self.encoder_layers[0](aggregated))
        if self.dropout:
            embedded = self.dropout(embedded)
        for encoder_layer in self.encoder_layers[1:-1]:
            if self.dropout:
                embedded = self.dropout(self.act_fn(encoder_layer(embedded)))
            else:
                embedded = self.act_fn(encoder_layer(embedded))
        encoded = self.encoder_layers[-1](embedded)
        decoded = self.act_fn(self.decoder_layers[0](encoded))
        if self.dropout:
            decoded = self.dropout(decoded)
        for decoder_layer in self.decoder_layers[1:-1]:
            if self.dropout:
                decoded = self.dropout(self.act_fn(decoder_layer(decoded)))
            else:
                decoded = self.act_fn(decoder_layer(decoded))
        decoded = self.decoder_layers[-1](decoded)
        return (aggregated, decoded)

    def encode(self, data):
        """
        Encoding of the initial feature vector

        Arguments
            :data (torch_geometric.data.Data): A data object that contains the node features, edge indices and edge weights
        Returns
            :encoded_features (torch.Tensor): The encoded representation of the initial feature vector
        """
        if self.feature_transformation:
            aggregated = self.feature_transformation(data.x)
        else:
            aggregated = data.x
        for i in range(self.num_aggr):
            aggregated = aggregated + self.aggr(aggregated,
                                                data.edge_index,
                                                edge_weight=data.edge_attr)
        embedded = self.act_fn(self.encoder_layers[0](aggregated))
        for encoder_layer in self.encoder_layers[1:-1]:
            embedded = self.act_fn(encoder_layer(embedded))
        encoded = self.encoder_layers[-1](embedded)
        return encoded

    def decode(self, encoded_node_features):
        """
        Decoding of an encoded tensor
        Forward phase of the encoder

        Arguments
            :encoded_node_features (torch.Tensor): A torch Tensor that represent the encoded feature vector which requires decoding
        Returns
            :decoded_features (torch.Tensor): The decoded form of the encoded features
        """
        decoded = self.act_fn(self.decoder_layers[0](encoded_node_features))
        for decoder_layer in self.decoder_layers[1:-1]:
            decoded = self.act_fn(decoder_layer(decoded))
        decoded = self.decoder_layers[-1](decoded)
        return decoded

def train_model(device, model, nmb_epochs, train_loader, val_loader,
                loss_fn, optimizer, model_logger, scheduler=None, verbose=False):
  """train model

  A function that trains a given neural network

  Arguments
    :device (str): The device to which the model and tensors are moved during training.
    :model (torch.Module): The neural network that needs to be trained. This is aa torch.nn.Module class that
                                   has a forward function
    :nmb_epochs (int): The number of epochs that the model needs to be trained
    :train_loader (torch.DataLoader): The dataloader that contains the training dataset and generates batches
    :val_loader (torch.DataLoader): The dataloader that contains the validation dataset and generates batches
    :loss_fn (torch.nn): The loss function that is used during the optimization of the neural network
    :optimizer (torch.optim): The optimizer that is used during the training of the model
    :model_logger (gqcml.utils.train): The model logger class that registers the training progress and saves the best model
    :(optional) scheduler (torch.optim.lr_scheduler): A scheduler for decreasing the learning rate
  Returns
    :optimized_model (torch.nn.Module): The optimized model after the specified options
  """
  nmb_train_dp = len(train_loader.dataset)
  nmb_val_dp = len(val_loader.dataset)
  for epoch in range(1, nmb_epochs+1):
    training_loss = []
    model.train()
    for batch_idx, data in enumerate(train_loader):
      data = data.to(device)
      optimizer.zero_grad()
      initial, decoded =model(data)
      loss = loss_fn(initial, decoded)
      loss.backward()
      optimizer.step()
      training_loss.append(loss.item()*data.num_graphs)
    validation_loss = []
    model.eval()
    for batch_idx, batch in enumerate(val_loader):
      data = data.to(device)
      initial, decoded=model(data)
      loss = loss_fn(initial, decoded)
      validation_loss.append(loss.item()*data.num_graphs)
    if scheduler:
        scheduler.step(np.sum(validation_loss)/nmb_val_dp)
    model_logger.add_epoch_metrics(epoch, training_loss, nmb_train_dp, validation_loss, nmb_val_dp)
    model_logger.check_improvement(model, epoch)
    if verbose:
      print("---Epoch "+str(epoch)+"---")
      print("Train loss: "+str(np.sum(training_loss)/nmb_train_dp))
      print("Val loss: "+str(np.sum(validation_loss)/nmb_val_dp))
  return model
