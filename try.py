from Core.Midi2Image import MidiFile as midi
import os
from Core.PytorchGenerator import Dataset
indexes = []
with open("./datasetList.txt","r") as f:
    indexes = f.readlines()
indexes = [i.replace("\n","") for i in indexes ]
indexes = indexes[:50]
print(len(indexes))
dataset = Dataset(indexes)
X,y = dataset[2]
print(X.shape)

import Core.AutoEncoder
from Core.AutoEncoder import VAE

a = VAE(epoch = 12,batch_size = 1,)