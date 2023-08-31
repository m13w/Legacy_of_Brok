import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Load player character image
player_image = pygame.image.load("character.png")
player_rect = player_image.get_rect()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Load enemy images
enemy_images = [
    pygame.image.load("character.png"),
    pygame.image.load("character.png"),
    # Add more enemy images as needed
]

enemies = []

class Enemy:
    def __init__(self, image, spawn_point):
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = spawn_point
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 100

    def update(self, dt):
        self.rect.move_ip(self.velocity * dt)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    # Spawn enemies from random edges
    if random.random() < 0.02:  # Adjust the spawn rate as needed
        spawn_edge = random.choice(["top", "bottom", "left", "right"])
        if spawn_edge == "top":
            spawn_point = pygame.Vector2(random.uniform(0, screen.get_width()), 0)
        elif spawn_edge == "bottom":
            spawn_point = pygame.Vector2(random.uniform(0, screen.get_width()), screen.get_height())
        elif spawn_edge == "left":
            spawn_point = pygame.Vector2(0, random.uniform(0, screen.get_height()))
        else:
            spawn_point = pygame.Vector2(screen.get_width(), random.uniform(0, screen.get_height()))

        enemy_image = random.choice(enemy_images)
        enemy = Enemy(enemy_image, spawn_point)
        enemies.append(enemy)

    # Update enemy positions
    for enemy in enemies:
        enemy.update(dt)

    # Draw enemies on the screen
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    # Blit the player character
    screen.blit(player_image, player_pos - player_rect.center)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
