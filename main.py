import pygame
from game import *

score = 0
with open('high_score', 'r') as file:
    init_high = int(file.readline())
high_score = init_high

run = True
while run:
    timer.tick(fps)
    screen.fill('gray')


    render_board(score, high_score)
    render_pieces(board_values)


    if spawn_new or init_count < 2:
        board_values, game_over = spawn_new_piece(board_values)
        spawn_new = False
        init_count += 1


    if direction:
        board_values, score = update_board(direction, board_values, score)
        direction = ''
        spawn_new = True

    if game_over:
        draw_game_over()
        if score > high_score:
            high_score = score
            with open('high_score', 'a') as file:
                file.write(f'{high_score}\n')
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0] * 4 for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    direction = ''
                    game_over = False
            else:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

    pygame.display.flip()

pygame.quit()
