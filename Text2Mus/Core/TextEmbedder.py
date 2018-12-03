texts = []  # list of text samples
labels_index = {}  # dictionary mapping label name to numeric id
labels = []  # list of label ids

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