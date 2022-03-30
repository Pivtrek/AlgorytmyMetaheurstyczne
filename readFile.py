import numpy as np
import math
from itertools import permutations


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

def kRandom(matrix,k):
    numberOfCities = len(matrix)
    route = np.random.permutation(numberOfCities)
    routeDist = summOfRoutes(route, matrix)
    bestRoute = route
    bestRouteDist = routeDist

    for i in range(k-1):
        route = np.random.permutation(numberOfCities)
        routeDist = summOfRoutes(route, matrix)
        if routeDist < bestRouteDist:
            bestRoute = route
            bestRouteDist = summOfRoutes(bestRoute, matrix)

    #print(bestRouteDist)
    #print(bestRoute)
    return bestRouteDist, bestRoute

def summOfRoutes(array, matrix):
    odl = 0
    nodes = int(len(array))
    for i in range(0,(nodes-1)):
        print(i)
        x = array[i]
        odl += matrix[x][array[i+1]]

    return odl


def twoOptInvert(actualRoute, i, j):
    routeSize = len(actualRoute)

    print(actualRoute)
    print(actualRoute[i])
    print(actualRoute[j])
    newRoute = list(range(0))
    for k in range(0,i):
        newRoute.append(actualRoute[k])

    for k in range(j,i-1,-1):
        newRoute.append(actualRoute[k])

    for k in range(j+1,routeSize):
        newRoute.append(actualRoute[k])
    print(newRoute)
    return newRoute


def generateBestNeighbour(route, matrix):
    print(route)
    currentRoute = route
    currentBestDist = summOfRoutes(currentRoute, matrix)
    routeSize = len(route)

    for i in range(0,(routeSize-1)):
        for j in range(i+1,routeSize):
            newRoute = twoOptInvert(route,i,j)
            newDist = summOfRoutes(newRoute, matrix)
            if newDist < currentBestDist:
                print("znalazlam lepszego")
                currentRoute = newRoute
                currentBestDist = summOfRoutes(currentRoute, matrix)
            
    return currentRoute

def twoOpt(route,matrix):
    newRoute = route
    print(newRoute)
    while True:
        newRoute = generateBestNeighbour(newRoute, matrix)
        if newRoute == route:
            print("newRoute == route")
            break

    return newRoute



#kRandom(readFullMatrix(fullmatrix),10)
#print(summOfRoutes(np.random.permutation(29),readFullMatrix(fullmatrix)))

twoOpt(kRandom(readFullMatrix(fullmatrix),10)[1], fullmatrix)

#array = list(range(10))
#twoOptInvert(array,4,7)