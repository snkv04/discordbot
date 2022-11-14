
import random

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for j in range(columns)] for i in range(rows)]
        self.score = 0
        self.add_tile()
        self.add_tile()
    
    def add_tile(self):
        empty_square = False
        while empty_square == False:
            row = random.choice(range(self.rows))
            column = random.choice(range(self.columns))
            if(self.board[row][column] == 0):
                self.board[row][column] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
                empty_square = True

    def replace_row(self, row_index, new_row):
        self.board[row_index] = new_row
    
    def replace_column(self, col_index, new_col):
        for i in range(self.rows):
            self.board[i][col_index] = new_col[i]

    @staticmethod
    def rotate_board(matrix):
        new_matrix = []
        for i in range(len(matrix[0])):
            new_row = []
            for j in range(len(matrix)):
                new_row.append(matrix[len(matrix) - 1 - j][i])
            new_matrix.append(new_row)
        return new_matrix

    @staticmethod
    def rotate_board_cc(matrix):
        new_matrix = [[0 for j in range(len(matrix))] for i in range(len(matrix[0]))]
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                new_matrix[i][j] = matrix[j][len(matrix[0]) - 1 - i]
        return new_matrix

    @staticmethod
    def flip_board(matrix):
        new_matrix = []
        for i in range(len(matrix)):
            new_matrix.append(list(reversed(matrix[i])))
        return new_matrix
    
    def move(self, direction):
        
        def move_left(matrix):
            score_increment = 0
            new_matrix = []
            for i in range(len(matrix)):
                row = matrix[i]
                
                # moves all the values to the left
                new_row = [value for value in row if value != 0]
                
                # combines the equally-valued tiles together
                """for tempj in range(len(new_row) - 1):
                    if new_row[tempj] == new_row[tempj + 1]:
                        new_row.pop(tempj)
                        new_row[tempj] = (new_row[tempj] * 2)
                        score_increment += new_row[tempj] * 2"""

                tempj = 0
                while True:
                    if tempj > (len(new_row) - 2):
                        break
                    if new_row[tempj] == new_row[tempj + 1]:
                        new_row.pop(tempj)
                        new_row[tempj] = (new_row[tempj] * 2)
                        score_increment += new_row[tempj]
                    tempj += 1
                
                # adds 0s to the end of the new row
                while len(new_row) < len(row):
                    new_row.append(0)

                new_matrix.append(new_row)
            
            return [new_matrix, score_increment]

        if(direction == "left"):
            returns = move_left(self.board)
            self.board = returns[0]
            self.score += returns[1]
        elif(direction == "right"):
            returns = move_left(Board.flip_board(self.board))
            self.board = Board.flip_board(returns[0])
            self.score += returns[1]
        elif(direction == "up"):
            returns = move_left(Board.rotate_board_cc(self.board))
            self.board = Board.rotate_board(returns[0])
            self.score += returns[1]
        elif(direction == "down"):
            returns = move_left(Board.rotate_board(self.board))
            self.board = Board.rotate_board_cc(returns[0])
            self.score += returns[1]
        
        self.add_tile() 

    def move_legal(self, direction):
        new_board = None
        if direction == "left":
            new_board = self.board
        if direction == "right":
            new_board = Board.flip_board(self.board)
        elif direction == "up":
            new_board = Board.rotate_board_cc(self.board)
        elif direction == "down":
            new_board = Board.rotate_board(self.board)
        for row in new_board:
            j = 0
            while True:
                if j > (len(row) - 2):
                    break

                if row[j] == 0 and row[j + 1] != 0:
                    return True
                elif row[j] == row[j + 1] and row[j] != 0:
                    return True
                j += 1
        return False

    def has_legal_move(self):
        return self.move_legal("left") or self.move_legal("right") or \
            self.move_legal("up") or self.move_legal("down")

    def highest_tile(self):
        highest_value = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] > highest_value:
                    highest_value = self.board[i][j]
        return highest_value

# myboard = Board(4, 4)
# print(myboard)
# print(myboard.board)
# myboard.add_tile()
# print(myboard)
# print(myboard.rectangular_board_string())
# myboard.rotate_board()
# print(myboard.rectangular_board_string())
# myboard.rotate_board_cc()
# myboard.rotate_board_cc()
# print(myboard.rectangular_board_string())
