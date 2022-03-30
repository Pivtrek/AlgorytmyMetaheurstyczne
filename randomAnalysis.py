from matplotlib import pyplot as plt
import sys
import random
import numpy as np

class RandomAnalysis:
    supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
    supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']

    supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']

    edge_weight_format = ""

    header = dict()
    optimal={"berlin52.tsp": 7542 ,"br17.atsp": 39,"gr120.tsp": 6942 }
    dimension = 0
    matrix = []
    coordinates = dict()
    path = []
    kArange = np.arange(100, 10000, 100)
    prdMedian = [0]*99 #magic number 5000/100

    def __init__(self, filename):
        self.filename = filename
        self.read_data_from = {
            "FULL_MATRIX": self.read_data_from_full_matrix,
            "EUC_2D": self.read_data_from_euc_2d,
            "LOWER_DIAG_ROW": self.read_data_from_lower_diag_row
        }
        self.read()
        self.show_matrix()
        self.show_solution()

    def read(self):
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.replace(":", "")
                if any(x in line for x in self.supported_header_delimiters):
                    break
                split = [x.strip() for x in line.split(maxsplit=1)]
                if len(split) < 2:
                    break
                key, value = split
                self.header[key] = value

            self.set_edge_weight_format()
            self.set_dimension()

            if self.edge_weight_format not in self.supported_formats:
                print("Unsupported data format")
                exit(1)

            self.matrix = [[0 for y in range(0, self.dimension)] for x in range(0, self.dimension)]
            self.read_data_from[self.edge_weight_format](file)

    def set_edge_weight_format(self):
        for format_key in self.supported_format_keys:
            if format_key in self.header.keys():
                self.edge_weight_format = self.header[format_key]
                break

    def set_dimension(self):
        self.dimension = int(self.header["DIMENSION"])
        self.path = [x for x in range(0, self.dimension)]

    def read_data_from_full_matrix(self, file):
        numbers = self.read_numbers(file)
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                self.matrix[i][j] = int(numbers[i * self.dimension + j])

    def read_data_from_lower_diag_row(self, file):
        numbers = self.read_numbers(file)
        index = 0
        for i in range(0, self.dimension):
            for j in range(0, i + 1):
                self.matrix[i][j] = self.matrix[j][i] = numbers[index]
                index += 1

    def read_data_from_euc_2d(self, file):
        numbers = [a for a in [x.split() for x in file.readlines()] if len(a) == 3]
        index = 0
        for i in range(0, self.dimension):
            ni, ni_x, ni_y = numbers[i]
            self.coordinates[int(ni)] = {'x': int(float(ni_x)), 'y': int(float(ni_y))}
            for j in range(0, i + 1):
                nj, nj_x, nj_y = numbers[j]
                distance = int(((float(ni_x) - float(nj_x)) ** 2 + (float(ni_y) - float(nj_y)) ** 2) ** 0.5)
                self.matrix[i][j] = self.matrix[j][i] = distance
                index += 1

    def show_matrix(self):
        for subset in self.matrix:
            print(subset)

    def k_random_method(self):
        #k=100
        m = 0
        for k in (self.kArange):
            print("k: ",k)
            for l in range(40):
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
                self.prdMedian[m] += self.PRD(min_dist)
            self.prdMedian[m] = self.prdMedian[m]/100
            #print("prd średnia: ",self.prdMedian[m])
            m = m+1

    def cost(self,vertex):
        distance=0
        for i in range(len(vertex)):
            if i+1==len(vertex):
                distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                break
            distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
        return distance

    def show_solution(self):
        print("Metoda k-random: ")
        self.k_random_method()
        self.draw_test()

    def draw_test(self):
        print("self.kArange: ", self.kArange)
        print("self.prdMedian: ", self.prdMedian)
        plt.plot(self.kArange, self.prdMedian, color="blue", marker="o", markersize=2)
        plt.show()

    def PRD(self,x):
        ref=self.optimal[self.filename]
        result=100*(x-ref)/ref
        #print("PRD(x):{}%".format(result))
        return result

    @staticmethod
    def read_numbers(file):
        return [item for sublist in [x.split() for x in file.readlines()] for item in sublist if
                item.isnumeric()]
