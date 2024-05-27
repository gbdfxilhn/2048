import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
TIMER = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font('freesansbold.ttf', 24)

colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light_text': (249, 246, 242),
    'dark_text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}

board_values = [[0] * 4 for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''

def draw_game_over():
    pygame.draw.rect(SCREEN, 'black', (50, 50, 300, 100), border_radius=10)
    text1 = FONT.render('Game Over!', True, 'white')
    text2 = FONT.render('Press Enter to Restart', True, 'white')
    SCREEN.blit(text1, (130, 65))
    SCREEN.blit(text2, (70, 105))

def update_board(direction, board, score):
    merged = [[False] * 4 for _ in range(4)]
    if direction == 'UP':
        for j in range(4):
            for i in range(1, 4):
                if board[i][j] != 0:
                    k = i
                    while k > 0 and board[k - 1][j] == 0:
                        board[k - 1][j], board[k][j] = board[k][j], 0
                        k -= 1
                    if k > 0 and board[k - 1][j] == board[k][j] and not merged[k - 1][j]:
                        board[k - 1][j] *= 2
                        score += board[k - 1][j]
                        board[k][j] = 0
                        merged[k - 1][j] = True

    elif direction == 'DOWN':
        for j in range(4):
            for i in range(2, -1, -1):
                if board[i][j] != 0:
                    k = i
                    while k < 3 and board[k + 1][j] == 0:
                        board[k + 1][j], board[k][j] = board[k][j], 0
                        k += 1
                    if k < 3 and board[k + 1][j] == board[k][j] and not merged[ k+ 1][j]:
                        board[k + 1][j] *= 2
                        score += board[k + 1][j]
                        board[k][j] = 0
                        merged[k + 1][j] = True

    elif direction == 'LEFT':
        for i in range(4):
            for j in range(1, 4):
                if board[i][j] != 0:
                    k = j
                    while k > 0 and board[i][k - 1] == 0:
                        board[i][k - 1], board[i][k] = board[i][k], 0
                        k -= 1
                    if k > 0 and board[i][k - 1] == board[i][k] and not merged[i][k - 1]:
                        board[i][k - 1] *= 2
                        score += board[i][k - 1]
                        board[i][k] = 0
                        merged[i][k - 1] = True

    elif direction == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):
                if board[i][j] != 0:
                    k = j
                    while k < 3 and board[i][k + 1] == 0:
                        board[i][k + 1], board[i][k] = board[i][k], 0
                        k += 1
                    if k < 3 and board[i][k + 1] == board[i][k] and not merged[i][k + 1]:
                        board[i][k + 1] *= 2
                        score += board[i][k + 1]
                        board[i][k] = 0
                        merged[i][k + 1] = True
    return board, score

def spawn_new_piece(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 4 if random.randint(1, 10) == 10 else 2
    return board, not empty_cells

def render_board(score, high_score):
    pygame.draw.rect(SCREEN, colors['bg'], (0, 0, WIDTH, WIDTH), border_radius=10)
    score_text = FONT.render(f'Score: {score}', True, 'black')
    high_score_text = FONT.render(f'High Score: {high_score}', True, 'black')
    SCREEN.blit(score_text, (10, 410))
    SCREEN.blit(high_score_text, (10, 450))

def render_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = colors.get(value, colors['other'])
            value_color = colors['light_text'] if value > 8 else colors['dark_text']
            pygame.draw.rect(SCREEN, color, (j * 97.5 + 10, i * 97.5 + 10, 87.5, 87.5), border_radius=5)
            if value:
                value_text = pygame.font.SysFont('comicsans', 48 - 5 * len(str(value)), bold=True).render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 97.5 + 53.75, i * 97.5 + 53.75))
                SCREEN.blit(value_text, text_rect)
