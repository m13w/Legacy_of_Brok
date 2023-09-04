import pygame
import random
import math
from load import gun_image, gun_image_rev, projectile_image,drop_image, enemy_images, player_image
from user_settings import ENEMY_COL_RADIUS, PLAYER_COL_RADIUS, BULLET_SPEED, ENEMY_SPAWN_RATE

enemies = []
active_items = []

class Explosion:
    def __init__(self, image, position, duration):
        self.image = image
        self.rect = image.get_rect(center= position)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start_time >= self.duration

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
    def __init__(self, position, xp_bar):
        self.image = player_image
        self.rect = self.image.get_rect(center=position)
        self.radius = PLAYER_COL_RADIUS
        self.gun_image = gun_image
        self.gun_rect = self.gun_image.get_rect()
        self.gun_offset = pygame.Vector2(30, 30) # player-gun relative position.
        self.gun_angle = 0
        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_delay = 0.35
        self.gun_direction = pygame.Vector2(1, 0)
        self.xp = 0
        self.level = 1
        self.window_bounds = pygame.display.get_surface().get_rect()
        self.xp_bar = xp_bar


    def shoot(self, mouse_pos):
        if self.shoot_cooldown <= 0:
            direction = pygame.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
            firing_point = self.gun_rect.center 
            bullet_velocity = direction.normalize() * BULLET_SPEED
            bullet = Bullet(projectile_image, firing_point, bullet_velocity, self.gun_angle)
            self.projectiles.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update(self, dt, keys, mouse_pos):
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
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        self.check_item_collision()
        
    def check_item_collision(self):
        for item in active_items[:]:
            if self.rect.colliderect(item.rect):
                active_items.remove(item)
                self.xp += 1
                self.xp_bar.update(1)  # Increment the XP bar by 1 for each collected crystal
                if self.xp_bar.current_xp == self.xp_bar.max_xp:
                    self.xp_bar.current_xp = 0
                    self.xp_bar.max_xp += 5
                    self.level += 1
                print("xp:", self.xp)  # debug console visual
                print("level: ", self.level) #debug console visual

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rotated_gun = pygame.transform.rotate(self.gun_image, -self.gun_angle)
        
        if self.gun_angle > 90 or self.gun_angle < -90:
            self.gun_image = gun_image_rev
        else:
            self.gun_image = gun_image

        rotated_rect = rotated_gun.get_rect(center=self.gun_rect.center)
        screen.blit(rotated_gun, rotated_rect.topleft)

class Enemy:

    enemies = []
    active_explosions = []
    
    def __init__(self, image, spawn_point):
        self.image = image
        self.rect = image.get_rect(center=spawn_point)
        self.radius = ENEMY_COL_RADIUS
        self.speed = 100

    @classmethod
    def spawn_random_enemy(cls, screen_width, screen_height):
        if random.random() < ENEMY_SPAWN_RATE:
            spawn_edge = random.choice(["top", "bottom", "left", "right"])
            if spawn_edge == "top":
                spawn_point = pygame.Vector2(random.uniform(0, screen_width), 0)
            elif spawn_edge == "bottom":
                spawn_point = pygame.Vector2(random.uniform(0, screen_width), screen_height)
            elif spawn_edge == "left":
                spawn_point = pygame.Vector2(0, random.uniform(0, screen_height))
            else:
                spawn_point = pygame.Vector2(screen_width, random.uniform(0, screen_height))

            enemy_image = random.choice(enemy_images)
            enemy = cls(enemy_image, spawn_point)
            cls.enemies.append(enemy)        

    def update(self, dt, player):
        direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        distance = direction.length()

        if distance > 0:
            direction.normalize_ip()
            self.rect.move_ip(direction * self.speed * dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, player):
        distance = pygame.math.Vector2(player.rect.center).distance_to(self.rect.center)
        return distance < player.radius + self.radius
        
    def kill(self):
        crytal = Crystal(drop_image, self.rect.center)
        active_items.append(crytal)

        if self in enemies:
            enemies.remove(self)    

    def drop_crystal(self):
        crystal = Crystal(self.drop_crystal, self.rect.center)
        active_items.append(crystal)

class XPBar:
    def __init__(self, max_xp):
        self.max_xp = max_xp
        self.current_xp = 0
        self.bar_color = (12, 93, 130)  # bar color
        self.bar_color2 = (24,159,192)  # fill color
        self.bar_rect = pygame.Rect(10, 10, 200, 20)  # Adjust the position and size as needed

    def update(self, collected_xp):
        # Update the XP bar based on collected XP
        self.current_xp = min(self.max_xp, self.current_xp + collected_xp)

    def draw(self, screen):
        # Draw the XP bar on the screen
        pygame.draw.rect(screen, self.bar_color, self.bar_rect)
        fill_width = (self.current_xp / self.max_xp) * self.bar_rect.width
        fill_rect = pygame.Rect(self.bar_rect.left, self.bar_rect.top, fill_width, self.bar_rect.height)
        pygame.draw.rect(screen, self.bar_color2, fill_rect)

class HPBar:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.bar_color = (255, 0, 0)  # Red bar for HP
        self.bar_rect = pygame.Rect(10, 40, 200, 20)  # Adjust position and size as needed

    def update(self, damage):
        # Update the HP bar based on damage taken
        self.current_hp = max(0, self.current_hp - damage)

    def draw(self, screen):
        # Draw the HP bar on the screen
        pygame.draw.rect(screen, self.bar_color, self.bar_rect)
        fill_width = (self.current_hp / self.max_hp) * self.bar_rect.width
        fill_rect = pygame.Rect(self.bar_rect.left, self.bar_rect.top, fill_width, self.bar_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)  # Green fill for HP