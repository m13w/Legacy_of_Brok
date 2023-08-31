import math, pygame

pygame.init()

# === CONSTANTS ===

#window dimensions set into the name 'win'
win = pygame.display.set_mode((1280,800))

#cursor / player ship image
cursor = pygame.image.load("images/cursor.png").convert_alpha()


# === CLASSES ===

#bullet class, holds image and other points
class projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.image = pygame.transform.smoothscale(pygame.image.load('images/bullet.png'), (30,60))
        self.vel = 3

    #gets called in the update_win() to draw the bullet on the screen
    def draw(self,win):
        win.blit(self.image, (self.x,self.y))



# === MAIN FUNCTIONS ===


#keeps the display.update() and other blit code for easier layout
def update_win():

    win.fill((31,27,24))

    for bullet in bullets:
        bullet.draw(win)

    win.blit(rot_image, rot_image_rect.topleft)
    
    pygame.display.update()



#   0 - image is looking to the right
#  90 - image is looking up
# 180 - image is looking to the left
# 270 - image is looking down
correction_angle = 90

cursor_pos = list(win.get_rect().center)

#this is where the bullets go into a list
bullets = []
#for control of how many bullets are fired and at what interval
shoot_loop = 0


# === MAIN LOOP ===

run = True
while run:
    pygame.time.delay(2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    
    #cursor postion and rectangle
    cursor_rect = cursor.get_rect(center = (cursor_pos))
    




    #simple movement / key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and cursor_rect.x > -10:
        cursor_pos[0] -= 1
    if keys[pygame.K_d] and cursor_rect.x < 1210:
        cursor_pos[0] += 1
    if keys[pygame.K_w] and cursor_rect.y > -10:
        cursor_pos[1] -= 1
    if keys[pygame.K_s] and cursor_rect.y < 730:
        cursor_pos[1] += 1
    if keys[pygame.K_SPACE]:
        x,y = pygame.mouse.get_pos()
        print(x,y)




    #controls how many bullets are shot (interval)
    if shoot_loop > 0:
        shoot_loop += 0.06
    if shoot_loop > 3:
        shoot_loop = 0


    #will move the bullet image in list and .pop it if it goes above screen
    for bullet in bullets:
        if bullet.y < 800 and bullet.y > -10:
            bullet.y -= bullet.vel  # Moves the bullet by its vel (3)
        else:
            bullets.pop(bullets.index(bullet))  # This will remove the bullet if it is off the screen


    #checks the bullet loop and will add another bullet to the loop if conditions are met
    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if len(bullets) < 100:
            bullets.append(projectile(round(cursor_rect.x + 25), round(cursor_rect.y ), 6, (255,255,255)))

        shoot_loop = 1
        



    







    #calculates mouse position, angle and rotation for image
    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - cursor_rect.centerx, my - cursor_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    #rotated image surface
    rot_image      = pygame.transform.rotate(cursor, angle)
    rot_image_rect = rot_image.get_rect(center = cursor_rect.center)





    update_win()


pygame.quit()
exit()