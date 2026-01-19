import pygame
import sys
from game_state import GameState
from constants import *

# ----------- Initialize Pygame -----------
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chessboard - Pygame")

clock = pygame.time.Clock()

def load_piece_images():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP',
              'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(
            pygame.image.load(f'images/{piece}.png'),
            (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images

# ----------- Draw Chessboard -----------
def draw_board(surface, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(surface, color, rect)

            piece = board[row][col]
            if piece != "--":
                surface.blit(
                    piece_images[piece],
                    (col * SQUARE_SIZE, row * SQUARE_SIZE)
                )

game_state = GameState()
piece_images = load_piece_images()

# ----------- Main Loop -----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(screen, game_state.board)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
