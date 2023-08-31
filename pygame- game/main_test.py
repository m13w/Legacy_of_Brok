import pygame
import math
import pygame.mask
import random
from load import background_image, player_image, enemy_images, reset_image, gun_image, projectile_image
import sys
""" un brotato cu mecanici de upgrade de chicken invaders """



PLAYER_COL_RADIUS = 40
ENEMY_COL_RADIUS = 40
enemies = []

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

class Bullet:
    def __init__(self, image, position, velocity):
        self.image = image
        self.rect = image.get_rect(center=position)
        self.velocity = velocity

    def update(self, dt):
        self.rect.move_ip(self.velocity * dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.image = pygame.transform.smoothscale(pygame.image.load('images/bullet.png'), (30,60))
        self.vel = 3
        
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.x, my - self.y
        len = math.hypot(dx, dy)
        self.dx = dx / len
        self.dy = dy / len

        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.image, angle)

    def move(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel

    def draw(self,win):
        win.blit( self.image, (round(self.x), round(self.y)))

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

    def shoot(self, mouse_pos):
        if self.shoot_cooldown <= 0:
            angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
            bullet_velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * 800  # Adjust the bullet speed as needed
            bullet = Bullet(projectile_image, self.rect.center, bullet_velocity)
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

        if keys[pygame.K_SPACE]:
            self.shoot(mouse_pos)
        
        # Reduce the shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        #shooting logic


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rotated_gun = pygame.transform.rotate(self.gun_image, -self.gun_angle)  # Rotate gun image
        rotated_rect = rotated_gun.get_rect(center=self.gun_rect.center)
        screen.blit(rotated_gun, rotated_rect.topleft)

class Enemy:
    def __init__(self, image, spawn_point):
        self.image = image
        self.rect = image.get_rect(center=spawn_point)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 100
        self.radius = ENEMY_COL_RADIUS

    def update(self, dt, player):
        self.rect.move_ip(self.velocity * dt)

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

player = Player(player_image, (screen.get_width() / 2, screen.get_height() / 2))

enemies = []

def reset_game() -> None:
    global game_over, player_pos, enemies
    game_over = False
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    enemies = []


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

        ################################################################################################
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


        for bullet in player.projectiles:       
            if -10 < bullet.x < 1200 and -10 < bullet.y < 800:
                bullet.move()
            else:
                player.projectiles.pop(player.projectiles.index(bullet))

        # Update enemy positions
        for enemy in enemies:
            enemy.update(dt, player)
        # pygame.draw.circle(screen, (255, 0, 0), player.rect.center, player.radius + 5) # colision viewer circle radius ceva
        
        for bullet in player.projectiles:
            bullet.update(dt)
            bullet.draw(screen)

        for enemy in enemies:
            # pygame.draw.circle(screen, (255, 0, 0), enemy.rect.center, enemy.radius + 5) # colision viewer circle radius ceva
            if enemy.check_collision(player):
                game_over = True

        for enemy in enemies:
            enemy.draw(screen)

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
