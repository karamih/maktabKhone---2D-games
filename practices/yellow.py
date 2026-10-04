import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Second Game')

bg_img = pygame.image.load('../assets/parallax-mountain-bg.png')
bg_img_transformed = pygame.transform.smoothscale(bg_img, screen.get_size())

mountain_far_img = pygame.image.load('../assets/parallax-mountain-montain-far.png')
mountain_far_img_transformed = pygame.transform.smoothscale(mountain_far_img, screen.get_size())

mountains_img = pygame.image.load('../assets/parallax-mountain-mountains.png')
mountains_img_transformed = pygame.transform.smoothscale(mountains_img, screen.get_size())

trees_img = pygame.image.load('../assets/parallax-mountain-trees.png')
trees_img_transformed = pygame.transform.smoothscale(trees_img, screen.get_size())

fg_trees_img = pygame.image.load('../assets/parallax-mountain-foreground-trees.png')
fg_trees_img_transformed = pygame.transform.smoothscale(fg_trees_img, screen.get_size())

bird_img = pygame.image.load('../assets/birdd.png')
bird_img_transformed = pygame.transform.smoothscale(bird_img, (64, 64))
bird_rect = bird_img_transformed.get_rect(topleft=(100, 200))

clock = pygame.time.Clock()

running = True
facing_right = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        bird_rect.x += dt * 200
        if not facing_right:
            bird_img_transformed = pygame.transform.flip(
                bird_img_transformed,
                True,
                False
            )
            facing_right = True
    if keys[pygame.K_LEFT]:
        bird_rect.x -= dt * 200
        if facing_right:
            bird_img_transformed = pygame.transform.flip(
                bird_img_transformed,
                True,
                False
            )
            facing_right = False
    if keys[pygame.K_UP]:
        bird_rect.y -= dt * 200
        bird_img_transformed = pygame.transform.rotate(bird_img_transformed, 2)
    if keys[pygame.K_DOWN]:
        bird_rect.y += dt * 200
        bird_img_transformed = pygame.transform.rotate(bird_img_transformed, -2)

    screen.blit(bg_img_transformed, (0, 0))
    screen.blit(mountain_far_img_transformed, (0, 0))
    screen.blit(mountains_img_transformed, (0, 0))
    screen.blit(trees_img_transformed, (0, 0))
    screen.blit(fg_trees_img_transformed, (0, 0))

    screen.blit(bird_img_transformed, bird_rect)

    pygame.display.flip()

pygame.quit()
