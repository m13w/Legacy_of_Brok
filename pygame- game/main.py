"""
Brotato with chicken invaders upgrade mechanics - main file developed by VladIfju and CiprianPopa
"""
import pygame
import random
import sys
from user_settings import WINDOW_WIDTH, WINDOW_HEIGHT
from engine_init import (
    Crystal, 
    Player, 
    Enemy, 
    Explosion, 
    active_items, 
    HPBar,
    XPBar
)
from load import (
    background_image, 
    player_image, 
    reset_image, 
    shot_effect
)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True
game_over = False
pygame.display.set_caption("Legacy of Brok")
pygame.display.set_icon(player_image)
font = pygame.font.Font(None, 64)
max_xp = 10
xp_bar = XPBar(max_xp=max_xp)
dt = 0
start_hp = 100  # Adjust the maximum HP as needed
hp_bar = HPBar(start_hp)
last_damage_time = 0
damage_cooldown = 500 #ms 1k = 1s


reset_button_rect = reset_image.get_rect()
reset_button_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100)

player = Player(
    player_image,
    (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 
    xp_bar=xp_bar
    )

active_explosions = []

def reset_game():
    global game_over, player_pos, enemies, active_items
    game_over = False
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    Enemy.enemies = []
    player.collected_items = []  # Reset collected items
    player.level = 1  # Reset level
    player.xp = 0
    active_items.clear()
    xp_bar.current_xp = 0
    xp_bar.max_xp = 10
    hp_bar.current_hp = 100

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

        # Detect and handle bullet-enemy collisions + explosions
        for bullet in player.projectiles[:]:
            bullet.update(dt)
            for enemy in Enemy.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    player.projectiles.remove(bullet)
                    Enemy.enemies.remove(enemy)
                    enemy.kill()
                    explosion = Explosion(shot_effect, enemy.rect.center, 200) # 200 = ms
                    active_explosions.append(explosion)
                    break   
        for explosion in active_explosions[:]:
            if explosion.update():
                active_explosions.remove(explosion)
            else:
                explosion.draw(screen)

        # Remove bullets and enemies when off-screen
        for bullet in player.projectiles[:]:
            if (bullet.rect.left > screen.get_width() 
                or bullet.rect.right < 0 
                or bullet.rect.top > screen.get_height() 
                or bullet.rect.bottom < 0
            ):
                player.projectiles.remove(bullet)

        #Colision test enemies
        for enemy in Enemy.enemies[:]:
            enemy.update(dt, player)
            if enemy.check_collision(player):
                current_time = pygame.time.get_ticks()
                if current_time - last_damage_time > damage_cooldown:
                    hp_bar.update(10)
                    last_damage_time = current_time
                    if hp_bar.current_hp <= 0:
                        game_over = True
                break
        
        #enemy spawner.
        Enemy.spawn_random_enemy(WINDOW_WIDTH, WINDOW_HEIGHT)

        for bullet in player.projectiles:
            bullet.update(dt)
            rotated_bullet = pygame.transform.rotate(bullet.image, -bullet.angle)  # Rotate bullet image
            rotated_rect = rotated_bullet.get_rect(center=bullet.rect.center)
            screen.blit(rotated_bullet, rotated_rect.topleft)

        firing_point = player.rect.center + player.gun_offset.rotate(-player.gun_angle)

        for enemy in Enemy.enemies:
            enemy.draw(screen)
        
        for item in active_items[:]:
            if isinstance(item, Crystal):
                item.draw(screen)
            item.draw(screen)
        
        xp_bar.draw(screen)
        hp_bar.draw(screen)
        
    else:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(game_over_text, text_rect)
        screen.blit(reset_image, reset_button_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        
        if (
            reset_button_rect.collidepoint(mouse_x, mouse_y) 
            and mouse_clicked[0]
        ):
            reset_game()

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60

pygame.quit()
sys.exit()
