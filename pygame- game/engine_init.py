import pygame
import math
from load import gun_image, gun_image_rev, projectile_image,drop_image
from user_settings import ENEMY_COL_RADIUS, PLAYER_COL_RADIUS, BULLET_SPEED

enemies = []
active_items = []

class Explosion:
    def __init__(self, image, position, duration) -> None:
        self.image = image
        self.rect = image.get_rect(center= position)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

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
        self.gun_offset = pygame.Vector2(30, 30) #se refera la pozitia relativa fata de player
        self.gun_angle = 0
        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_delay = 0.35
        self.gun_direction = pygame.Vector2(1, 0)
        self.level = 0
        self.window_bounds = pygame.display.get_surface().get_rect() # Get window bounds

    def shoot(self, mouse_pos):
        if self.shoot_cooldown <= 0:
            # Calculate direction and angle
            direction = pygame.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
            angle = math.atan2(direction.y, direction.x)

            # Calculate the firing point relative to the player's position
            firing_point = self.gun_rect.center 

            # Calculate the bullet's velocity
            bullet_velocity = direction.normalize() * BULLET_SPEED   # Adjust the bullet speed as needed

            # Create and append the bullet with the current gun angle
            bullet = Bullet(projectile_image, firing_point, bullet_velocity, self.gun_angle)
            self.projectiles.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update(self, dt, keys, mouse_pos):
        #player movement
        if keys[pygame.K_w] and self.rect.top > self.window_bounds.top:
            self.rect.y -= 300 * dt
        if keys[pygame.K_s] and self.rect.bottom < self.window_bounds.bottom:
            self.rect.y += 300 * dt
        if keys[pygame.K_a] and self.rect.left > self.window_bounds.left:
            self.rect.x -= 300 * dt
        if keys[pygame.K_d] and self.rect.right < self.window_bounds.right:
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
                active_items.remove(item)
                self.level += 1  # Increase level or experience points
                print(self.level)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rotated_gun = pygame.transform.rotate(self.gun_image, -self.gun_angle)  # Rotate gun image
        
        if self.gun_angle > 90 or self.gun_angle < -90:
            self.gun_image = gun_image_rev
        else:
            self.gun_image = gun_image
            

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
