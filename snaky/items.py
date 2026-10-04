import random
import pygame

from settings import (
    WIDTH,
    HEIGHT,
    ITEM_LIFETIME,
    SEGMENT_SIZE,
    FOOD_SCORE,
    FOOD_GROWTH,
    FOOD_COLOR,
    GOLD_SCORE,
    GOLD_VALUE,
    GOLD_COLOR
)

ITEM_TYPES = {
    'food': {
        'color': FOOD_COLOR,
        'radius': 7,
        'score': FOOD_SCORE,
        'growth': FOOD_GROWTH,
        'gold': 0,
        'lifetime': ITEM_LIFETIME
    },
    'gold': {
        'color': GOLD_COLOR,
        'radius': 10,
        'score': GOLD_SCORE,
        'growth': 0,
        'gold': GOLD_VALUE,
        'lifetime': ITEM_LIFETIME
    }
}


class WorldItem:
    def __init__(self, item_type: dict, position: pygame.Vector2):
        self.item_type = item_type
        self.position = position

        config = ITEM_TYPES[item_type]

        self.color = config['color']
        self.radius = config['radius']
        self.score = config['score']
        self.growth = config['growth']
        self.gold = config['gold']
        self.lifetime = config['lifetime']

        self.remaining_time = self.lifetime

    def update(self, dt):
        self.remaining_time -= dt

    @property
    def expired(self):
        return self.remaining_time <= 0

    def collides_with(self, position):
        distance = self.position.distance_to(position)
        return distance < self.radius + SEGMENT_SIZE / 2

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (round(self.position.x), round(self.position.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (round(self.position.x - self.radius / 3),
             round(self.position.y - self.radius / 3)),
            max(1, self.radius // 3)
        )


class ItemManager:
    def __init__(self, snake, max_items=4):
        self.snake = snake
        self.max_items = max_items
        self.items: list[WorldItem] = []

    def random_position(self):
        margin = SEGMENT_SIZE * 2

        for _ in range(100):
            position = pygame.Vector2(
                random.randint(margin, WIDTH - margin),
                random.randint(margin, HEIGHT - margin)
            )

            overlaps_snake = any(
                position.distance_to(segment) < SEGMENT_SIZE * 2
                for segment in self.snake.segments
            )

            overlaps_item = any(
                position.distance_to(item.position) < SEGMENT_SIZE * 2
                for item in self.items
            )

            if not overlaps_snake and not overlaps_item:
                return position

        return pygame.Vector2(WIDTH / 2, HEIGHT / 2)

    def spawn_item(self):
        item_type = random.choices(
            ['food', 'gold'],
            weights=[0.7, 0.3],
            k=1
        )[0]

        position = self.random_position()
        self.items.append(WorldItem(item_type, position))

    def update(self, dt):
        for item in self.items:
            item.update(dt)

        self.items = [
            item for item in self.items if not item.expired
        ]

        while len(self.items) < self.max_items:
            self.spawn_item()

    def collect_at(self, position):
        collected = []

        for item in self.items:
            if item.collides_with(position):
                collected.append(item)
                self.items.remove(item)

        return collected

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)
