import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemies = []

# Spawn an enemy every 2 seconds
enemy_timer = 0
enemy_spawn_time = 2000

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet at the current player position
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Update enemy positions and spawn new ones
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
        enemies.append([enemy_x, enemy_y])
        enemy_timer = current_time

    for enemy in enemies:
        enemy[1] += enemy_speed

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                               (enemy[0], enemy[1], enemy_width, enemy_height)):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Remove enemies that are off the screen
    enemies = [enemy for enemy in enemies if enemy[1] < screen_height]

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player
    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

