class Matrix:
    
    def __init__(self, rows, cols):
        self.matrix = [[0 for j in range(cols)] for i in range(rows)]
    
    def get(self, row, col):
        return self.matrix[row][col]
    
    def set(self, row, col, val):
        self.matrix[row][col] = val
