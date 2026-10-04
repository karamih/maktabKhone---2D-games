import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500), flags=pygame.RESIZABLE)
pygame.display.set_caption('First Game')
font = pygame.font.Font(None, 64)

clock = pygame.time.Clock()

player_pos = pygame.Vector2(200, 200)
enemy_pos = pygame.Vector2(300, 400)

player_radius = 10
enemy_radius = 20

enemy_color = 'blue'

speed = 300
enemy_speed = 200

running = True
is_game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if is_game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_pos = pygame.Vector2(400, 200)
                    enemy_pos = pygame.Vector2(200, 200)
                    is_game_over = False

    if not is_game_over:
        dt = clock.tick(60) / 1000

        screen.fill('white')

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            player_pos.x += dt * speed
        if keys[pygame.K_LEFT]:
            player_pos.x -= dt * speed
        if keys[pygame.K_UP]:
            player_pos.y -= dt * speed
        if keys[pygame.K_DOWN]:
            player_pos.y += dt * speed

        distance_vector = player_pos - enemy_pos
        if 0 < distance_vector.length() < 150:
            enemy_color = 'red'
            direction = distance_vector.normalize()
            enemy_pos += direction * enemy_speed * dt
            if distance_vector.length() < player_radius + enemy_radius:
                game_over_text = font.render('Game Over', True, 'black')
                game_over_rect = game_over_text.get_rect(
                    center=screen.get_rect().center
                )
                screen.blit(game_over_text, game_over_rect)
                is_game_over = True
        else:
            enemy_color = 'blue'

        pygame.draw.circle(screen, 'black', player_pos, player_radius)
        pygame.draw.circle(screen, enemy_color, enemy_pos, enemy_radius)

        pygame.display.flip()

pygame.quit()
