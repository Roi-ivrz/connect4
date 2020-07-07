import numpy as np



ROW, COLUMN = 6, 7
in_a_row = 4

def build_board():
    board = np.zeros((ROW,COLUMN))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_valid_position(board, col):
    return board[ROW-1][col] == 0

def get_next_open_row(board, col):
    for row in range(ROW):
        if board[row][col] == 0:
            return row

def winning_move(board, piece):
    # check horizontally
    for row in range(ROW):
         for column in range(COLUMN - (in_a_row - 1)):
             if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                 return True

    # check vertically
    for column in range(COLUMN):
         for row in range(ROW - (in_a_row - 1)):
             if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and board[row+3][column] == piece:
                 return True
    
    # check positive diagonals
    for column in range(COLUMN - (in_a_row - 1)):
         for row in range(ROW - (in_a_row - 1)):
             if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] == piece and board[row+3][column+3] == piece:
                 return True

    # check negative diagonals
    for column in range(COLUMN - (in_a_row - 1)):
         for row in range((in_a_row-1), ROW):
             if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] == piece and board[row-3][column+3] == piece:
                 return True

def printBoard(board):
    print(np.flip(board, 0))

board = build_board()
printBoard(board)
game, turn = True, 0

while game:
    # ask player 1 input
    if turn == 0:
        correctResponse = False
        while not correctResponse:
            col = int(input('player 1 move: (0-6): '))
            if col >= 0 and col <= 6: correctResponse = True
            else: print('invalid response')

        if check_valid_position(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
        else: print('row already full')

        if winning_move(board, 1):
            print(' PLAYER 1 WON')
            game = False

    # ask player 2 input
    else:
        correctResponse = False
        while not correctResponse:
            col = int(input('player 2 move: (0-6): '))
            if col >= 0 and col <= 6: correctResponse = True
            else: print('invalid response')
    
        if check_valid_position(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
        else: print('row already full')

        if winning_move(board, 2):
            print(' PLAYER 2 WON')
            game = False

    printBoard(board)
    turn += 1
    turn = turn % 2