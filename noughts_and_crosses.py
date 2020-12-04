import pygame as pg
from pygame.locals import *
import random, sys
import minimax

WIDTH, HEIGHT = 650, 650    # Window size
EDGE = 7    # Grid line width

board = [[None]*3 for i in range(3)]   # Grid where square is False if it's empty, otherwise contains name of player that occupies it
empty = [(1, 1), (3, 1), (5, 1), (1, 3), (3, 3), (5, 3), (1, 5), (3, 5), (5, 5)]    # Remaining positions
turn = True

fg_colour = pg.Color((0, 0, 0))
bg_colour = pg.Color((255, 255, 255))

pg.init()
msg_font = pg.font.SysFont(None, 170, bold=True)
msg_colour = (16, 119, 73)
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(bg_colour)

class Player:
    size = (100, 100)

    def __init__(self, image, player):
        self.image = pg.transform.scale(pg.image.load(image).convert(), self.size)
        self.player = player

    def which_box(self, pos, axis):
        if axis == "x":
            dim = WIDTH
        else:
            dim = HEIGHT
        if pos < dim // 3:
            return 1
        elif pos > dim // 3 and pos < 2 * (dim // 3):
            return 3
        elif pos > 2 * (dim // 3):
            return 5

    def place_symbol(self):
        global board, empty

        # human
        if self.player == "x":
            x_pos, y_pos = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
            x, y = self.which_box(x_pos, "x"), self.which_box(y_pos, "y")
            if x == None or y == None:
                return

        # cpu
        if self.player == "o":
            (x, y) = minimax.find_best_move(board)
            (x, y) = (x*2 + 1, y*2 + 1)

        screen.blit(self.image, (x * (WIDTH // 6) - self.size[0] // 2, y * (HEIGHT // 6) - self.size[1] // 2))
        empty.remove((x, y))
        board[(y-1)//2][(x-1)//2] = self.player

    def check_won(self, board):
        if board[0][0] == self.player and board[1][1] == self.player and board[2][2] == self.player:
            return True
        elif board[0][2] == self.player and board[1][1] == self.player and board[2][0] == self.player:
            return True
        else:
            for i in range(3):
                if board[0][i] == self.player and board[1][i] == self.player and board[2][i] == self.player:
                    return True
                elif board[i][0] == self.player and board[i][1] == self.player and board[i][2] == self.player:
                    return True
        return False


# Initialise nought and cross
cpu = Player("nought.jpg", "o")    # cpu is nought
human = Player("cross.png", "x")    # human is cross

# Draw grid
pg.draw.rect(screen, fg_colour, pg.Rect(0, HEIGHT - EDGE, WIDTH, EDGE))
for i in range(0, HEIGHT, HEIGHT // 3):
    pg.draw.rect(screen, fg_colour, pg.Rect(0, i, WIDTH, EDGE))
pg.draw.rect(screen, fg_colour, pg.Rect(WIDTH - EDGE, 0, EDGE, HEIGHT))
for i in range(0, WIDTH, WIDTH // 3):
    pg.draw.rect(screen, fg_colour, pg.Rect(i, 0, EDGE, HEIGHT))

def is_game_finished(board, empty):
    """
    Display different message depending on whether game is a win, loss or draw. Then quit the game.
    """
    text = ""
    if human.check_won(board):
        text = "You win!"
    elif cpu.check_won(board):
        text = "You lose!"
    elif len(empty) == 0:
        text = "Draw"
    else:
        return

    msg_surface = msg_font.render(text, False, msg_colour)
    pg.time.wait(500)
    screen.fill(pg.Color(0, 0, 0))
    screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2 - msg_surface.get_height() // 2))
    pg.display.flip()
    pg.time.wait(2000)
    pg.quit()
    sys.exit()

# Main game loop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and turn == True:
            human.place_symbol()
            turn = False
    
    pg.display.flip()

    is_game_finished(board, empty)

    if turn == False:
        pg.time.wait(500)
        cpu.place_symbol()
        turn = True

    pg.display.flip()
