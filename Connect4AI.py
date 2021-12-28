import Player
import math
import random
import sys, pygame
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

# Functions


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
    print('  1    2    3    4    5    6    7')


def startTwoPlayerGame():
    board = createBoard()
    printBoard(board)
    while True:
        drop(p1, board)
        printBoard(board)
        if win(p1, board):
            print('Congratulations ' + p1.name +
                  '!\nYou have won with the ' + p1.piece + ' pieces!')
            break
        if isFull(board):
            print('Game is tied')
            break
        drop(p2, board)  # AI FUNCTION
        printBoard(board)
        if win(p2, board):
            print('\nCongratulations ' + p2.name +
                  '!\nYou have won with the ' + p2.piece + ' pieces!')
            break
        if isFull(board):
            print('Game is tied')
            break
    playAgain = input('Would you like to play another game?\n 1.Yes or 2.No')
    if int(playAgain) == 1:
        startTwoPlayerGame()


def startOnePlayerGame():
    board = createBoard()
    printBoard(board)
    while True:
        drop(p1, board)
        printBoard(board)
        if win(p1, board):
            print('Congratulations ' + p1.name +
                  '!\nYou have won with the ' + p1.piece + ' pieces!')
            break
        if isFull(board):
            print('Game is tied')
            break
        AIPlayerDrop(p2, p1, board)  # AI FUNCTION
        printBoard(board)
        if win(p2, board):
            print('\nCongratulations!\nYou have won!')
            break
        if isFull(board):
            print('Game is tied')
            break
    playAgain = input('Would you like to play another game?\n 1.Yes or 2.No')
    if int(playAgain) == 1:
        startOnePlayerGame()


def noMovesLeft(board):
    if len(allValidLocations(board)) == 0:
        return True
    else:
        return False


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


def winCondition(board, AIplayer):
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j] == AIplayer.piece:
                    if board[i + 2][j] == AIplayer.piece:
                        if board[i + 3][j] == pieces[0]:
                            return True

    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i][j + 1] == AIplayer.piece:
                    if board[i][j + 2] == AIplayer.piece:
                        if board[i][j + 3] == pieces[0]:
                            return True

    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j - 1] == AIplayer.piece:
                    if board[i + 2][j - 2] == AIplayer.piece:
                        if board[i + 3][j - 3] == pieces[0]:
                            return True

    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j + 1] == AIplayer.piece:
                    if board[i + 2][j + 2] == AIplayer.piece:
                        if board[i + 3][j + 3] == pieces[0]:
                            return True
    return False


def isFull(board):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == pieces[0]:
                return False
    return True


def minimax(board, depth, alpha, beta, maximizingPlayer, AIPlayer, player):
    validDropSites = allValidLocations(board)
    if depth == 0 or winCondition(board, AIPlayer) or winCondition(board, player) or noMovesLeft(board):
        if winCondition(board, AIPlayer) or winCondition(board, player) or noMovesLeft(board):
            if winCondition(board, AIPlayer):
                return [None, 1000]
            elif winCondition(board, player):
                return [None, -1000]
            elif noMovesLeft(board):
                return [None, 0]
        else:
            return [None, evaluate(player, AIPlayer, board)]
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(validDropSites)
        for i in validDropSites:
            row = nextOpenRow(board, i)
            copyBoard = board.copy()
            pretendDrop(copyBoard, row, column, AIPlayer)
            newScore = minimax(copyBoard, depth-1, alpha,
                               beta, False, AIPlayer, player)[1]
            if newScore > value:
                value = newScore
                column = i
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(validDropSites)
        for i in validDropSites:
            row = nextOpenRow(board, i)
            copyBoard = board.copy()
            pretendDrop(copyBoard, row, column, player)
            newScore = minimax(copyBoard, depth-1, alpha,
                               beta, True, AIPlayer, player)[1]
            if newScore < value:
                value = newScore
                column = i
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def nextOpenRow(board, column):
    for i in range(rows):
        if board[i][column] == pieces[0]:
            return i


def isValidMove(board, col):
    return board[rows - 1][col] == pieces[0]


def allValidLocations(board):
    locations = []
    for i in range(columns):
        if isValidMove(board, i):
            locations.append(i)
    return locations


