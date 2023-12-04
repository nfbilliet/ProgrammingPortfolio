import os
import torch
import numpy as np
import random

def random_seed(seed_value, use_cuda):
  """random seed

  Sets the random seed for all the different packages to the same value
  """
  np.random.seed(seed_value) # cpu vars
  torch.manual_seed(seed_value) # cpu  vars
  random.seed(seed_value) # Python
  if use_cuda:
    torch.cuda.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value) # gpu vars
    torch.backends.cudnn.deterministic = True  #needed
    torch.backends.cudnn.benchmark = False

class model_logger():
  def __init__(self,
               history_dir,
               model_dir,
               modelname,
               loss_fn):
    """Model logger

    The model logger class is a training monitor that logs the progress of training of a neural network.
    The logger has a registering function that logs the training loss, validation loss and the variance between
    the different batches (as an additional metric to evaluate the epoch loss). In addition to the registrering 
    function the class also has a function to check if the model has improved.

    Arguments
        history_dir (str): The filepath where the history file that records all the training information.

        model_dir (str): The filepath where the optimal model is stored.

        modelname (str): A string that contains the modelname. This name will be used to store the optimal model and the history.

        loss_fn (str): A string describing the loss function used in the optimization of the model.
    """
    self.model_dir = model_dir
    self.modelname=modelname
    self.loss_fn = loss_fn
    metrics_filepath = os.path.join(history_dir, modelname+"_history.csv")
    self.metrics_file = open(metrics_filepath, "w")
    self.metrics_file.write("Epochs,Training loss, Batch training variance, Validation loss, Batch validation variance\n")
    self.metrics_file.flush()
    self.train_losses = []
    self.train_variances = []
    self.val_losses = []
    self.val_variances = []
    self.optimal = (0,0,0,0,0)

  def add_epoch_metrics(self, epoch, training_losses, nmb_train_datapoints,
                        validation_losses, nmb_val_datapoints):
    """Add epoch metrics

    A function used to write the loss metrics of an epoch to the history file.

    Parameters

        :param epoch (int): The number of the epoch the model is currently on

        :param training_losses (list): A list containing all the batch training losses during the current epoch  

        :param nmb_train_datapoints (int): The total number of datapoints in the training dataset

        :param validation_losses (list): A list containing all the batch validation losses during the current epoch

        :param nmb_val_datapoints (int): The total number of datapoints in the validation dataset

        :return: Nothing is returned, the average loss for the training and validation set is computed together with
                 the variances of the batch losses and written to the metrics file
    """
    train_loss=sum(training_losses)/nmb_train_datapoints
    self.train_losses.append(train_loss)
    train_var=np.var(np.array(training_losses))
    self.train_variances.append(train_var)
    val_loss=sum(validation_losses)/nmb_val_datapoints
    self.val_losses.append(val_loss)
    val_var=np.var(np.array(validation_losses))
    self.val_variances.append(val_var)
    self.metrics_file.write(str(epoch)+","+str(train_loss)+","+str(train_var)+","+str(val_loss)+","+str(val_var)+"\n")
    self.metrics_file.flush()

  def check_improvement(self, model, epoch):
    """Check improvement 

    A function to checkpoint the model during optimization based on the evolution of the validation loss.

    Parameters

        :param model (torch.Module): The model object that is currently being optimized. This object needs to have
                                     the state_dict() function in order to retrieve the parameters.

        :param epoch (int): The current epoch of the model optimization.
    
        :return: Nothing is returned, the function checks whether the validation loss has decreased and saved the model
    """
    modelpath = os.path.join(self.model_dir, self.modelname+"_val.pth")
    if self.val_losses[-1]<self.optimal[3] or epoch==1:
      torch.save(model.state_dict(),modelpath)
      self.optimal=[epoch, self.train_losses[-1], self.train_variances[-1], self.val_losses[-1], self.val_variances[-1]]

  def summary(self):
    """summary

    A function that returns the optimal state of the model during optimization as a dictionary object
    """
    history_dict = {"Epoch":self.optimal[0],
                    "Loss function":self.loss_fn,
                    "Training loss":self.optimal[1],
                    "Training batch variance":self.optimal[2],
                    "Validation loss":self.optimal[3],
                    "Validation batch variance":self.optimal[4]}
    return history_dict
    
def train_model(device, model, nmb_epochs, train_loader, val_loader,
                loss_fn, optimizer, model_logger, scheduler=None, verbose=False):
  """train model

  A function that trains a given neural network

  Parameters

      :param device (str): The device to which the model and tensors are moved during training. 

      :param model (torch.Module): The neural network that needs to be trained. This is aa torch.nn.Module class that
                                   has a forward function

      :param nmb_epochs (int): The number of epochs that the model needs to be trained

      :param train_loader (torch.DataLoader): The dataloader that contains the training dataset and generates batches

      :param val_loader (torch.DataLoader): The dataloader that contains the validation dataset and generates batches

      :param loss_fn (torch.nn): The loss function that is used during the optimization of the neural network

      :param optimizer (torch.optim): The optimizer that is used during the training of the model

      :param model_logger (gqcml.utils.train): The model logger class that registers the training progress and saves the best model

      :param (optional) scheduler (torch.optim.lr_scheduler): A scheduler for decreasing the learning rate
  """
  nmb_train_dp = len(train_loader.dataset)
  nmb_val_dp = len(val_loader.dataset)
  for epoch in range(1, nmb_epochs+1):
    training_loss = []
    for batch_idx, batch in enumerate(train_loader):
      batch = [tensor_stack.to(device) for tensor_stack in batch]
      optimizer.zero_grad()
      prediction=model(*batch[:-1])
      loss = loss_fn(prediction, batch[-1])
      loss.backward()
      optimizer.step()
      training_loss.append(loss.item()*batch[0].shape[0])
    validation_loss = []
    for batch_idx, batch in enumerate(val_loader):
      batch = [tensor_stack.to(device) for tensor_stack in batch]
      prediction=model(*batch[:-1])
      loss = loss_fn(prediction, batch[-1])
      validation_loss.append(loss.item()*batch[0].shape[0])
      if scheduler:
        scheduler.step(sum(validation_loss)/nmb_val_dp)
    if verbose:
      print("---Epoch "+str(epoch)+"---")
      print("Train loss: "+str(sum(training_loss)/nmb_train_dp))
      print("Val loss: "+str(sum(validation_loss)/nmb_val_dp))
    model_logger.add_epoch_metrics(epoch, training_loss, nmb_train_dp, validation_loss, nmb_val_dp)
    model_logger.check_improvement(model, epoch)
  return model

      

