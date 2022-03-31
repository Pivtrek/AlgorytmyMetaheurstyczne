from generate import GenerateGraph
from matplotlib import pyplot as plt
import random
import sys
import copy
import time
import os
import psutil
class TestTime:
    edge_weight_format = ""
    matrix=[]
    currentNode = 0
    kRandomTimeSolution = [0]*14
    neighborTimeSolution = [0]*14
    extendedNeighborTimeSolution = [0]*14
    optTimeSolution = [0]*14
    kRandomMemSolution = [0]*14
    neighborMemSolution = [0]*14
    extendedNeighborMemSolution = [0]*14
    optMemSolution = [0]*14
    dimension = 10

    def __init__(self):
        self.variant='FULL_MATRIX'
        self.seed=random.seed(100)
        self.upper_bound=100
        self.repetitions=10
        print("dlugosc probek ", len(self.kRandomTimeSolution))
        for j in range(self.repetitions):
            self.currentNode = 0
            for i in range(10,150,10):
                self.dimension=i
                self.generate()
                self.currentNode += 1

        for j in range(len(self.kRandomTimeSolution)):
            self.kRandomTimeSolution[j] = self.kRandomTimeSolution[j]/self.repetitions
            self.neighborTimeSolution[j] = self.neighborTimeSolution[j]/self.repetitions
            self.extendedNeighborTimeSolution[j] = self.extendedNeighborTimeSolution[j]/self.repetitions
            self.optTimeSolution[j] = self.optTimeSolution[j]/self.repetitions
            self.kRandomMemSolution[j] = self.kRandomMemSolution[j]/self.repetitions
            self.neighborMemSolution[j] = self.neighborMemSolution[j]/self.repetitions
            self.extendedNeighborMemSolution[j] = self.extendedNeighborMemSolution[j]/self.repetitions
            self.optMemSolution[j] = self.optMemSolution[j]/self.repetitions

        self.draw_solution()

    def generate(self):
        newMatrix = []
        if(self.variant=='FULL_MATRIX'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if i==j:
                        row.append(9999)
                    else:
                        row.append(random.randint(1,self.upper_bound))
                newMatrix.append(row)
            self.matrix = newMatrix
        elif(self.variant=='EUC_2D'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if i==j:
                        row.append(0)
                        break
                    else:
                        value=random.randint((self.upper_bound/2)+1,self.upper_bound)
                        row.append(value)
            newMatrix.append(row)
            for i in range(self.dimension):
                for j in range(i+1,self.dimension):
                    newMatrix[i].append(newMatrix[j][i])
            self.matrix = newMatrix

        elif(self.variant=='LOWER_DIAG_ROW'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if(i==j):
                        row.append(0)
                        break
                    else:
                        row.append(random.randint(1,self.upper_bound))
            newMatrix.append(row)
            for i in range(self.dimension):
                for j in range(i+1,self.dimension):
                    newMatrix[i].append(newMatrix[j][i])
            self.matrix = newMatrix
        else:
            print("Unsupported type of problem, please choose one from list down below: ")
            for item in self.supported_formats:
                print(item)
            return
        self.show_matrix()
        self.generate_path()

    def show_matrix(self):
        for row in self.matrix:
            print(row)

    def generate_path(self):
        print("Metoda k-random: ")
        self.k_random_method()
        print("Metoda najbliższego sąsiada: ")
        self.nearest_neighbor()
        print("Roszerzona metoda najbliższego sąsiada: ")
        self.extended_nearest_neighbor()
        print("Algorytm 2-OPT: ")
        self.two_opt()


    def k_random_method(self):
        start_time = time.time()
        k=100*self.dimension
        print("k: ",k)
        min_dist=sys.maxsize
        vertex=[x for x in range(self.dimension)]
        path=[]
        for j in range(k):
            random.shuffle(vertex)
            distance=0
            for i in range(len(vertex)):
                if i+1==len(vertex):
                    distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                    break
                if(int(self.matrix[vertex[i]][vertex[i+1]])==0):
                    continue
                distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
            if(distance<min_dist):
                min_dist=distance
                path=vertex.copy()
        #print("Droga: ",min_dist)
        #print("Cykl: ",path)
        #self.test_cost(path)
        self.kRandomTimeSolution[self.currentNode] +=  (time.time()-start_time)
        process = psutil.Process(os.getpid())
        #print("Pamięć: %s" % process.memory_info().rss)
        self.kRandomMemSolution[self.currentNode] += process.memory_info().rss

    def nearest_neighbor(self):
        start_time = time.time()
        start=random.randint(0,self.dimension-1)
        #print(start)
        path=[start]
        min_dist=0
        matrix_copy=copy.deepcopy(self.matrix)
        while(len(path)!=self.dimension):
            distances=matrix_copy[start]
            distances.sort()
            counter=0
            j=0
            while j < self.dimension:
                if distances[counter]==self.matrix[start][j]:
                    if j not in path:
                        if(distances[counter]==0):
                            counter=counter+1
                            j=-1
                        else:
                            min_dist=min_dist+int(distances[counter])
                            path.append(j)
                            start=j
                            counter=0
                            break
                j=j+1
                if(j==self.dimension):
                    j=0
                    counter=counter+1
                if(counter==self.dimension):
                    print("Ślepy zaułek")
                    return
        #print("Droga: ",min_dist)
        #self.test_cost(path)
        #print("Cykl: ",path)
        #print("Czas: %s " % (time.time()-start_time))
        self.neighborTimeSolution[self.currentNode] += (time.time()-start_time)
        process = psutil.Process(os.getpid())
        #print("Pamięć: %s" % process.memory_info().rss)
        self.neighborMemSolution[self.currentNode] += process.memory_info().rss



    def extended_nearest_neighbor(self):
        currentStart = 0
        start_time = time.time()
        for i in range(0,self.dimension):
            start= i
            #print(start)
            path=[start]
            min_dist=0
            matrix_copy=copy.deepcopy(self.matrix)
            while(len(path)!=self.dimension):
                distances=matrix_copy[start]
                distances.sort()
                counter=0
                j=0
                while j < self.dimension:
                    if distances[counter]==self.matrix[start][j]:
                        if j not in path:
                            if(distances[counter]==0):
                                counter=counter+1
                                j=-1
                            else:
                                min_dist=min_dist+int(distances[counter])
                                path.append(j)
                                start=j
                                counter=0
                                break
                    j=j+1
                    if(j==self.dimension):
                        j=0
                        counter=counter+1
                    if(counter==self.dimension):
                        print("Ślepy zaułek")
                        return
        #print("Droga: ",min_dist)
        #self.test_cost(path)
        #print("Cykl: ",path)
        #print("Czas: %s " % (time.time()-start_time))
        self.extendedNeighborTimeSolution[self.currentNode] += (time.time()-start_time)
        process = psutil.Process(os.getpid())
        self.extendedNeighborMemSolution[self.currentNode] += process.memory_info().rss
        #print("Pamięć: %s" % process.memory_info().rss)

    def cost(self,vertex):
        distance=0
        for i in range(len(vertex)):
            if i+1==len(vertex):
                distance=distance+self.matrix[vertex[i]][vertex[0]]
                break
            distance=distance+self.matrix[vertex[i]][vertex[i+1]]
        return distance

    def two_opt(self):
        start_time = time.time()
        path = [x for x in range(self.dimension)]
        best = path
        improved = True
        while improved:
            improved = False
            for i in range(0, len(path)-1):
                for j in range(i+1, len(path)):
                    if j-i == 1: continue
                    new_route = path[:]
                    new_route[i:j] = reversed(new_route[i:j])
                    if self.cost(new_route) < self.cost(best):
                        best = new_route
                        improved = True
            path = best
        #print("Droga: ",self.cost(best))
        #print("Cykl: ", path)
        #self.test_cost(path)
        #print("Czas: %s " % (time.time()-start_time))
        self.optTimeSolution[self.currentNode] += (time.time()-start_time)
        process = psutil.Process(os.getpid())
        self.optMemSolution[self.currentNode] += process.memory_info().rss
        #print("Pamięć: %s" % process.memory_info().rss)
    pass

    def draw_solution(self):
        plt.plot(range(10,150,10), self.kRandomTimeSolution, color="blue", marker="o", markersize=2)
        plt.plot(range(10,150,10), self.neighborTimeSolution, color="red", marker="o", markersize=2)
        plt.plot(range(10,150,10), self.extendedNeighborTimeSolution, color="pink", marker="o", markersize=2)
        plt.plot(range(10,150,10), self.optTimeSolution, color="green", marker="o", markersize=2)
        plt.show()
        #plt.plot(range(10,150,10), self.kRandomMemSolution, color="blue", marker="o", markersize=2)
        #plt.plot(range(10,150,10), self.neighborMemSolution, color="red", marker="o", markersize=2)
        #plt.plot(range(10,150,10), self.extendedNeighborMemSolution, color="pink", marker="o", markersize=2)
        #plt.plot(range(10,150,10), self.optMemSolution, color="green", marker="o", markersize=2)
        #plt.show()
        pass