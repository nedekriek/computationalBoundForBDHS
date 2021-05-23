import pickle
import numpy as np

def serialize(data, filename):
    if filename.endswith(".obj"):
        filehandler=open(filename,"wb")
        pickle.dump(data, filehandler)
        filehandler.close()
    

def deserialize(filename):
    if filename.endswith(".obj"):
        filehandler=open(filename, "rb")
        data=pickle.load(filehandler)
        filehandler.close()
        return data
