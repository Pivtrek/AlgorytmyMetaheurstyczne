import numpy as np
import math


def readFullMatrix(name):
    matrix = np.loadtxt(name)
    return matrix


fullmatrix = "bays29.tsp"
def readEuc2d(name):
    euc2d = np.loadtxt(name, usecols=np.arange(1,3))
    return euc2d

def convertEuc2dToFullMatrix(euc2d):
    rows = int(euc2d.size/2)
    mat = [[0 for _ in range(rows)] for _ in range(rows)]
    #print(euc2d)
    for i in range(0,rows):
        for j in range(i+1,rows):
            dist = math.sqrt(((euc2d[i][0]-euc2d[j][0])**2 + (euc2d[i][1]-euc2d[j][1])**2))
            print(range(i+1,rows))
            mat[i][j] = dist
            mat[j][i] = dist

    x = np.array(mat)
    z = np.asmatrix(x)
    return z


