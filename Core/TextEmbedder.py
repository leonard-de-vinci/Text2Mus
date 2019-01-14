import os
import numpy as np
from numpy import zeros, newaxis
from scipy.spatial.distance import cosine


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
    def similarity(self, word1, word2):
        return cosine(self.GloveVector[word1],self.GloveVector[word2])
    def EmotionalCloseness(self, word):
        toreturn = []
        for w in basicEmotions:
            toreturn.append(self.similarity(w,word))
        return np.array(toreturn,dtype = np.float32)
        
    def Vectorize(self, word):
        a = self.GloveVector[word]
        return a

#28 basic emotions
basicEmotions = ["suffering",
    "weeping",
    "anxiety",
    "grief",
    "dejection",
    "despair",
    "joy",
    "love",
    "tender",
    "devotion",
    "reflection",
    "meditation",
    "determination",
    "hatred",
    "anger",
    "disdain",
    "contempt",
    "disgust",
    "guilt",
    "pride",
    "helplessness",
    "patience",
    "affirmation",
    "fear",
    "horror",
    "shame",
    "shyness",
    "modesty"]
Embedder = TextEmbedder("d:\glove.6B.100d.txt")

#print(Embedder.EmotionalCloseness("hating")[basicEmotions.index("hatred")])