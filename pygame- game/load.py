import pygame
background_image = pygame.image.load("Legacy_of_Brok/pygame- game/background1.jpg")
player_image = pygame.image.load("Legacy_of_Brok/pygame- game/character.png")
pygame.image.load("Legacy_of_Brok/pygame- game/enemy.png")
pygame.image.load("Legacy_of_Brok/pygame- game/enemy2.png")
pygame.image.load("Legacy_of_Brok/pygame- game/enemy3.gif")

reset_image = pygame.image.load("Legacy_of_Brok/pygame- game/reset.png")
reset_image = pygame.transform.scale(reset_image,(300, 100))

gun_image = pygame.image.load("Legacy_of_Brok/pygame- game/gun.png")
gun_image = pygame.transform.scale(gun_image, (80, 80))

projectile_image = pygame.image.load("Legacy_of_Brok/pygame- game/bullet.png")
projectile_image = pygame.transform.scale(projectile_image, (20,20))

drop_image = pygame.image.load("Legacy_of_Brok/pygame- game/drop.png")
drop_image = pygame.transform.scale(drop_image, (40,40))

enemy_images = [
    pygame.transform.scale(pygame.image.load("Legacy_of_Brok/pygame- game/enemy.png"),(100,100)),
    pygame.transform.scale(pygame.image.load("Legacy_of_Brok/pygame- game/enemy2.png"),(100,100)),
    pygame.transform.scale(pygame.image.load("Legacy_of_Brok/pygame- game/enemy3.gif"),(100,100))
]