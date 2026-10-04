from settings import (
    ITEM_LIMIT,
    INITIAL_GOLD,
    BOOST_GOLD_COST
)

from snake import Snake
from items import ItemManager


class Game:
    def __init__(self):
        self.snake = Snake()
        self.items = ItemManager(snake=self.snake, max_items=ITEM_LIMIT)

        self.score = 0
        self.gold = INITIAL_GOLD

        self.boosting = False

    def update(self, dt, boost_requested=False):
        self.boosting = boost_requested and self.gold > 0

        if self.boosting:
            self.gold -= BOOST_GOLD_COST * dt
            self.gold = max(0, self.gold)

            if self.gold <= 0:
                self.boosting = False

        self.snake.update(dt, boosting=self.boosting)

        self.items.update(dt)

        collected_items = self.items.collect_at(
            self.snake.head
        )

        for item in collected_items:
            self.score += item.score
            self.gold += item.gold

            if item.growth > 0:
                self.snake.grow(item.growth)
