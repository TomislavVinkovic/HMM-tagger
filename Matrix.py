import numpy as np

class Matrix:
    def __init__(self, rows, cols, dataType='int'):
        if(dataType == 'int'):
            self.matrix = np.zeros((rows, cols), dtype=int)
        else:
            self.matrix = np.zeros((rows, cols))
    
    def get(self, row, col):
        return self.matrix[row][col]
    
    def set(self, row, col, val):
        self.matrix[row][col] = val

    def print(self):
        print(self.matrix)
