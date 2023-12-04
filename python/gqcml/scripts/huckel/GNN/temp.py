import sys
sys.path.append("../../..")

import torch
import torch_geometric
import numpy as np
from h5py import File as f
import os
import itertools
import gqcml

data_dir = "/home/nbilliet/projects/def-stijn/nbilliet/gqcg_data/huckel/data"
dataset = f(os.path.join(data_dir, "huckel_4s_gqcml_2a2b.h5"), "r")
train_input=np.abs(np.array(dataset["train_input"]))
train_output=torch.from_numpy(np.abs(np.array(dataset["train_energy"])))
preprocessor = gqcml.data.Data.Preprocessor(4)
preprocessor_func=preprocessor.vdegree_weighted_nf
opt_arg=[True, "linear combination"]
diagonal_format=[]
train_nf, train_am = gqcml.datasets.Datasets.trius_to_inputs(train_input, preprocessor,
                                              diagonal_format, preprocessor_func, opt_arg)
train_nf, train_am = torch.from_numpy(train_nf), torch.from_numpy(train_am)
datapoints = []
for nf, am, e in zip(train_nf, train_am, train_output):
    datapoints.append(gqcml.torchgeom_interface.datasets.graph_to_Data(nf, am, e))
train_loader = torch_geometric.data.DataLoader(datapoints[0], batch_size=2, shuffle=True)
model=gqcml.torchgeom_interface.auto_encoder.GraphAutoEncoder(6,
                                                              [54,54,32,32,16,32,32,54,54],
                                                              torch.nn.ReLU(),
                                                              dropout=True,
                                                              feature_transformation=False,
                                                              residual=True,
                                                              concatenate=True)
