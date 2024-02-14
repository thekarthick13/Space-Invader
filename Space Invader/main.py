import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))  # (x,y)

# vanity
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("arcade-game.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("bg1.jpg")

# SPACESHIP
playerImg = pygame.image.load("arcade-game.png")
playerX = 370  # hard coded values (aka center)
playerY = 480
playerX_change = 0  # add this value when key is pressed then assign this value to our original value later on

# enemy
# enemyImg = pygame.image.load("alien.png")
#
# enemyX=random.randint (0,736)    #random spawn only doesnt hve anything to do with movement
# enemyY=random.randint (50,150)
# enemyX_change=0.3     #to make it a little faster than our movement
# enemyY_change=40
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

numEnemy = 6

# enemy list
for i in range(numEnemy):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0  # to be chnaged inside while loop so that its pos is synced with spaceship
bulletY = 480  # same as spaceship
bulletX_change = 0
bulletY_change = 0.5  # 0.8
bullet_state = "ready"  # ready means u cant see bullet on screen    'fire' means bullet is currently moving

# score
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 20)   # importing_font
textX = 10
textY = 10

# game over

font2 = pygame.font.Font("freesansbold.ttf", 80)

def game_over(x, y):
    over_text = font2.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (x,y))

def show_score(x,y):
    score = font.render("Score: " + str(score_val), True, (255,255,255))    #render the text first (text, bool, color)
    screen.blit(score, (x,y))
def player(x, y):  # func with arg
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # this how u call global func in python
    screen.blit(bulletImg, (x, y))  # making the bullet appear ....  +16 and +10 makes the bullet appear in the center of the spaceship


# collision formla if distance btw two 2d points is zero ie collision

def isCollision(enemyX, enemyY, bulletX, bulletY):  # boolean function
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))  # sqrt[(x2-x2)^2 + (y2-y1)^2]
    if dist < 35:  # 35 is good enough
        return True
    else:
        return False


running = True
while running:

    screen.fill((61, 61, 41))
    # background comes below screen fill cuz code gets executed one by one thus image will be executed last and is persistent
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # to see if any key has been pressed
            if event.key == pygame.K_LEFT:  # if yes then see if left key has been pressed
                playerX_change = -0.3  # when key is held down add -0.5
            if event.key == pygame.K_RIGHT:  # if yes then see if right key has been pressed
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # otherwise bullet keeps changing direction (buggy) so we want space to work only when one bullet has fired and state becomes ready again
                    bulletX = playerX  # so that the initial pos of the player gets stored and the bullet movement is not affected by the player movement
                    fire_bullet(bulletX, bulletY)  # calling the func initially to set the state

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # stop moving

    # checking for player boundary
    playerX += playerX_change  # displacement

    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:  # account for the size of the png as well (800-32)
        playerX = 768

    # enemy movement
    for i in range(numEnemy):

        enemyX[i] += enemyX_change[i]  # first make it move automatically by adding 0.3 to the left and the code below specifies condition what to do if end is hit

        if enemyX[i] <= -19:
            enemyX_change[i] = 0.3  # bounce back from left wall
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 755:  # account for the size of the png as well (800-32)
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        if enemyY[i] >= 440:              #440 is perfect
            for j in range(numEnemy):
                enemyY[j] = 2000        #without this some enemues still linger after game over. this way every one goes below screen ie making it look like all enemies vanished
                game_over(150,200)

        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # boolean
        if collision:
            bulletY = 480  # if bullet collides, it stops there and comes back to player ie doesnt pass through the enemies
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 736)  # to respawn back in its default spawning location
            enemyY[i] = random.randint(50, 150)
            print(score_val)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)  # now to actually blit the bullet and move the bullet
        bulletY -= bulletY_change  # it will move 2px at a time on a loop till it reaches upper boundary
    # respawning bullet when it goes out of bounds
    if bulletY <= 0:
        bulletY = 480  # when it reaches top bullet position should be reset
        bullet_state = "ready"

    player(playerX, playerY)  # calling the func with arg and giving it the values of already hard coded x and y values
    show_score(textX,textY)
    pygame.display.update()
