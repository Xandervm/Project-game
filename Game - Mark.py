import pygame
import random
import os


pygame.init()

myfont = pygame.font.SysFont("timesnewroman", 20)

#define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

#set resolution
screen = pygame.display.set_mode((950,600))

gameDisplay = pygame.display.set_mode((950,600))
pygame.display.set_caption('Treasure Hunter')

gameExit = False

z = random.randint(1,3)

clock = pygame.time.Clock()

winning_screen = pygame.image.load("Treasure.png")

False_answer = pygame.image.load("wrong.png")

mkPlayer_img = pygame.image.load("mkPlayer.png")

class mkPlayer(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.transform.scale(mkPlayer_img, (40,40))
                self.rect = self.image.get_rect()
                self.rect.center = (400,300)
                self.speedx = 0
                self.speedy = 0

        def update(self):
                self.speedx = 0
                self.speedy = 0
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_LEFT]:
                        self.speedx = -2
                if keystate[pygame.K_RIGHT]:
                        self.speedx = 2
                if keystate[pygame.K_UP]:
                        self.speedy = -2
                if keystate[pygame.K_DOWN]:
                        self.speedy = 2
                if self.rect.right > 800:
                        self.rect.right = 800
                if self.rect.left < 0:
                        self.rect.left = 0
                if self.rect.top < 0:
                        self.rect.top = 0
                if self.rect.bottom > 600:
                        self.rect.bottom = 600

                self.rect.x += self.speedx
                self.rect.y += self.speedy

class Treasure(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((45,45))
                self.image.fill(red)
                self.image.set_colorkey(red)
                self.rect = self.image.get_rect()
                self.rect.center = (140,170)

class TreasureII(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((45,45))
                self.image.fill(red)
                self.image.set_colorkey(red)
                self.rect = self.image.get_rect()
                self.rect.center = (745,292)

class TreasureIII(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((45,45))
                self.image.fill(red)
                self.image.set_colorkey(red)
                self.rect = self.image.get_rect()
                self.rect.center = (208,570)
                
#define sprites
all_sprites = pygame.sprite.Group()
treasures = pygame.sprite.Group()
player = mkPlayer()
Treasure = Treasure()
TreasureII = TreasureII()
TreasureIII = TreasureIII()
all_sprites.add(player)
treasures.add(Treasure, TreasureII, TreasureIII)
#define keystate
keystate = pygame.key.get_pressed()
#mainloop
while not gameExit:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        gameExit = True

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        gameExit = True
                        
        background_image = pygame.image.load("bg - new.jpg")
        screen.blit(background_image, [0,0])
        all_sprites.update()
        all_sprites.draw(screen)

        if z == 1:
                pygame.draw.rect(gameDisplay, black, [140,170,10,10])
                label = myfont.render("Y nbslt uif tqpu", 1, (255,255,0))
                screen.blit(label, (805, 10))
        elif z == 2:
                pygame.draw.rect(gameDisplay, black, [745,292,10,10])
                label = myfont.render("My eye is dark", 1, (255,255,0))
                screen.blit(label, (805, 10))
                label = myfont.render("My mane is", 1, (255,255,0))
                screen.blit(label, (805, 30))
                label = myfont.render("yellow", 1, (255,255,0))
                screen.blit(label, (805, 50))
                label = myfont.render("I am a bit", 1, (255,255,0))
                screen.blit(label, (805, 90))
                label = myfont.render("of a tropical", 1, (255,255,0))
                screen.blit(label, (805, 110))
                label = myfont.render("fellow", 1, (255,255,0))
                screen.blit(label, (805, 130))
        elif z == 3:
                pygame.draw.rect(gameDisplay, black, [208,570,10,10])
                label = myfont.render("255,0,0", 1, (255,255,0))
                screen.blit(label, (805, 10))
                label = myfont.render("220°", 1, (255,255,0))
                screen.blit(label, (805, 30))
        if z == 1:
                if pygame.sprite.collide_rect(player, Treasure) and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(winning_screen, [125,0])
                if pygame.sprite.collide_rect(player, Treasure) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(False_answer, [100,0])
        elif z == 2:
                if pygame.sprite.collide_rect(player, TreasureII) and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(winning_screen, [125,0])
                if pygame.sprite.collide_rect(player, TreasureII) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(False_answer, [100,0])
        elif z == 3:
                if pygame.sprite.collide_rect(player, TreasureIII) and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(winning_screen, [125,0])
                if pygame.sprite.collide_rect(player, TreasureIII) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                        screen.blit(False_answer, [100,0])
                                
        pygame.display.update()
        clock.tick(180)

pygame.quit()
quit()
