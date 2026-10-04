import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Coin Collector')

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 50))
        self.image.fill('dodgerblue')

        self.rect = self.image.get_rect(center=(150, 250))

        self.speed = 300

        self.score = 0

    def update(self, dt) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt

        self.rect.clamp_ip(screen.get_rect())


class CoinSprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple, value: int):
        super().__init__()

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            'gold',
            (12, 12),
            12
        )

        self.rect = self.image.get_rect(center=position)

        self.value = value


player = PlayerSprite()

player_group = pygame.sprite.Group(player)
coin_group = pygame.sprite.Group()

for _ in range(10):
    position = (
        random.randint(30, 770),
        random.randint(30, 470)
    )
    value = random.randint(1, 10)

    coin = CoinSprite(position, value)
    coin_group.add(coin)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    collected_coins = pygame.sprite.spritecollide(
        player,
        coin_group,
        dokill=True
    )

    player_group.update(dt)

    for coin in collected_coins:
        player.score += coin.value

    screen.fill('#20252b')

    coin_group.draw(screen)
    player_group.draw(screen)

    score_text = font.render(
        f"Score: {player.score}",
        True,
        'white'
    )
    screen.blit(score_text, (20, 20))

    if len(coin_group) == 0:
        win_text = font.render(
            'You collected all coins!',
            True,
            'gold'
        )
        screen.blit(win_text, (240, 230))

    pygame.display.flip()

pygame.quit()
