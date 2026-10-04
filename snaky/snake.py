import pygame

from settings import (
    WIDTH,
    HEIGHT,
    SEGMENT_SIZE,
    INITIAL_SPEED,
    INITIAL_LENGTH,
    SNAKE_COLOR,
    SNAKE_HEAD_COLOR,
    BOOST_MULTIPLIER
)


class Snake:
    def __init__(self):
        self.direction = pygame.Vector2(1, 0)
        self.speed = INITIAL_SPEED

        start = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

        self.segments = [
            start - pygame.Vector2(i * SEGMENT_SIZE, 0)
            for i in range(INITIAL_LENGTH)
        ]

        self.growth_pending = 0
        self.move_time = 0

    @property
    def head(self):
        return self.segments[0]

    def set_direction(self, direction: pygame.Vector2):
        if direction.length_squared() == 0:
            return

        direction = direction.normalize()

        if direction == -self.direction:
            return

        self.direction = direction

    def grow(self, amount: int = 1):
        self.growth_pending += amount

    def update(self, dt, boosting=False):
        speed = self.speed

        if boosting:
            speed *= BOOST_MULTIPLIER

        self.move_time += speed * dt

        while self.move_time >= SEGMENT_SIZE:
            self.move_time -= SEGMENT_SIZE

            new_head = self.head + self.direction * SEGMENT_SIZE

            new_head.x %= WIDTH
            new_head.y %= HEIGHT

            self.segments.insert(0, new_head)

            if self.growth_pending > 0:
                self.growth_pending -= 1
            else:
                self.segments.pop()

    def draw(self, screen: pygame.Surface):
        for index, segment in enumerate(self.segments):
            color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_COLOR

            rect = pygame.Rect(
                round(segment.x - SEGMENT_SIZE / 2),
                round(segment.y - SEGMENT_SIZE / 2),
                SEGMENT_SIZE - 2,
                SEGMENT_SIZE - 2
            )

            pygame.draw.rect(screen, color, rect, border_radius=5)
