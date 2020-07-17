import numpy as np
import pygame
import sys, math, random

BLUE = (40, 100, 219)
BLACK = (0, 0, 0)
RED = (255, 6, 6)
YELLOW = (255, 255, 0)
ROW, COLUMN = 6, 7
in_a_row = 4

PLAYER = 0
BOT = 1
PLAYER_PIECE = 1
BOT_PIECE = 2
BLANK = 0

def build_board():
    board = np.zeros((ROW,COLUMN))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def check_valid_position(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for row in range((ROW-1), -1, -1):
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

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*squareSize, (r+1)*squareSize, squareSize, squareSize))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c*squareSize + squareSize/2), int((r+1)*squareSize + squareSize/2)), radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*squareSize + squareSize/2), int((r+1)*squareSize + squareSize/2)), radius)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c*squareSize + squareSize/2), int((r+1)*squareSize + squareSize/2)), radius)
    pygame.display.update()

def window_scoring(window, piece):
    if piece == BOT_PIECE:
        opponent_piece = PLAYER_PIECE
    else:
        opponent_piece = BOT_PIECE

    score = 0
    if window.count(piece) == 4:
                score += 1000
    elif window.count(piece) == 3 and window.count(BLANK) == 1:
                score += 15

    elif window.count(opponent_piece) == 3 and window.count(BLANK) == 1:
                score -= 30

    return score

def score_position(board, piece):
    score = 0
    #center scoring
    center_array = [int(i) for i in list(board[:, COLUMN//2])]
    center_count = center_array.count(piece)
    score += center_count * 10

    # horizontal scoring
    for r in range(ROW):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN - 3):
            window = row_array[c:c + 4]
            score += window_scoring(window, piece)
    # vertical scoring
    for c in range(COLUMN):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW - 3):
            window = col_array[r:r + 4]
            score += window_scoring(window, piece)
    #positive diagonal
    for r in range(3, ROW):
        for c in range (COLUMN - 3):
            window = []
            window.extend((board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]))
            score += window_scoring(window, piece)
    #negative diagonal
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = []
            window.extend((board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]))
            score += window_scoring(window, piece)

    return score

def get_all_valid_locations(board):
    valid_location_list = []
    for c in range(COLUMN):
        if check_valid_position(board, c):
            valid_location_list.append(c)

    return valid_location_list

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_column_list = get_all_valid_locations(board)
    if depth == 0 or winning_move(board, BOT_PIECE) or winning_move(board, PLAYER_PIECE) or len(valid_column_list) == 0:
        if winning_move(board, BOT_PIECE):
            return [100000, 0]
        elif winning_move(board, PLAYER_PIECE):
            return [-10000, 0]
        elif len(valid_column_list) == 0:
            return [0, 0]
        else:
            return[(score_position(board, BOT_PIECE)), 0]

    if maximizingPlayer:
        maxVal = [-math.inf, random.choice(valid_column_list)]
        for col in valid_column_list:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, BOT_PIECE)
            newScore = minimax(temp_board, depth-1, alpha, beta, False)
            newScorePair = [newScore[0], col]
            if newScore[0] > maxVal[0]:
                maxVal = newScorePair

            alpha = max(alpha, newScore[0])
            if alpha >= beta:
                break
        return maxVal
    else:
        minVal = [math.inf, random.choice(valid_column_list)]
        for col in valid_column_list:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            newScore = minimax(temp_board, depth-1, alpha, beta, True)
            newScorePair = [newScore[0], col]
            if newScore[0] < minVal[0]:
                minVal = newScorePair
            
            beta = min(beta, newScore[0])
            if beta >= alpha:
                break
        return minVal

def pick_best_move(board,piece):
    valid_location_list = get_all_valid_locations(board)
    print(valid_location_list)
    # best_move = [column, score]
    best_move = [random.choice(valid_location_list), -10000]
    for c in valid_location_list:
        r = get_next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, r, c, piece)
        score = score_position(temp_board, piece)
        if score > best_move[1]:
            best_move[0] = c
            best_move[1] = score
    print('best move:', best_move)
    return best_move[0]
        
##################################################################################################################
board = build_board()
print(board, '\n')
game = True
turn = random.randint(PLAYER, BOT)

pygame.init()
squareSize = 100
width = COLUMN * squareSize
height = (ROW + 1) * squareSize
size = (width, height)
radius = int(squareSize/2 * 0.85)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont('monospace', 75)

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, squareSize))
            posX = event.pos[0]
            pygame.draw.circle(screen, RED, (posX, int(squareSize/2)), radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, squareSize))
            # ask player 1 input
            if turn == PLAYER:
                posX = event.pos[0]
                col = int(math.floor(posX / squareSize))

                if check_valid_position(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = font.render('PLAYER 1 WON', 1, RED)
                        screen.blit(label, (75, 10))
                        game = False

                    turn += 1
                    turn = turn % 2

                    print(board, '\n')
                    draw_board(board)
                else: print('row already full')
                


    # ask player 2 input
    if turn == BOT and game:
        bestMove = minimax(board, 5, -math.inf, math.inf, True)
        print(bestMove)
        col = bestMove[1]
    
        if check_valid_position(board, col):
            row = get_next_open_row(board, col)
            pygame.time.wait(500)
            drop_piece(board, row, col, 2)
        else: print('row already full')

        if winning_move(board, 2):
            label = font.render('PLAYER 2 WON', 1, YELLOW)
            screen.blit(label, (75, 10))
            game = False
                
        turn += 1
        turn = turn % 2
        print(board, '\n')
        draw_board(board)
        

    if not game:
        pygame.time.wait(5000)