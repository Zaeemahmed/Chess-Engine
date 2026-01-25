import pygame
import sys
from game_state import GameState
from move_generator import MoveGenerator
from move import Move
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
def draw_board(surface, board, possible_moves=[]):
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

            if((row, col) in possible_moves):
                pygame.draw.rect(surface, HIGHLIGHT_COLOR, rect, 5)

game_state = GameState()
move_generator = MoveGenerator()
piece_images = load_piece_images()

possible_moves = []

# ----------- Main Loop -----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // SQUARE_SIZE
            row = mouse_y // SQUARE_SIZE
            print(f"Clicked on square: ({row}, {col})")

            # Two cases: piece is not selected or piece is selected
            if(game_state.square_selected == ()):
                if(game_state.board[row][col] != "--" and game_state.board[row][col][0] == game_state.player_turn):
                    game_state.square_selected = (row, col)
                    possible_moves = move_generator.generate_moves(game_state.board, (row, col))
                else:
                    continue
            
            else:
                if(game_state.square_selected == (row, col) or game_state.board[row][col][0] == game_state.player_turn or (row, col) not in possible_moves):
                    if(game_state.board[row][col][0] == game_state.player_turn):
                        game_state.square_selected = (row, col)
                        possible_moves = move_generator.generate_moves(game_state.board, (row, col))
                    continue
                start_sq = game_state.square_selected
                end_sq = (row, col)
                move = Move(start_sq, end_sq, game_state.board)
                game_state.make_move(move)
                game_state.square_selected = ()
                possible_moves = []

    draw_board(screen, game_state.board, possible_moves)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
