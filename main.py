import pygame

import os
# Game Initialization
pygame.init()

# music
pygame.mixer.init()
pygame.mixer.music.load("start.mp3")
#pygame.mixer.music.play(-1)
# Center the Game Application
#os.environ['SDL_VIDEO_CENTERED'] = '1'

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
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "Retro.ttf"

# Game Hero
heroPicture = pygame.image.load("spaceship.png")
heroPicture = pygame.transform.scale(heroPicture, (100, 100))

# Game Framerate
clock = pygame.time.Clock()
FPS=30

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

class Hero:
     def __init__ (self, x, y):
         self.x = x
         self.y = y
    
     def draw(self, game):
         game.screen.blit(heroPicture, (self.x, self.y))

class Alien:
    def __init__ (self, x, y, imagePath):
         self.x = x
         self.y = y
         self.imagePath = imagePath

    def draw(self, game):
         alienPicture = pygame.image.load(self.imagePath)
         alienPicture = pygame.transform.scale(alienPicture, (50, 50))
         game.screen.blit(alienPicture, (self.x, self.y))          

    def move(self, alien_direction):
         if self.x == 0:
             alien_direction = "Right"

         elif self.x == game_width:
             alien_direction = "Left"   
             
         if alien_direction == "Left":
             self.x -= 20
         else:
             self.x += 20


#Alien creation
def alien_creator(level, aliens):
    if (level == 1):
        for i in range(2):
            for j in range(3):
                alien = Alien(120 + 350 * j, 50 + 80 * i , "alien1.png")
                aliens.append(alien)

    if (level == 2):
        for i in range(2):
            for j in range(8):
                path = "alien" + str(i + 1) + ".png" 
                alien = Alien(40 + 120 * j, 50 + 80 * i , path)
                aliens.append(alien)

    if (level >= 3):
        for i in range(3):
            for j in range(8):
                path = "alien" + str(i + 1) + ".png" 
                alien = Alien(40 + 120 * j, 50 + 80 * i , path)
                aliens.append(alien)                

class Game:

     screen = None
     level = 3
     lives = 5
     hero = Hero(game_width/2 - 50, game_height - 100)
     hero_vel = 10
     #defining aliens
     aliens = []
     alien_creator(level, aliens)
     alien_direction = "Left"

     def redraw_window(self):
         background = pygame.image.load("backgr.png")
         background = pygame.transform.scale(background, (1000, 800))
         screen.blit(background, [0, 0])

         #text
         lives_label = text_format(f"Lives: {self.lives}", font, 50, white)
         level_label = text_format(f"Level: {self.level}", font, 50, white)

         screen.blit(lives_label, (10, 10))
         screen.blit(level_label, (self.width - 150, 10))

         self.hero.draw(self)
         for anAlien in self.aliens:
            anAlien.draw(self)
         pygame.display.update()


     def __init__(self, width, height):
         pygame.init()
         self.width = width
         self.height = height
         self.screen = pygame.display.set_mode((width, height))
         self.clock = pygame.time.Clock()
         done = False

         while not done:
             self.redraw_window()
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     done  = True
             
             if self.aliens:
                 for alien in self.aliens:
                     alien.move(self.alien_direction)       

             keys = pygame.key.get_pressed()
             if keys[pygame.K_a] and self.hero.x - self.hero_vel > 0:
                 self.hero.x -= 10
             if keys[pygame.K_d] and self.hero.x - self.hero_vel < game_width - 20:
                 self.hero.x += 10
             if keys[pygame.K_LEFT] and self.hero.x - self.hero_vel > 0:
                 self.hero.x -= 10
             if keys[pygame.K_RIGHT] and self.hero.x - self.hero_vel < game_width - 20:
                 self.hero.x += 10                    

         pygame.display.flip()
         self.clock.tick(60)
         self.screen.fill((0, 0, 0))             

#Initialize the Game
main_menu()
pygame.quit()
quit()
