import torch
import numpy as np
from torch.utils import data
from Core.Midi2Image import MidiFile as midi

class Dataset(data.Dataset):
    'Characterizes a dataset for PyTorch'
    def __init__(self, list_IDs):
       'Initialization'
       self.list_IDs = list_IDs

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.list_IDs)

    def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        ID = self.list_IDs[index]
        tmp = midi(self.list_IDs[index],1)
        X = tmp.get_Array2()
        # Load data and get label
        X = torch.Tensor(X)
        return X,X
