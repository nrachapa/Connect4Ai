import Player
import math
import random
import sys
import pygame

#python3 -m venv .venv
#source .venv/bin/activate
# restarting game, no need to ask for player name and coin
# board printing
# put row and column numbers
# Don't need to actually even ask for the piece that they want
# switch order of player and or pieces when restarting
# | __ | __ | __  |  |  |
# | __
# python3 -m pip install -U pygame --user

# Global Variables
rows = 6
columns = 7
piece1 = 'X'
piece2 = 'O'
pieces = [' ', piece1, piece2]
p1 = Player.Player('', '')
p2 = Player.Player('', '')
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
game_over = False
width = columns * SQUARESIZE
height = (rows + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
myfont = pygamefont.SysFont("monospace", 75)
turn = 0
# Functions


def drawBoard(board):
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE +
                                SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),
                                   int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(columns):
        for r in range(rows):
            if board[r][c] == pieces[1]:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == pieces[2]: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            pygame.display.update()    

def createBoard():
    board = []
    for i in range(rows):
        boardRow = []
        for j in range(columns):
            boardRow.append(pieces[0])
        board.append(boardRow)
    return board

def printBoard(board):
    for i in board:
        print(i)
        print()

def nextOpenRow(board, column):
    for i in range(rows):
        if board[i][column] == pieces[0]:
            return i

def isValidMove(board, col):
    return board[rows - 1][col] == pieces[0]

def startTwoPlayerGame():
    board = createBoard()
    printBoard(board)

    pygame.init()

    drawBoard(board)

    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
				    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			    else: 
				    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if isValidMove(board, col):
                        row = nextOpenRow(board, col)
                        dropV2(board, row, col, p1)
                        
                        if isFull(board):
                            text = myfont.render('Game is tied!', 1, RED)
                            screen.blit(text, (40, 10))
                            game_over = True
                        
                        if win(p1, board):
                            text = myfont.render('Congratulations ' + p1.name + '!', 1, RED)
                            screen.blit(text, (40, 10))
                            game_over = True
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if isValidMove(boarc, col):
                        row = nextOpenRow(board, col)
                        dropV2(board, row, col, p2)

                        if isFull(board):
                            text = myfont.render('Game is tied!', 1, YELLOW)
                            screen.blit(text, (40, 10))
                            game_over = True
                        
                        if win(p2, board):
                            text = myfont.render('Congratulations ' + p2.name + '!', 1, YELLOW)
                            screen.blit(text, (40, 10))
                            game_over = True
                
                print_board(board)
                draw_board(board)

                turn += 1
                turn %= 2
                
                if game_over:
                    pygame.time.wait(3000)
    startTwoPlayerGame()

def win(player, board):
    # Checking Horizontally
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == player.piece:
                if board[i + 1][j] == player.piece:
                    if board[i + 2][j] == player.piece:
                        if board[i + 3][j] == player.piece:
                            return True
    # Checking vertically
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i][j + 1] == player.piece:
                    if board[i][j + 2] == player.piece:
                        if board[i][j + 3] == player.piece:
                            return True
    # Checking diagonally /
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == player.piece:
                if board[i + 1][j - 1] == player.piece:
                    if board[i + 2][j - 2] == player.piece:
                        if board[i + 3][j - 3] == player.piece:
                            return True
    # Checking diagonally \
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i + 1][j + 1] == player.piece:
                    if board[i + 2][j + 2] == player.piece:
                        if board[i + 3][j + 3] == player.piece:
                            return True
    return False

def dropV2(board, row, col, player):
    board[row][col] = player.piece

def isFull(board):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == pieces[0]:
                return False
    return True

def drop(player, board):
    if player.name != 'bot':
        print('\nIt is your turn to drop a ' +
              player.piece + ' piece, ' + player.name + '!')
        pickColumn = input('\nWhich column would you like to drop you piece in?\n' +
                           player.name + ', pick from column 1-7?')
        for i in reversed(board):
            if i[int(pickColumn) - 1] == pieces[0]:
                i[int(pickColumn) - 1] = player.piece
                return True
    return False

def chooseTwoPlayer():
    print('Player 1: ')
    print('What is your name')
    name = input()
    p1 = Player.Player(name, pieces[1])
    print('Player 2: ')
    print('What is your name')
    name1 = input()
    if name1 == 'bot':
        print('Error Occurred! Pick a different name!')
        chooseTwoPlayer()
    p2 = Player.Player(name1, pieces[2])
    return p1, p2

# Main Method
if __name__ == "__main__":
    choice = 0
    p1, p2 = chooseTwoPlayer()
    startTwoPlayerGame()
    print('I hope you enjoyed the game!')