def scoreColumns(player, AIplayer, board):
    score = 0
    # 4 in a row - AI
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i][j + 1] == AIplayer.piece:
                    if board[i][j + 2] == AIplayer.piece:
                        if board[i][j + 3] == AIplayer.piece:
                            return 1000
    # 3 in a row - AI
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i][j + 1] == AIplayer.piece:
                    if board[i][j + 2] == AIplayer.piece:
                        if board[i][j + 3] == pieces[0]:
                            score += 100
    # 2 in a row - AI
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i][j + 1] == AIplayer.piece:
                    if board[i][j + 2] == pieces[0]:
                        if board[i][j + 3] == pieces[0]:
                            score += 10
     # 4 in a row - player
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i][j + 1] == player.piece:
                    if board[i][j + 2] == player.piece:
                        if board[i][j + 3] == player.piece:
                            return -1000
    # 3 in a row - player
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i][j + 1] == player.piece:
                    if board[i][j + 2] == player.piece:
                        if board[i][j + 3] == pieces[0]:
                            score -= 100
    # 2 in a row - player
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i][j + 1] == player.piece:
                    if board[i][j + 2] == pieces[0]:
                        if board[i][j + 3] == pieces[0]:
                            score -= 10
    return score


def scoreRows(player, AIplayer, board):
    score = 0
    # 4 in a row - AI
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j] == AIplayer.piece:
                    if board[i + 2][j] == AIplayer.piece:
                        if board[i + 3][j] == AIplayer.piece:
                            return 1000
    # 3 in a row - AI
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j] == AIplayer.piece:
                    if board[i + 2][j] == AIplayer.piece:
                        if board[i + 3][j] == pieces[0]:
                            score += 100
    # 2 in a row - AI
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j] == AIplayer.piece:
                    if board[i + 2][j] == pieces[0]:
                        if board[i + 3][j] == pieces[0]:
                            score += 10
    # 4 in a row - player
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == player.piece:
                if board[i + 1][j] == player.piece:
                    if board[i + 2][j] == player.piece:
                        if board[i + 3][j] == player.piece:
                            return -1000
    # 3 in a row - player
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == player.piece:
                if board[i + 1][j] == player.piece:
                    if board[i + 2][j] == player.piece:
                        if board[i + 3][j] == pieces[0]:
                            score -= 100
    # 2 in a row - player
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == player.piece:
                if board[i + 1][j] == player.piece:
                    if board[i + 2][j] == pieces[0]:
                        if board[i + 3][j] == pieces[0]:
                            score -= 10
    return score


def scoreDiagonals(player, AIplayer, board):
    score = 0
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j - 1] == AIplayer.piece:
                    if board[i + 2][j - 2] == AIplayer.piece:
                        if board[i + 3][j - 3] == AIplayer.piece:
                            return 1000
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j - 1] == AIplayer.piece:
                    if board[i + 2][j - 2] == AIplayer.piece:
                        if board[i + 3][j - 3] == pieces[0]:
                            score += 100
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j - 1] == AIplayer.piece:
                    if board[i + 2][j - 2] == pieces[0]:
                        if board[i + 3][j - 3] == pieces[0]:
                            score += 10
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == player.piece:
                if board[i + 1][j - 1] == player.piece:
                    if board[i + 2][j - 2] == player.piece:
                        if board[i + 3][j - 3] == player.piece:
                            return -1000
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == player.piece:
                if board[i + 1][j - 1] == player.piece:
                    if board[i + 2][j - 2] == player.piece:
                        if board[i + 3][j - 3] == pieces[0]:
                            score -= 100
    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == player.piece:
                if board[i + 1][j - 1] == player.piece:
                    if board[i + 2][j - 2] == pieces[0]:
                        if board[i + 3][j - 3] == pieces[0]:
                            score -= 10
    return score


