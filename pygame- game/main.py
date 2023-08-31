import pygame
import math
import pygame.mask
import random
from load import background_image, player_image, enemy_images, reset_image, gun_image, projectile_image, drop_image
import sys
""" un brotato cu mecanici de upgrade de chicken invaders """

PLAYER_COL_RADIUS = 40
ENEMY_COL_RADIUS = 40
enemies = []
active_items = []

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

class Crystal:
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bullet:
    def __init__(self, image, position, velocity, angle):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.velocity = velocity
        self.angle = angle

    def update(self, dt):
        self.rect.move_ip(self.velocity * dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Player:
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.radius = PLAYER_COL_RADIUS
        self.gun_image = gun_image
        self.gun_rect = self.gun_image.get_rect()
        self.gun_offset = pygame.Vector2(60, 10) #se refera la pozitia relativa fata de player
        self.gun_angle = 0
        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_delay = 0.2
        self.gun_direction = pygame.Vector2(1, 0)
        self.collected_items = []
        self.level = 0

    def shoot(self, mouse_pos):
        if self.shoot_cooldown <= 0:
            # Calculate direction and angle
            direction = pygame.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
            angle = math.atan2(direction.y, direction.x)

            # Calculate the firing point relative to the player's position
            firing_point = self.gun_rect.center 

            # Calculate the bullet's velocity
            bullet_velocity = direction.normalize() * 650  # Adjust the bullet speed as needed

            # Create and append the bullet with the current gun angle
            bullet = Bullet(projectile_image, firing_point, bullet_velocity, self.gun_angle)
            self.projectiles.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update(self, dt, keys, mouse_pos):
        #player movement
        if keys[pygame.K_w]:
            self.rect.y -= 300 * dt
        if keys[pygame.K_s]:
            self.rect.y += 300 * dt
        if keys[pygame.K_a]:
            self.rect.x -= 300 * dt
        if keys[pygame.K_d]:
            self.rect.x += 300 * dt

        self.gun_rect.center = self.rect.center + self.gun_offset
        angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        self.gun_angle = math.degrees(angle)

        self.gun_direction = pygame.Vector2(math.cos(angle), math.sin(angle))

        self.shoot(mouse_pos)
        
        # Reduce the shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        self.check_item_collision()
        

    def check_item_collision(self):
        for item in active_items[:]:
            if self.rect.colliderect(item.rect):
                self.collected_items.append(item)
                active_items.remove(item)
                self.level += 1  # Increase level or experience points
                print(self.level)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rotated_gun = pygame.transform.rotate(self.gun_image, -self.gun_angle)  # Rotate gun image

        if self.gun_angle > 90 or self.gun_angle < -90:
            rotated_gun = pygame.transform.flip(rotated_gun, flip_x=False,flip_y=True)
        
        item_spacing = 30  # Adjust the spacing between items
        for i, item in enumerate(self.collected_items):
            item_x = self.rect.centerx + i * item_spacing
            item_y = self.rect.centery
            screen.blit(item.image, (item_x, item_y))

        rotated_rect = rotated_gun.get_rect(center=self.gun_rect.center)
        screen.blit(rotated_gun, rotated_rect.topleft)

class Enemy:
    def __init__(self, image, spawn_point):
        self.image = image
        self.rect = image.get_rect(center=spawn_point)
        self.radius = ENEMY_COL_RADIUS
        self.speed = 100

    def update(self, dt, player):
        direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        distance = direction.length()

        if distance > 0:
            direction.normalize_ip()
            self.rect.move_ip(direction * self.speed * dt)

        # Check for collision between player and enemy
        if self.check_collision(player):
            game_over = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, player):
        # Calculate the distance between the player and the enemy
        distance = pygame.math.Vector2(player.rect.center).distance_to(self.rect.center)

        # Check if the distance is less than the sum of the player and enemy radii
        if distance < player.radius + self.radius:
            return True
        else:
            return False
        
    def kill(self):
        # Generate an item and add it to the list of items
        crytal = Crystal(drop_image, self.rect.center)
        active_items.append(crytal)

        # Remove the enemy from the list of enemies
        if self in enemies:
            enemies.remove(self)    

    def drop_crystal(self):
        crystal = Crystal(self.drop_crystal, self.rect.center)  # Use the crystal image you loaded
        active_items.append(crystal)

player = Player(player_image, (screen.get_width() / 2, screen.get_height() / 2))

enemies = []

def reset_game() -> None:
    global game_over, player_pos, enemies, active_items
    game_over = False
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    enemies = []
    active_items = []  # Reset the list of active items
    player.collected_items = []  # Reset collected items
    player.level = 0  # Reset level



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    if not game_over:
        screen.blit(background_image, (0, 0))

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

        for enemy in enemies[:]:
            enemy.update(dt, player)
            if enemy.check_collision(player):
                game_over = True
                break

        ################################################################################################
        # Spawn enemies from random edges
        if random.random() < 0.04:  # Adjust the spawn rate as needed
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
            enemy.update(dt, player)
        # pygame.draw.circle(screen, (255, 0, 0), player.rect.center, player.radius + 5) # colision viewer circle radius ceva

        for enemy in enemies:
            # pygame.draw.circle(screen, (255, 0, 0), enemy.rect.center, enemy.radius + 5) # colision viewer circle radius ceva
            if enemy.check_collision(player):
                game_over = True

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
