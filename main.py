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
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

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
    width = 800
    height = 600
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
                        game = Game(width, height)
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        background = pygame.image.load("back.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
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
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 60))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 250))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 320))


        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Space Invaders")

class Hero:
     def __init__ (self, x, y):
         self.x = x
         self.y = y
    
     def draw(self, game):
         #image = pygame.image.load(heroPicture)
         game.screen.blit(heroPicture, (self.x, self.y))
     
class Game:

     screen = None
     aliens = []
     level = 1
     lives = 5

     def redraw_window(self):
         background = pygame.image.load("backgr.png")
         background = pygame.transform.scale(background, (screen_width, screen_height))
         screen.blit(background, [0, 0])

         #text
         lives_label = text_format(f"Lives: {self.lives}", font, 50, white)
         level_label = text_format(f"Level: {self.level}", font, 50, white)

         screen.blit(lives_label, (10, 10))
         screen.blit(level_label, (650, 10))

         hero = Hero(self.width/2, self.height - 100)

         hero.draw(self)
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

         pygame.display.flip()
         self.clock.tick(60)
         self.screen.fill((0, 0, 0))             

#Initialize the Game
main_menu()
pygame.quit()
quit()
