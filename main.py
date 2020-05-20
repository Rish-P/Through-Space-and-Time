import pygame
import random
import math
from pygame import mixer

pygame.init()

#creating game window
display_surface=pygame.display.set_mode((800,700))

#adding title and icon to the game window
pygame.display.set_caption("Space Invaders")
mixer.music.load("bg_music.mp3")
mixer.music.play(-1)



#making the UFO player icon
playerimg=pygame.image.load("spaceship2.png") # loading the image into the icon variable
playerx=370      # coordinates of the UFO icon
playery=600
change=0

def player(x,y):
    display_surface.blit(playerimg,(x,y))  #adds a icon to the screen window, at the coordinates mentioned



#ENEMY creating
enemyimg=[]
enemyx=[]
enemyy=[]
echange=[]
echangey=[]
num=5
for i in range(num):
    enemyimg.append(pygame.image.load("monster.png")) # loading the image into the icon variable
    enemyx.append(random.randint(15,750))      # coordinates of the UFO icon
    enemyy.append(random.randint(50,160))
    echange.append(8)
    echangey.append(30)
    def enemy(x,y,i):
        display_surface.blit(enemyimg[i],(x,y))




#bullet creating
bullet_img=pygame.image.load("bullet.png")
bullet_x=0
bullet_y=625
b_change=12
b_state="ready"

def bullet(x,y):
    global b_state
    b_state = "fire"
    display_surface.blit(bullet_img,(x+20,y+10))



#background image
background= pygame.image.load("bg.jpeg")
score=0
#to kill the enemy bot after collision
def iscollide(x1,x2,y1,y2):
    dist=math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
    if dist < 36:
        return True
    else:
        return False

#ADDING THE SCORE
val=0
font=pygame.font.Font("Anhattan.otf",40)
test=True
textX=10
textY=20
def scoreshower(x,y):
    score=font.render("Score : "+ str(val),True,(255,255,255))
    display_surface.blit(score,(x,y))


#WHEN THE GAME IS DONE...
font1=pygame.font.Font("Song of corona.ttf.ttf",150)

x=170
y=300
def done(x,y):
    game_over=font1.render("Game Over",True,(66, 203, 245))
    display_surface.blit(game_over,(x,y))




#GAME loop, VVIMP
while True:
    display_surface.fill((255, 255, 255))
    display_surface.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -5.5
            if event.key == pygame.K_RIGHT:
                change = +5.5
            if event.key == pygame.K_SPACE: # press space to fire a bullet and change to the 'fire' state
                if b_state is "ready":
                    blt=mixer.Sound("Missile+2.wav")
                    blt.play()
                    bullet_x=playerx
                    bullet(bullet_x,bullet_y)

        if event.type == pygame.KEYUP: # once we lift up the key, ufo stops moving
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                change = 0

    playerx+=change
    #so that UFO doesnt venture out of bounds
    if playerx >= 736:
        playerx = 736
    elif playerx <= 0:
        playerx = 0

    
    #compiling the enemy mechanics into a for loop, because there are gonna be multiple enemy bots appearing
    for i in range(num):
        if enemyy[i] > 540:
            for j in range(num):
                enemyy[j]=2000
            done(x,y)
            scoreshower(325,510)
            test=False
            break
        enemyx[i]+=echange[i]
        if enemyx[i] >= 736:
            echange[i] = -4
            enemyy[i]+=echangey[i]
        elif enemyx[i] <= 0:
            echange[i] = 4
            enemyy[i]+=echangey[i]
        collide=iscollide(bullet_x,enemyx[i],bullet_y,enemyy[i])
        if collide: 
            boom=mixer.Sound("Explosion+1.wav")
            boom.play()
            bullet_y=625
            b_state="ready"          #the enemy has been shot down. thus we restart the bullet and increment the score
            val+=1
            enemyx[i]=random.randint(15,750)      # to regenerate an enemy bot at random position immediately after being hit
            enemyy[i]=random.randint(50,160)
        enemy(enemyx[i],enemyy[i],i)

    if bullet_y <=100 :
        bullet_y=600
        b_state="ready"
    if b_state is "fire":
        bullet(bullet_x,bullet_y)
        bullet_y -= b_change
    
    
        
    #adding boundary beyond which enemy bots don't cross
    pygame.draw.line(display_surface,(66, 245, 108),(0,550),(800,550))
    player(playerx,playery)
    if test!=False:
        scoreshower(textX,textY)
    pygame.display.update()
