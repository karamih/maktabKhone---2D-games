import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Survival Game')

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

game_over = False


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 50))
        self.image.fill('dodgerblue')

        self.rect = self.image.get_rect(center=(150, 250))

        self.speed = 300

        self.health = 3
        self.invincible = False
        self.invincible_timer = 0

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

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

    def take_damage(self):
        if self.invincible:
            return

        self.health -= 1
        self.invincible = True
        self.invincible_timer = 1.0


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()

        self.image = pygame.Surface((40, 40))
        self.image.fill('tomato')
        self.rect = self.image.get_rect(center=position)


player = PlayerSprite()
player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group()

for _ in range(5):
    position = (
        random.randint(50, 750),
        random.randint(50, 450)
    )
    enemy_group.add(EnemySprite(position))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    if not game_over:
        player_group.update(dt)

        if pygame.sprite.spritecollide(
                player,
                enemy_group,
                dokill=False
        ):
            player.take_damage()

        if player.health <= 0:
            game_over = True

    screen.fill('#20252b')

    enemy_group.draw(screen)

    if not player.invincible or int(pygame.time.get_ticks() / 100) % 2 == 0:
        player_group.draw(screen)

    health_text = font.render(
        f'Health: {player.health}',
        True,
        'white'
    )
    screen.blit(health_text, (20, 20))

    if game_over:
        game_over_text = font.render(
            'Game Over',
            True,
            'tomato'
        )
        screen.blit(
            game_over_text,
            game_over_text.get_rect(center=screen.get_rect().center)
        )

    pygame.display.flip()
pygame.quit()
