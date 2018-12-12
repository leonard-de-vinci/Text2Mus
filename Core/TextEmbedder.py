import os
import numpy as np
from numpy import zeros, newaxis


class TextEmbedder(object):
    """description of class"""
    def __init__(self, pathGlove):
        self.GloveVector = self.LoadGlove(pathGlove)

    def LoadGlove(self,path):
        with open(path, encoding="utf8" ) as f:
            content = f.readlines()
            vectorize  = {}
            for line in content:
                splitLine = line.split()
                word = splitLine[0]
                embedding = np.array([float(val) for val in splitLine[1:]])
                vectorize[word] = embedding
        return vectorize
    def Vectorize(self, word):
        a = self.GloveVector[word]
        c = zeros((1024))
        c[:a.shape[0]] = a
        b = a[:,newaxis,newaxis]
        return c.reshape((2,16,32))
        