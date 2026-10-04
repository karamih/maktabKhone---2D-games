import pygame

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    GRID_COLOR,
    SEGMENT_SIZE
)

from game import Game
from ui import GameUI

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake: Gold Rush")

clock = pygame.time.Clock()

game_sound = pygame.mixer.Sound('assets/mixkit-game-level-music-689.wav')

game = Game()
ui = GameUI()

running = True

while running:
    pygame.mixer.Sound.play(game_sound)

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.set_direction(pygame.Vector2(0, -1))
            elif event.key == pygame.K_DOWN:
                game.snake.set_direction(pygame.Vector2(0, 1))
            elif event.key == pygame.K_RIGHT:
                game.snake.set_direction(pygame.Vector2(1, 0))
            elif event.key == pygame.K_LEFT:
                game.snake.set_direction(pygame.Vector2(-1, 0))

    keys = pygame.key.get_pressed()
    boost_requested = keys[pygame.K_SPACE]

    game.update(dt, boost_requested)

    screen.fill(BACKGROUND_COLOR)

    for x in range(0, WIDTH, SEGMENT_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, SEGMENT_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
        )

    game.snake.draw(screen)
    game.items.draw(screen)

    ui.draw(
        screen,
        score=game.score,
        gold=game.gold,
        snake_length=len(game.snake.segments),
        boosting=game.boosting
    )

    pygame.display.flip()

pygame.quit()
