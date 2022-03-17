import numpy as np

def readFullMatrix(name):
    matrix = np.loadtxt(name)
    return matrix

name = "berlin52.tsp"

def readEuc2d(name):
    euc2d = np.loadtxt(name, usecols=np.arange(1,3))
    return euc2d


print(readEuc2d(name))
