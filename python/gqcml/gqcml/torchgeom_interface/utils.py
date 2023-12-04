import os
import numpy as np
from h5py import File as f
import torch
import torch_geometric
import matplotlib.pyplot as plt
import functools
import operator

def train_model(device, model, nmb_epochs, train_loader, val_loader,
                loss_fn, optimizer, model_logger, scheduler=None, verbose=False, reduction="mean"):
  """
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
    :scheduler (opt, torch.optim.lr_scheduler): A scheduler for decreasing the learning rate
  Returns
    :model (torch.nn.Module): The optimized model
  """
  nmb_train_dp = len(train_loader.dataset)
  nmb_val_dp = len(val_loader.dataset)
  for epoch in range(1, nmb_epochs+1):
    training_loss = []
    for batch_idx, data in enumerate(train_loader):
      data = data.to(device)
      optimizer.zero_grad()
      prediction=model(data)
      loss = loss_fn(prediction, data.y)
      loss.backward()
      optimizer.step()
      if reduction=="mean":
        training_loss.append(loss.item()*data.num_graphs)
      elif reduction=="sum":
        training_loss.append(loss.item())
    validation_loss = []
    for batch_idx, batch in enumerate(val_loader):
      data = data.to(device)
      prediction=model(data)
      loss = loss_fn(prediction, data.y)
      if reduction=="mean":
        validation_loss.append(loss.item()*data.num_graphs)
      elif reduction=="sum":
        validation_loss.append(loss.item())
      if scheduler:
        scheduler.step(sum(validation_loss)/nmb_val_dp)
    model_logger.add_epoch_metrics(epoch, training_loss, nmb_train_dp, validation_loss, nmb_val_dp)
    model_logger.check_improvement(model, epoch)
    if verbose:
      print("---Epoch "+str(epoch)+"---")
      print("Train loss: "+str(sum(training_loss)/nmb_train_dp))
      print("Val loss: "+str(sum(validation_loss)/nmb_val_dp))
  return model

def train_SchNet(device, model, nmb_epochs, train_loader, val_loader,
                loss_fn, optimizer, model_logger, scheduler=None, verbose=False, reduction="mean"):
  """
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
    :scheduler (opt, torch.optim.lr_scheduler): A scheduler for decreasing the learning rate
  Returns
    :model (torch.nn.Module): The optimized model
  """
  nmb_train_dp = len(train_loader.dataset)
  nmb_val_dp = len(val_loader.dataset)
  for epoch in range(1, nmb_epochs+1):
    training_loss = []
    for batch_idx, data in enumerate(train_loader):
      data = data.to(device)
      optimizer.zero_grad()
      prediction=model(data)
      loss = loss_fn(prediction, data.y.double())
      loss.backward()
      optimizer.step()
      if reduction=="mean":
        training_loss.append(loss.item()*data.num_graphs)
      elif reduction=="sum":
        training_loss.append(loss.item())
    validation_loss = []
    for batch_idx, batch in enumerate(val_loader):
      data = data.to(device)
      prediction=model(data)
      loss = loss_fn(prediction, data.y.double())
      if reduction=="mean":
        validation_loss.append(loss.item()*data.num_graphs)
      elif reduction=="sum":
        validation_loss.append(loss.item())
      if scheduler:
        scheduler.step(sum(validation_loss)/nmb_val_dp)
    model_logger.add_epoch_metrics(epoch, training_loss, nmb_train_dp, validation_loss, nmb_val_dp)
    model_logger.check_improvement(model, epoch)
    if verbose:
      print("---Epoch "+str(epoch)+"---")
      print("Train loss: "+str(sum(training_loss)/nmb_train_dp))
      print("Val loss: "+str(sum(validation_loss)/nmb_val_dp))
  return model


