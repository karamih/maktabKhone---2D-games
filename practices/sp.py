import pygame

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()


def crop_sheet(sheet_addr, column, row, w, h):
    sheet_img = pygame.image.load(sheet_addr).convert_alpha()
    return sheet_img.subsurface(column * w, row * h, w, h)


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, speed: int, flip: bool = False):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load('../assets/birdd.png').convert_alpha(), (64, 64))
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.flip = flip

    def update(self, dt) -> None:
        if self.flip:
            self.rect.x -= dt * self.speed
        else:
            self.rect.x += dt * self.speed


enemy1 = EnemySprite(pos=(100, 200), speed=150)
enemy2 = EnemySprite(pos=(400, 100), speed=50, flip=True)
enemy3 = EnemySprite(pos=(300, 400), speed=100)

bird_enemies = pygame.sprite.Group()
bird_enemies.add(enemy1, enemy2, enemy3)

# sheet = pygame.image.load('assets/handball-characters.png')
# boy_image = sheet.subsurface(2300, 370, 1200, 2000)
# boy_img_transformed = pygame.transform.smoothscale(boy_image, (100, 150))
# boy_img_rect = boy_img_transformed.get_rect(
#     center=screen.get_rect().center
# )

frame = crop_sheet('assets/Hero.png', 4, 0, 16, 16)
frame = pygame.transform.smoothscale(frame, (64, 64))
frame_rect = frame.get_rect(center=screen.get_rect().center)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    screen.fill('white')

    bird_enemies.update(dt)
    bird_enemies.draw(screen)
    # screen.blit(boy_img_transformed, boy_img_rect)

    # screen.blit(frame, frame_rect)

    pygame.display.flip()
