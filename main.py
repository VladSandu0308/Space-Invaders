import pygame
import random

import os
# Game Initialization
pygame.init()

# music
pygame.mixer.init()
pygame.mixer.music.load("start.mp3")
pygame.mixer.music.play()

# Game Resolution
menu_width=800
menu_height=600
screen=pygame.display.set_mode((menu_width, menu_height))

game_width=1000
game_height=700

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
yellow=(255, 255, 0)

# Game Fonts
font = "Retro.ttf"

# Game Hero
heroPicture = pygame.image.load("spaceship.png")
heroPicture = pygame.transform.scale(heroPicture, (100, 100))

# Game Framerate
clock = pygame.time.Clock()
FPS=120

# Main Menu
def main_menu():
    width = menu_width
    height = menu_height
    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                        pygame.mixer.music.stop()
                        game = Game(game_width, game_height)
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        background = pygame.image.load("back.jpg")
        background = pygame.transform.scale(background, (menu_width, menu_height))
        screen.blit(background, [0, 0])
        
        title=text_format("Space Invaders", font, 110, yellow)
        if selected=="start":
            text_start=text_format("START", font, 95, white)
        else:
            text_start = text_format("START", font, 95, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 95, white)
        else:
            text_quit = text_format("QUIT", font, 95, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (menu_width/2 - (title_rect[2]/2), 60))
        screen.blit(text_start, (menu_width/2 - (start_rect[2]/2), 250))
        screen.blit(text_quit, (menu_width/2 - (quit_rect[2]/2), 320))


        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Space Invaders")

# Hero (The Ship) class
class Hero:
     def __init__ (self, x, y):
         self.x = x
         self.y = y
    
     def draw(self, game):
         game.screen.blit(heroPicture, (self.x, self.y))
         
     def checkColision(self, laser):
         laserTopY = laser.y
         laserTopX = laser.x
         heroWidth = heroPicture.get_width()
         heroHeight = heroPicture.get_height()

         if laserTopX <= self.x + heroWidth and laserTopX >= self.x - 10:             
             if laserTopY >= self.y and laserTopY <= self.y + heroHeight:
                 return 1
         return 0   

# alien class
class Alien:
    def __init__ (self, x, y, imagePath, canAttack=False):
         self.x = x
         self.y = y
         self.imagePath = imagePath
         alienPicture = pygame.image.load(self.imagePath)
         self.alienPicture = pygame.transform.scale(alienPicture, (50, 50))
         self.canAttack = canAttack
         self.cooldown = 0

    def draw(self, game):
         game.screen.blit(self.alienPicture, (self.x, self.y))
         self.cooldown = max(self.cooldown - 1, 0)


    def moveX(self, alienXDirection, alienYDirection):
         if self.x == 0:
             alienXDirection = "Right"
             alienYDirection = -3

         elif self.x == game_width - 40:
             alienXDirection = "Left"   
             alienYDirection = 3
             
         if alienXDirection == "Left":
             self.x -= 2
         else:
             self.x += 2

         return (alienXDirection, alienYDirection)    

    def moveY(self, alienYDirection):
         self.y += alienYDirection

    def checkColision(self, laser):
         laserTopY = laser.y
         laserTopX = laser.x
         alienWidth = self.alienPicture.get_width()
         alienHeight = self.alienPicture.get_height()

         if laserTopX <= self.x + alienWidth / 2 and laserTopX >= self.x - alienWidth / 2:             
             if laserTopY >= self.y - alienHeight / 2 and laserTopY <= self.y + alienHeight / 2:
                 return 1
         return 0     


#Alien creation (for each level)
# You cand easily add new levels
def alien_creator(level, aliens, dict):
    if (level == 1):
        for i in range(2):
             alien = Alien (300 + 320 * i, 50, "alien1.png", True)
             aliens.append(alien)     

    if (level == 2):
        for i in range(2):
            for j in range(3):
                if i == 1:
                    alien = Alien(120 + 350 * j, 50 + 80 * i , "alien1.png", True)
                else:
                    alien = Alien(120 + 350 * j, 50 + 80 * i , "alien1.png")
                aliens.append(alien)
                if i == 1:
                    dict[alien] = aliens[i * 3 + j - 3]

    if (level == 3):
        for i in range(2):
            for j in range(8):
                path = "alien" + str(i + 1) + ".png"
                if i == 1:
                    alien = Alien(40 + 120 * j, 50 + 80 * i , path, True)
                else:
                    alien = Alien(40 + 120 * j, 50 + 80 * i , path)
                
                aliens.append(alien)
                if i == 1:
                    dict[alien] = aliens[i * 8 + j - 8]

    if (level >= 4):
        for i in range(3):
            for j in range(8):
                path = "alien" + str(i + 1) + ".png"
                if i == 2:
                    alien = Alien(40 + 120 * j, 50 + 80 * i , path, True)
                else:
                    alien = Alien(40 + 120 * j, 50 + 80 * i , path) 
                aliens.append(alien)    
                if i >= 1:
                    dict[alien] = aliens[i * 8 + j - 8]

