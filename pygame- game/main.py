""" un brotato cu mecanici de upgrade de chicken invaders - main file by VladIfju and CiprianPopa"""
import pygame
import pygame.mask
import random
from engine_init import Crystal, Player, Enemy, active_items
from load import background_image, player_image, enemy_images, reset_image, gun_image, projectile_image, drop_image
import sys

ENEMY_SPAWN_RATE = 0.02

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
game_over = False
dt = 0
pygame.display.set_caption("Legacy of Brok")

# Load your character image
pygame.display.set_icon(player_image)
font = pygame.font.Font(None, 64)

# Resize the character image
player_image = pygame.transform.scale(player_image, (90, 110))

# button for reset UI
reset_button_rect = reset_image.get_rect()
reset_button_rect.center = (screen.get_width() / 2, screen.get_height() / 2 + 100)

player = Player(player_image, (screen.get_width() / 2, screen.get_height() / 2))
enemies = []

def reset_game() -> None:
    global game_over, player_pos, enemies, active_items
    game_over = False
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    enemies = []
    if game_over:
        active_items = []
    player.collected_items = []  # Reset collected items
    player.level = 0  # Reset level
    active_items.clear()


#MAIN GAME LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    if not game_over:
        screen.blit(background_image, (0, 0))  #DRAW BACKGROUND

        keys = pygame.key.get_pressed()
        player.update(dt, keys, mouse_pos=mouse_pos)
        player.draw(screen)


        # Detect and handle bullet-enemy collisions
        for bullet in player.projectiles[:]:
            bullet.update(dt)
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    player.projectiles.remove(bullet)
                    enemies.remove(enemy)
                    enemy.kill()
                    break

        # Remove bullets and enemies when off-screen
        for bullet in player.projectiles[:]:
            if bullet.rect.left > screen.get_width() or bullet.rect.right < 0 or bullet.rect.top > screen.get_height() or bullet.rect.bottom < 0:
                player.projectiles.remove(bullet)

        #Colision test enemies
        for enemy in enemies[:]:
            enemy.update(dt, player)
            if enemy.check_collision(player):
                game_over = True
                break

        # Spawn enemies from random edges
        if random.random() < ENEMY_SPAWN_RATE:  #SPAWN RATE
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

        for bullet in player.projectiles:
            bullet.update(dt)

            rotated_bullet = pygame.transform.rotate(bullet.image, -bullet.angle)  # Rotate bullet image
            rotated_rect = rotated_bullet.get_rect(center=bullet.rect.center)
            screen.blit(rotated_bullet, rotated_rect.topleft)

        firing_point = player.rect.center + player.gun_offset.rotate(-player.gun_angle)

        for enemy in enemies:
            enemy.draw(screen)
        
        for item in active_items[:]:
            if isinstance(item, Crystal):
                item.draw(screen)

            item.draw(screen)
        
    else:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(game_over_text, text_rect)
        screen.blit(reset_image, reset_button_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if reset_button_rect.collidepoint(mouse_x, mouse_y) and mouse_clicked[0]:
            reset_game()

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
sys.exit()
