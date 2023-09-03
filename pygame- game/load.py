import pygame

# Define the base path to your assets folder
ASSETS_PATH = "Legacy_of_Brok/pygame- game/assets/"

# Load the images
background_image = pygame.image.load(ASSETS_PATH + "background1.jpg")
player_image = pygame.image.load(ASSETS_PATH + "character.png")
enemy_image1 = pygame.image.load(ASSETS_PATH + "enemy.png")
enemy_image2 = pygame.image.load(ASSETS_PATH + "enemy2.png")
enemy_image3 = pygame.image.load(ASSETS_PATH + "enemy3.gif")

# Scale the images
reset_image = pygame.image.load(ASSETS_PATH + "reset.png")
reset_image = pygame.transform.scale(reset_image, (300, 100))

gun_image = pygame.image.load(ASSETS_PATH + "gun.png")
gun_image = pygame.transform.scale(gun_image, (120, 120))

gun_image_rev = pygame.image.load(ASSETS_PATH + "gun-rev.png")
gun_image_rev = pygame.transform.scale(gun_image_rev, (120, 120))

projectile_image = pygame.image.load(ASSETS_PATH + "bullet.png")
projectile_image = pygame.transform.scale(projectile_image, (20, 20))

drop_image = pygame.image.load(ASSETS_PATH + "drop.png")
drop_image = pygame.transform.scale(drop_image, (40, 40))

enemy_images = [
    pygame.transform.scale(enemy_image1, (100, 100)),
    pygame.transform.scale(enemy_image2, (100, 100)),
    pygame.transform.scale(enemy_image3, (100, 100))
]
