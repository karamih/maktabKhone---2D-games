import pygame

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

player_img = pygame.image.load('../assets/Hero.png').convert_alpha()


def crop_sheet(img, column, row, w, h):
    return img.subsurface(column * w, row * h, w, h)


def create_frames(row, start_column, count):
    frames = []

    for column in range(start_column, start_column + count):
        frame = crop_sheet(player_img, column, row, 16, 16)
        frame = pygame.transform.smoothscale(frame, (64, 64))

        frames.append(frame)

    return frames


idle_frames = create_frames(0, 4, 1)
walk_left_frames = create_frames(1, 0, 4)
walk_right_frames = create_frames(1, 4, 4)
attack_frames = create_frames(2, 4, 4)

animations = {
    'idle': {'frames': idle_frames,
             'loop': True},
    'walk_left': {'frames': walk_left_frames,
                  'loop': True},
    'walk_right': {'frames': walk_right_frames,
                   'loop': True},
    'attack': {
        'frames': attack_frames,
        'loop': False
    }
}


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, animations: dict):
        super().__init__()
        self.animations = animations
        self.current_animation = 'idle'

        self.frame_index = 0
        self.animation_timer = 0

        self.image = self.animations[self.current_animation]['frames'][self.frame_index]
        self.rect = self.image.get_rect(center=screen.get_rect().center)

        self.speed = 200

        self.is_attacking = False

    def set_animation(self, animation_name):
        if self.current_animation == animation_name:
            return

        self.current_animation = animation_name

        self.frame_index = 0
        self.animation_timer = 0

    def start_attack(self):
        if self.is_attacking:
            return
        self.is_attacking = True
        self.set_animation('attack')

    def update(self, dt) -> None:
        keys = pygame.key.get_pressed()

        moving_right = False
        moving_left = False

        if not self.is_attacking:

            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed * dt
                moving_right = False
                moving_left = True

            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed * dt
                moving_right = True
                moving_left = False

            if moving_right:
                self.set_animation('walk_right')
            elif moving_left:
                self.set_animation('walk_left')
            else:
                self.set_animation('idle')

        self.animation_timer += dt

        animation = self.animations[self.current_animation]

        frames = animation['frames']
        loop = animation['loop']

        if self.animation_timer > 0.2:
            self.frame_index += 1
            self.animation_timer = 0

        if self.frame_index >= len(frames):
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(frames) - 1
                if self.current_animation == 'attack':
                    self.is_attacking = False
                    self.set_animation('idle')

        self.image = frames[self.frame_index]


player = PlayerSprite(animations)
player_group = pygame.sprite.Group()
player_group.add(player)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.start_attack()

    dt = clock.tick(60) / 1000

    screen.fill('white')

    player_group.update(dt)
    player_group.draw(screen)

    pygame.display.flip()
