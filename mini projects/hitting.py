import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Sprite Collision')

clock = pygame.time.Clock()


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50, 50))
        self.image.fill('dodgerblue')

        self.rect = self.image.get_rect(center=(150, 250))

        self.speed = 250

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


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()

        self.image = pygame.Surface((70, 70))
        self.image.fill('tomato')

        self.rect = self.image.get_rect(center=position)


player = PlayerSprite()
enemy = EnemySprite(position=(400, 250))
enemy2 = EnemySprite(position=(300, 300))
enemy3 = EnemySprite(position=(450, 200))

player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group(enemy, enemy2, enemy3)

font = pygame.font.Font(None, 36)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    player_group.update(dt)

    # if pygame.sprite.collide_rect(player, enemy):
    #     enemy.kill()

    if pygame.sprite.spritecollide(player, enemy_group, dokill=True):
        pass

    screen.fill('white')

    player_group.draw(screen)
    enemy_group.draw(screen)

    if len(enemy_group) == 0:
        text = font.render('Enemy defeated!', True, 'black')
        screen.blit(text, (200, 200))

    pygame.display.flip()
