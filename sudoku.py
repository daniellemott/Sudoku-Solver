class Sudoku:

    def __init__(self, grid):
        self.oldArray = self.createDictionary(grid)
        self.twoD = grid


    def accessUnsolvedGridEntry(self, x, y):
        return self.oldArray[(x, y)]

    def accessSolvedGrid(self):
        self.solveSodoku(0)
        return self.twoD

    # Enable access to unsolved sudoku grid entries once grid has been solved
    def createDictionary(self, grid):
        arrayDict = {}
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                arrayDict[(i, j)] = grid[i][j]
        return arrayDict

    # Ensures the entry is allowed to be placed in the cell.
    def isSafe(self, r, c, num):
        if not self.safeRow(r, num) or not self.safeCol(c, num) or self.safeSubgrid(r - r % 3, c - c % 3, num):
            return False
        return True

    # This method is courtesy of https://www.geeksforgeeks.org/sudoku-backtracking-7/
    def safeSubgrid(self, row, col, num):
        for i in range(3):
            for j in range(3):
                if(self.twoD[i+row][j+col] == num):
                    return True
        return False

    # Ensures there are no duplicate entries in the specified row.
    def safeRow(self, r, num):
        for entry in self.twoD[r]:
            if entry == num:
                return False
        return True

    # Ensures there are no duplicate entries in the specified column.
    def safeCol(self, c, num):
        for r in range(len(self.twoD)):
            if self.twoD[r][c] == num:
                return False
        return True

    # Determines end row or column index of 3x3 subgrid where the number is located.
    def navigate(self, n):
        if n // 3 == 0:
            return 3
        if n // 3 == 1:
            return 6
        return 9


    def solveSodoku(self, r):
        # Iterate through until a non-assigned cell is found
        if self.noEmpty():
            return True
        # Don't need to backtrack rows
        for i in range(r, len(self.twoD)):
            for j in range(len(self.twoD)):
                # Found non-assigned cell
                if not self.twoD[i][j]:
                    for k in range(1, 10):
                        if self.isSafe(i, j, k):
                            self.twoD[i][j] = k
                            if self.solveSodoku(r):
                                return True
                            self.twoD[i][j] = 0
                    return False

    # Determine if there aren't any empty entries in the grid
    def noEmpty(self):
        for i in range(len(self.twoD)):
            for j in range(len(self.twoD)):
                if not self.twoD[i][j]:
                    return False
        return True

    def displayGrid(self):
        for row in self.twoD:
            print(row)


# Test code
class Main:

    def main():
        grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                [5, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 0, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 6, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 4],
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]
        s = Sudoku(grid)
        s.solveSodoku(0)
        s.displayGrid()

