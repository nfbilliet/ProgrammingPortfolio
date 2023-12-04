import os
import torch
from h5py import File as f
import numpy as np

def evaluate_model(error_path, model_path, modelname,
                   model,test_loader, device,
                   dataset_descr="test", model_descr="_val.pth"):
    model.load_state_dict(torch.load(os.path.join(model_path, modelname+model_descr)))
    model.eval()
    error_filename = modelname.split(".")[0]+".h5"
    error_file = f(os.path.join(error_path, error_filename),"a")
    errors=[]
    for batch in test_loader:
      batch = [tensor_stack.to(device) for tensor_stack in batch]
      prediction=model(*batch[:-1])
      error = batch[-1]-prediction
      errors.append(error.abs().item())
    errors=np.array(errors).reshape(-1,1)
    error_file.create_dataset(dataset_descr+" errors",data=errors)
    mean_error = np.mean(errors)
    variance_error=np.var(errors)
    error_file.create_dataset(dataset_descr+" error mean", data=mean_error)
    error_file.create_dataset(dataset_descr+" error variance", data=variance_error)
    error_file.close()