def evaluate_model(model_path, error_path, modelname, model,
                   train_loader, val_loader, test_loader,
                   nmb_bins=100, model_descr="_val.pth", verbose=True):
    """
    Evaluates the optimal model on the training, validation and test datasets and stores a
        - summary: an array containing the mean, variance, minimum and maximum of the absolute
                   error of the prediction of the model
        - error distribution: The counts and bin borders of the plt.hist function 

    Arguments
      :device (str): The device to which the model and tensors are moved during training.
      :model_path (str): The filepath where the optimal model is saved
      :error_path (str): The filepath where the error file will be stored 
      :modelname (str): The base of the modelname
      :model (torch.nn.Module): The model object where the optimal weight can be loaded into
      :train_loader (torch_geometric.data.DataLoader): The dataloader containing the training data
      :val_loader (torch_geometric.data.DataLoader): The dataloader containing the validation data
      :test_loader (torch_geometric.data.DataLoader): The dataloader containing the test data
      :model_descr (opt, str): De suffix that is appended to the modelname used in storing the optimal model,
                               this is set to _val.pth standarly
      :nmb_bins (opt, int): The number of bins used in the distribution of the errors, this is set to 100 standarly
      :verbose (opt, bool): A boolean which controls whether the summary should be returned in the terminal
    Returns
      :None: The function returns nothing. Instead it stores all the calculated information in a h5 file.
             The h5 file contains 2 datasets for each loader 
                 - loader_name summary: An array containing [mean, variance, minimum, maximum] of the errors
                 - loader_name error distribution: a tuple containing the counts and bins 
    """
    model.load_state_dict(torch.load(os.path.join(model_path, modelname+model_descr)))
    model.eval()
    model.to("cpu")
    error_file = f(os.path.join(error_path, modelname+"_summary.h5"), "w")
    for loader_name, loader in zip(["training", "validation", "test"],
                                   [train_loader, val_loader, test_loader]):
      errors=[]
      for data in loader:
        data = data
        prediction=model(data)
        error = data.y-prediction
        errors.append(error.abs().detach().numpy().flatten())
      errors = functools.reduce(operator.iconcat, errors, [])
      print(len(errors))
      mean_error = np.mean(errors)
      variance_error=np.var(errors)
      min_error = np.amin(errors)
      max_error = np.amax(errors)
      error_file.create_dataset(loader_name+" summary", data=np.array([mean_error, variance_error,
                                                                       min_error, max_error]))
      count_bins = plt.hist(errors)
      error_file.create_dataset(loader_name+" error distribution counts", data=np.array(count_bins[0]))
      error_file.create_dataset(loader_name+" error distribution bins", data=np.array(count_bins[1]))
      if verbose:
        print("Summary metrics of the "+loader_name+" dataset")
        print(np.array([mean_error, variance_error, min_error, max_error]))

def evaluate_SchNet(model_path, error_path, modelname, model,
                   train_loader, val_loader, test_loader,
                   nmb_bins=100, model_descr="_val.pth", verbose=True):
    """
    Evaluates the optimal model on the training, validation and test datasets and stores a
        - summary: an array containing the mean, variance, minimum and maximum of the absolute
                   error of the prediction of the model
        - error distribution: The counts and bin borders of the plt.hist function 

    Arguments
      :device (str): The device to which the model and tensors are moved during training.
      :model_path (str): The filepath where the optimal model is saved
      :error_path (str): The filepath where the error file will be stored 
      :modelname (str): The base of the modelname
      :model (torch.nn.Module): The model object where the optimal weight can be loaded into
      :train_loader (torch_geometric.data.DataLoader): The dataloader containing the training data
      :val_loader (torch_geometric.data.DataLoader): The dataloader containing the validation data
      :test_loader (torch_geometric.data.DataLoader): The dataloader containing the test data
      :model_descr (opt, str): De suffix that is appended to the modelname used in storing the optimal model,
                               this is set to _val.pth standarly
      :nmb_bins (opt, int): The number of bins used in the distribution of the errors, this is set to 100 standarly
      :verbose (opt, bool): A boolean which controls whether the summary should be returned in the terminal
    Returns
      :None: The function returns nothing. Instead it stores all the calculated information in a h5 file.
             The h5 file contains 2 datasets for each loader 
                 - loader_name summary: An array containing [mean, variance, minimum, maximum] of the errors
                 - loader_name error distribution: a tuple containing the counts and bins 
    """
    model.load_state_dict(torch.load(os.path.join(model_path, modelname+model_descr)))
    model.eval()
    model.to("cpu")
    error_file = f(os.path.join(error_path, modelname+"_summary.h5"), "w")
    for loader_name, loader in zip(["training", "validation", "test"],
                                   [train_loader, val_loader, test_loader]):
      errors=[]
      for data in loader:
        data = data
        prediction=model(data)
        error = data.y.double()-prediction
        errors.append(error.abs().detach().numpy().flatten())
      errors = functools.reduce(operator.iconcat, errors, [])
      print(len(errors))
      mean_error = np.mean(errors)
      variance_error=np.var(errors)
      min_error = np.amin(errors)
      max_error = np.amax(errors)
      error_file.create_dataset(loader_name+" summary", data=np.array([mean_error, variance_error,
                                                                       min_error, max_error]))
      count_bins = plt.hist(errors)
      error_file.create_dataset(loader_name+" error distribution counts", data=np.array(count_bins[0]))
      error_file.create_dataset(loader_name+" error distribution bins", data=np.array(count_bins[1]))
      if verbose:
        print("Summary metrics of the "+loader_name+" dataset")
        print(np.array([mean_error, variance_error, min_error, max_error]))