# base laser class
class Laser:
    def __init__ (self, x, y):
         self.x = x
         self.y = y

    def draw(self, game):
        pass            

    def move(self, tick):
        pass

# Hero laser child 
class HeroLaser(Laser):
    def __init__ (self, x, y):
         super().__init__(x, y)

    def draw(self, game):
         laserPicture = pygame.image.load("laser.png")
         laserPicture = pygame.transform.scale(laserPicture, (50, 50))
         game.screen.blit(laserPicture, (self.x, self.y))  

    def move(self, tick):
         self.y -= 0.3 * tick     

# Enemy laser class
class EnemyLaser(Laser):
    def __init__ (self, x, y):
         super().__init__(x, y)

    def draw(self, game):
         laserPicture = pygame.image.load("alienLaser.png")
         laserPicture = pygame.transform.scale(laserPicture, (35, 35))
         game.screen.blit(laserPicture, (self.x, self.y))  

    def move(self, tick):
         self.y += 0.3 * tick  

class Game:

     screen = None
     level = 1
     levelMax = 5
     lives = 5

     hero = Hero(game_width / 2 - 50, game_height - 100)
     hero_vel = 10
     #defining aliens
     aliens = []
     alien_parents = {}
     alien_creator(level, aliens, alien_parents)
     alienXDirection = "Left"
     alienYDirection = 0
     hero_lasers = []
     enemy_lasers = []
     cooldown = 0
     newLevelCounter = 0
     changedLevel = -1
     doneLevelChange = 0
     background = pygame.image.load("backgr.png")
     background = pygame.transform.scale(background, (1000, 800))

    # redraw funcion (called each frame)
     def redraw_window(self):
         screen.blit(self.background, [0, 0])

         if self.drawDetails:
             lives_label = text_format(f"Lives: {self.lives}", font, 50, white)
             level_label = text_format(f"Level: {self.level}", font, 50, white)

             screen.blit(lives_label, (10, 10))
             screen.blit(level_label, (self.width - 150, 10))
             self.hero.draw(self)
        
         for anAlien in self.aliens:
            anAlien.draw(self)

         for laser in self.hero_lasers:
             laser.draw(self)

         for laser in self.enemy_lasers:
             laser.draw(self)      
        
        # change level           
         if len(self.aliens) == 0 and self.endGame == False:
             # in cazul in care nivelul respectiv nu a fost deja considerat terminat
             if self.doneLevelChange != 1 and self.changedLevel != self.level:
                 if self.level + 1 != self.levelMax:
                    self.newLevelCounter = 200
                 self.doneLevelChange = 1
                 self.changedLevel = self.level

             if self.newLevelCounter != 0:  

                 if self.newLevelCounter % 50 > 19 and self.level + 1 != self.levelMax:
                     end_level = text_format(f"LEVEL {self.level} COMPLETE!", font, 110, (221, 160, 221))
                     self.screen.blit(end_level, (190, 250))
                 self.newLevelCounter -= 1

             if self.newLevelCounter == 0:
                 self.doneLevelChange = 0
                 self.level += 1
                 self.alien_parents = {}
                 alien_creator(self.level, self.aliens, self.alien_parents) 

         #Win
         if self.level == self.levelMax and self.lives != 0:
             self.aliens = []
             self.enemy_lasers = []
             self.hero_lasers = []
             self.endGame = True
             self.drawDetails = False

             self.background = pygame.image.load("wonGame.jpg")
             self.background = pygame.transform.scale(self.background, (1000, 800))
             won_game = text_format("Congratulations! You won!", font, 70, (60, 179, 113))
             self.screen.blit(won_game, (200, 30))
             again_label = text_format("If you want to play again press SPACE", font, 50, (0, 128, 128))
             self.screen.blit(again_label, (190, 100))

             key = pygame.key.get_pressed()
             if key[pygame.K_SPACE]:
                 self.lives = 5
                 self.level = 1
                 self.endGame = False
                 self.drawDetails = True
                 alien_creator(self.level, self.aliens, self.alien_parents)  
                 self.background = pygame.image.load("backgr.png")
                 self.background = pygame.transform.scale(self.background, (1000, 800))   

         #Game Over
         if self.lives == 0:
             self.aliens = []
             self.enemy_lasers = []
             self.endGame = True
             end_level = text_format("GAME OVER!", font, 110, (221, 160, 221))
             self.screen.blit(end_level, (300, 210))
            
             again_label = text_format("If you want to play again press SPACE", font, 50, (176, 224, 230))
             self.screen.blit(again_label, (190, 310))

             key = pygame.key.get_pressed()
             if key[pygame.K_SPACE]:
                 self.lives = 5
                 self.level = 1
                 self.endGame = False
                 alien_creator(self.level, self.aliens, self.alien_parents)  

         pygame.display.update()


     def __init__(self, width, height):
         pygame.init()
         self.width = width
         self.height = height
         self.screen = pygame.display.set_mode((width, height))
         self.clock = pygame.time.Clock()
         done = False
         self.endGame = False
         self.drawDetails = True
        
        # main game loop (for frames)
         while not done:   
             if self.cooldown > 0:
                 self.cooldown -= 1

             tick = self.clock.tick(FPS)
             self.redraw_window()
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                     quit()

             # Moving the aliens
             if self.aliens and self.level > 3:
                 for alien in self.aliens:
                     (self.alienXDirection, self.alienYDirection) = alien.moveX(self.alienXDirection, self.alienYDirection)

                 if self.alienYDirection != 0:
                     for alien in self.aliens:
                         alien.moveY(self.alienYDirection)
                     if self.alienYDirection > 0:
                         self.alienYDirection -= 1
                     elif self.alienYDirection < 0:
                         self.alienYDirection += 1

            # hero lasers         
             for laser in self.hero_lasers:
                 if laser.y < 20:
                     self.hero_lasers.remove(laser)
                 else:
                     laser.move(tick)     
                     for alien in self.aliens:
                         if alien.checkColision(laser) == 1:
                             pygame.mixer.music.load("killedinvader.wav")
                             pygame.mixer.music.play()
                             self.aliens.remove(alien)
                             self.hero_lasers.remove(laser)
                             if alien in self.alien_parents:
                                 for parent in self.aliens:
                                     if self.alien_parents[alien] == parent:
                                         parent.canAttack = True
                                 
             #enemy laser
             for laser in self.enemy_lasers:
                 if laser.y > self.height:
                     self.enemy_lasers.remove(laser)
                 else:
                     laser.move(tick)
                     if self.hero.checkColision(laser) == 1:
                        self.lives -= 1
                        self.enemy_lasers.remove(laser)

            # alien attack AI
             for alien in self.aliens:
                 if alien.canAttack and alien.cooldown == 0:
                     if random.randint(1, 20) == 2:
                         laser = EnemyLaser(alien.x + 8, alien.y + 24)
                         self.enemy_lasers.append(laser)
                         alien.cooldown = 100
            
            # key input
             keys = pygame.key.get_pressed()
             if keys[pygame.K_a] and self.hero.x - self.hero_vel > 0:
                 self.hero.x -= 10
             if keys[pygame.K_LEFT] and self.hero.x - self.hero_vel > 0:
                 self.hero.x -= 10                 
             if keys[pygame.K_d] and self.hero.x - self.hero_vel < game_width - 20:
                 self.hero.x += 10
             if keys[pygame.K_RIGHT] and self.hero.x - self.hero_vel < game_width - 20:
                 self.hero.x += 10
             if keys[pygame.K_w] and self.cooldown == 0:
                 pygame.mixer.music.load("shoot.wav")
                 pygame.mixer.music.play()
                 laser = HeroLaser(self.hero.x + 24, self.hero.y)
                 self.cooldown = 20
                 self.hero_lasers.append(laser)
             if keys[pygame.K_UP] and self.cooldown == 0:
                 pygame.mixer.music.load("shoot.wav")
                 pygame.mixer.music.play()                 
                 laser = HeroLaser(self.hero.x + 24, self.hero.y)
                 self.cooldown = 20
                 self.hero_lasers.append(laser)

         pygame.display.flip()
         self.screen.fill((0, 0, 0))             

#Initialize the Game
main_menu()
pygame.quit()
quit()
