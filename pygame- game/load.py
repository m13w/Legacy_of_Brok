import pygame
background_image = pygame.image.load("background1.jpg")
player_image = pygame.image.load("character.png")
pygame.image.load("enemy.png")
pygame.image.load("enemy2.png")
pygame.image.load("enemy3.gif")

reset_image = pygame.image.load("reset.png")
reset_image = pygame.transform.scale(reset_image,(300, 100))

gun_image = pygame.image.load("gun.png")
gun_image = pygame.transform.scale(gun_image, (50, 50))

projectile_image = pygame.image.load("bullet.png")
projectile_image = pygame.transform.scale(projectile_image, (20,20))

drop_image = pygame.image.load("drop.png")
drop_image = pygame.transform.scale(drop_image, (40,40))

enemy_images = [
    pygame.transform.scale(pygame.image.load("enemy.png"),(100,100)),
    pygame.transform.scale(pygame.image.load("enemy2.png"),(100,100)),
    pygame.transform.scale(pygame.image.load("enemy3.gif"),(100,100))
]