def scoreReverseDiagonals(player, AIplayer, board):
    score = 0
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j + 1] == AIplayer.piece:
                    if board[i + 2][j + 2] == AIplayer.piece:
                        if board[i + 3][j + 3] == AIplayer.piece:
                            return 1000
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j + 1] == AIplayer.piece:
                    if board[i + 2][j + 2] == AIplayer.piece:
                        if board[i + 3][j + 3] == pieces[0]:
                            score += 100
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j + 1] == AIplayer.piece:
                    if board[i + 2][j + 2] == pieces[0]:
                        if board[i + 3][j + 3] == pieces[0]:
                            score += 10
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i + 1][j + 1] == player.piece:
                    if board[i + 2][j + 2] == player.piece:
                        if board[i + 3][j + 3] == player.piece:
                            return -1000
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i + 1][j + 1] == player.piece:
                    if board[i + 2][j + 2] == player.piece:
                        if board[i + 3][j + 3] == pieces[0]:
                            score -= 100
    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == player.piece:
                if board[i + 1][j + 1] == player.piece:
                    if board[i + 2][j + 2] == pieces[0]:
                        if board[i + 3][j + 3] == pieces[0]:
                            score -= 10
    return score


def evaluate(player, AIplayer, board):
    score = 0
    score += scoreColumns(player, AIplayer, board)
    score += scoreRows(player, AIplayer, board)
    score += scoreDiagonals(player, AIplayer, board)
    score += scoreReverseDiagonals(player, AIplayer, board)
    return score


def pretendDrop(board, row, col, player):
    board[row][col] = player.piece


def winningMove(board, AIplayer):
    for i in range(rows - 3):
        for j in range(columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j] == AIplayer.piece:
                    if board[i + 2][j] == AIplayer.piece:
                        if board[i + 3][j] == pieces[0]:
                            return i + 3, j

    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i][j + 1] == AIplayer.piece:
                    if board[i][j + 2] == AIplayer.piece:
                        if board[i][j + 3] == pieces[0]:
                            return i, j + 3

    for i in range(rows - 3):
        for j in range(3, columns):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j - 1] == AIplayer.piece:
                    if board[i + 2][j - 2] == AIplayer.piece:
                        if board[i + 3][j - 3] == pieces[0]:
                            return i + 3, j - 3

    for i in range(rows - 3):
        for j in range(columns - 3):
            if board[i][j] == AIplayer.piece:
                if board[i + 1][j + 1] == AIplayer.piece:
                    if board[i + 2][j + 2] == AIplayer.piece:
                        if board[i + 3][j + 3] == pieces[0]:
                            return i + 3, j + 3
    return None, None


def AIPlayerDrop(AIplayer, player, board):
    list = minimax(board, 5, -math.inf, math.inf, True, AIplayer, player)
    if list is None:
        if winCondition(board, AIplayer):
            if isFull(board):
                return False
            else:
                r, c = winningMove(board, AIplayer)
                pretendDrop(board, r, c, AIplayer)
        else:
            locations = allValidLocations(board)
            c = -1
            while locations.count(c) == 0:
                c = random.randint(0, 6)
            for i in reversed(board):
                if i[c] == pieces[0]:
                    i[c] = AIplayer.piece
                    return True
    else:
        if list[0] is None:
            if isFull(board):
                print('line 503')
                return False
            else:
                r, c = winningMove(board, AIplayer)
                pretendDrop(board, r, c, AIplayer)
        if isValidMove(board, list[0]):
            r = nextOpenRow(board, list[0])
            pretendDrop(board, r, list[0], AIplayer)
            print('pretendDrop occurred')
            return True
    return False


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


def chooseOnePlayer():
    print('Player 1: ')
    print('What is your name')
    name = input()
    if name == 'bot':
        print('Error Occurred! Pick a different name!')
        chooseOnePlayer()
    p1 = Player.Player(name, pieces[1])
    p2 = Player.Player('bot', pieces[2])
    return p1, p2


# Main Method
if __name__ == "__main__":
    choice = 0
    while True:
        choice = int(
            input('What Game Mode do you want?\n1. Two Player Mode\n2. One Player Mode'))
        if choice == 1:
            p1, p2 = chooseTwoPlayer()
            break
        elif choice == 2:
            p1, p2 = chooseOnePlayer()
            break
        else:
            print('Error Occurred\nEnter a valid input!')
            continue
    if p2.name == 'bot':
        startOnePlayerGame()
    else:
        startTwoPlayerGame()
    print('I hope you enjoyed the game!')
