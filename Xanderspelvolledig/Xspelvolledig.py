import pygame
import random
import time
import os
import threading
import shelve
#from random import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # dit spawnt het scherm in het midden van je scherm

def xandergame():
    def XStartmenu():
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Flutey_World.mp3")
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.fadeout
        WIDTH = 700
        HEIGHT = 600
        screentut = pygame.display.set_mode((WIDTH, HEIGHT))
        background_imagetwee = pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Xanderspelintroachtergrond.jpg").convert()
        BLACK = (0, 0, 0)

        # Startmenu loop
        end_it = False
        while (end_it == False):
            #screentut.fill(BLACK)
            #myfont = pygame.font.SysFont("Britannic Bold", 40)
            #nlabel = myfont.render("Welcome Start Screen", 1, (255, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_it = True
                elif event.type == pygame.KEYDOWN:
                    print("space")
                    end_it = True
                    # if event.type== pygame.K_SPACE:
                    #    print("space2")
                    #    end_it=True
            screentut.blit(background_imagetwee, [0, 0])
            pygame.display.flip()

    def XGameloop():
        WIDTH = 700
        HEIGHT = 600
        FPS = 60
        # define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        GREEN2 = (0, 155,0)
        BLUE = (0, 0, 255)
        RED2 = (150, 0, 0)
        RED3 = (100, 0, 0)
        RED4 = (30, 0, 0)
        RED5 = (244,54,29)
        TURQOISE = (0,255,255)
        YELLOW = (255,255,0)
        YELLOW2 = (150,150,0)
        RANDOMCOLLOR = (23,175,200)

        # initialize pygame and create window
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SPEL")
        clock = pygame.time.Clock()

        #explosion_anim = {}
        #explosion_anim['lg'] = []
        #explosion_anim['sm'] = []
        #for i in range(9):
        #    filename = "regularExplosion0{}.png".format(i)
        #    img = pygame.image.load(path.join(img_dir, img)).convert()
        #    img.set_colorkey(BLACK)
        #    img_lg = pygame.transform.scale(img, (75,75))
        #    explosion_anim['lg'].append(img_lg)
        #    img_sm = pygame.transform.scale(img, (32,32))
        #    explosion_anim['sm'].append(img_sm)

        font_name = pygame.font.match_font('arial')
        def draw_text(surf, text, size, x, y):
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)

        class music():
            #def playrandomsong(self):
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.queue("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/GasGasGas.mp3")
            randommuziek = random.randrange(0,5)
            if randommuziek == 0:
                pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Run.mp3")
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 1:
                pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Factory.mp3")
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 2:
                pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Radiocutter.mp3")
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 3:
                pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Twilighttechno.mp3")
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 4:
                pygame.mixer.music.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/MUSIC/Gloriousmorning.mp3")
                pygame.mixer.music.play(0)
                print(randommuziek)
            #def stopmusic(self):
            #    pygame.mixer.music.rewind

        #playerimg Xander

        player_image =      pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Xanderspelschipplayergrootmelkzijlen.png").convert_alpha()#.convert()
        bullet_imageleft =  pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Bulletgoingleft.png").convert_alpha()
        bullet_imageright = pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Bulletgoingright.png").convert_alpha()
        bullet_imageup =    pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Bulletgoingup.png").convert_alpha()
        bullet_imagedown =  pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Bulletgoingdown.png").convert_alpha()
        seadrakeleft =      pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seadrakered.png").convert_alpha()
        seadrakeright =     pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seadrakeblue.png").convert_alpha()
        seadrakedown =      pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seadrakeblue2.png").convert_alpha()
        seadrakeup =        pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seadrakered2.png").convert_alpha()
        seakrakenright =    pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seakrakenright.png").convert_alpha()
        seakrakenleft =     pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/seakrakenleft.png").convert_alpha()
        badguyshipright =   pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Slechterikshiprechts.png").convert_alpha()
        badguyshipleft =   pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Slechterikshiplinks.png").convert_alpha()
        morelives   =       pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Morelives.png").convert_alpha()
        moreammo    =       pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Moreammo.png").convert_alpha()
        morescore   =       pygame.image.load("C:/Users/Xander/Desktop/Pirates_of_the_Arrribean/IMG/Morescore.png").convert_alpha()




        #pygame.mouse.set_visible(False)

        class Xanderplayer(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = player_image #pygame.Surface((30,30))
                #self.image.fill(GREEN)
                self.rect = self.image.get_rect()
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
                self.speedx = 0
                self.speedy = 0
            def update(self):
                pos = pygame.mouse.get_pos()    # deze 2 regels
                self.rect.midtop = pos         # laten de speler de muis volgen
                self.speedx = 0
                self.speedy = 0

            def shootup(self):
                bulletup = Playerbulletsup(self.rect.centerx, self.rect.top)
                all_sprites.add(bulletup)
                bulletup.add(bullets)
            def shootdown(self):
                bulletdown = Playerbulletsdown(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bulletdown)
                bulletdown.add(bullets)
            def shootright(self):
                bulletright = Playerbulletsright(self.rect.centerx + 12, self.rect.top + 30)
                all_sprites.add(bulletright)
                bulletright.add(bullets)
            def shootleft(self):
                bulletleft = Playerbulletsleft(self.rect.centerx - 12, self.rect.top + 30)
                all_sprites.add(bulletleft)
                bulletleft.add(bullets)

        #Begin variabelen snelheid monsters ( op volgorde )         dit zijn de prototype values die ik had.
        minumumrspeedyup = int(3.8)                                        #minumumrspeedyup = 3
        maximumrspeedyup = int(5.2)                                        #maximumrspeedyup = 10

        minumumrspeedydown = int(-5.2)                                     #minumumrspeedydown = -10
        maximumrspeedydown = int(-3.8)                                     #maximumrspeedydown = -3

        minumumrspeedxright = int(3.8)                                     #minumumrspeedxright = 3
        maximumrspeedxright = int(5.2)                                     #maximumrspeedxright = 10

        minimumrspeedxleft = int(-5.2)                                     #minimumrspeedxleft = -10
        maximumrspeedxleft = int(-3.8)                                     #maximumrspeedxleft = -3

        #mobs classes

        class Xandermobup(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seadrakeup #pygame.Surface((30,40))
                #self.image.fill(RED)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(minumumrspeedyup, maximumrspeedyup)
                self.speedx = random.randrange(-2, 2)
            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, -40)
                    self.speedy = random.randrange(minumumrspeedyup, maximumrspeedyup)
                    self.speedx = random.randrange(-2, 2)

        class Xandermobdown(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seadrakedown#pygame.Surface((30,40))
                #self.image.fill(TURQOISE)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(WIDTH - self.rect.width) # hiermee spawned het altijd in het scherm
                self.rect.y = random.randrange(700,800) # hiermee spawnen ze onderaan
                self.speedy = random.randrange(minumumrspeedydown,maximumrspeedydown)
                self.speedx = random.randrange(-2, 2)
            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.bottom < -20 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(700, 800)
                    self.speedy = random.randrange(minumumrspeedydown,maximumrspeedydown)
                    self.speedx = random.randrange(-2, 2)

        class Xandermobright(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seadrakeright#pygame.Surface((40,30))
                #self.image.fill(BLUE)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(-30,-5) # hiermee spawned het altijd in het scherm # 1,2 = linkerkant van het scherm 699,700 = rechterkant van het scherm
                self.rect.y = random.randrange(2,598)       #0, 600 y-as spawning op het scherm 1,2 = linksboven
                self.speedy = random.randrange(-2, 2)
                self.speedx = random.randrange(minumumrspeedxright,maximumrspeedxright)         # -x = shit gaat naar links
            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT - 10 or self.rect.left < -25 or self.rect.right > WIDTH + 50:
                    self.rect.x = random.randrange(-10, -5)  # 0, 600 y-as spawning op het scherm 1,2 = linksboven
                    self.rect.y = random.randrange(2, 598)  #hiermee spawnt het weer op een random locatie aan de linkerkant van het scherm
                    self.speedy = random.randrange(-2, 2)
                    self.speedx = random.randrange(minumumrspeedxright,maximumrspeedxright)

        class Xandermobleft(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seadrakeleft#pygame.Surface((40,30))
                #self.image.fill(RED2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(710,730) # hiermee spawned het altijd in het scherm # 1,2 = linkerkant van het scherm 699,700 = rechterkant van het scherm
                self.rect.y = random.randrange(2,598)       #0, 600 y-as spawning op het scherm 1,2 = linksboven
                self.speedy = random.randrange(-2, 2)
                self.speedx = random.randrange(minimumrspeedxleft,maximumrspeedxleft)         # -x = shit gaat naar links
            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT - 10 or self.rect.left < -25: #or self.rect.bottom < HEIGHT + 600: #or self.rect.right > WIDTH + 50:
                    self.rect.x = random.randrange(710,730)  # hiermee spawned het altijd in het scherm # 1,2 = linkerkant van het scherm 699,700 = rechterkant van het scherm
                    self.rect.y = random.randrange(2, 598)  # 0, 600 y-as spawning op het scherm 1,2 = linksboven
                    self.speedy = random.randrange(-2, 2)
                    self.speedx = random.randrange(minimumrspeedxleft,maximumrspeedxleft)


        class XanderBIGSHOOTERmobleft(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = badguyshipright#pygame.Surface((50, 80))
                #self.image.fill(RED2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(710, 720)
                self.rect.y = HEIGHT / 2 - 35
                self.speedx = -1.9#-0.2  # -x = shit gaat naar links

            def update(self):
                self.rect.x += self.speedx
                if self.rect.x <= 650:                                          #660
                    self.speedx = 1.9 #2.1
                    XanderBIGSHOOTERmobleft.shooting(self)
                if self.rect.x >= 690:
                    self.speedx = -1.9#- 2.1
                    XanderBIGSHOOTERmobleft.shooting(self)

            def shooting(self):
                monsterbulletsleft = Monsterbulletsleft(self.rect.centerx - 30, self.rect.top + 35)
                all_sprites.add(monsterbulletsleft)
                #monsterbullets.add(monsterbulletsleft)
                monsterbulletsleft.add(monsterbullets)

        class XanderBIGSHOOTERmobright(pygame.sprite.Sprite):                           # RIGHT en LEft zijn omgedraaid
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = badguyshipleft#pygame.Surface((50, 80))
                #self.image.fill(RED2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(-50,-30)
                self.rect.y = HEIGHT / 2 - 35
                self.speedx = 1.9#0.2  # -x = shit gaat naar links

            def update(self):
                self.rect.x += self.speedx
                if self.rect.x <= -40:  # 660
                    self.speedx = 1.9#2.1
                    XanderBIGSHOOTERmobright.shooting(self)
                if self.rect.x >= 0:
                    self.speedx = -1.9#-2.1
                    XanderBIGSHOOTERmobright.shooting(self)

            def shooting(self):
                monsterbulletsright = Monsterbulletsright(self.rect.centerx + 30, self.rect.top + 35)
                all_sprites.add(monsterbulletsright)
                #monsterbullets.add(monsterbulletsright)
                monsterbulletsright.add(monsterbullets)

        class XanderBIGSHOOTERmobup(pygame.sprite.Sprite):  # RIGHT en LEft zijn omgedraaid
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = badguyshipright#pygame.Surface((80, 50))
                #self.image.fill(RED2)
                self.rect = self.image.get_rect()
                self.rect.y = random.randrange(620,650)          #-730,-710
                self.rect.x = WIDTH / 2 - 35
                self.speedy = -1.9#-0.2  # -x = shit gaat naar links

            def update(self):
                self.rect.y += self.speedy
                if self.rect.y >= 590:  # 6540
                   self.speedy = -1.9#-2.1
                   XanderBIGSHOOTERmobup.shooting(self)
                if self.rect.y <= 550:  #480
                    self.speedy = 1.9#2.1
                    XanderBIGSHOOTERmobup.shooting(self)

            def shooting(self):
                monsterbulletsup = Monsterbulletsup(self.rect.centerx, self.rect.top)
                all_sprites.add(monsterbulletsup)
                #monsterbullets.add(monsterbulletsup)
                monsterbulletsup.add(monsterbullets)

        class XanderBIGSHOOTERmobdown(pygame.sprite.Sprite):  # RIGHT en LEft zijn omgedraaid
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = badguyshipleft#pygame.Surface((80, 50))
                #self.image.fill(RED2)
                self.rect = self.image.get_rect()
                self.rect.y = random.randrange(-60, -50)  # -730,-710
                self.rect.x = WIDTH / 2 - 35
                self.speedy = 1.9#0.2  # -x = shit gaat naar links

            def update(self):
                self.rect.y += self.speedy
                if self.rect.y <= -40:  # 6540
                    self.speedy = 1.9#2.1
                    XanderBIGSHOOTERmobdown.shooting(self)
                if self.rect.y >= 0:  # 480
                    self.speedy = -1.9#-2.1
                    XanderBIGSHOOTERmobdown.shooting(self)

            def shooting(self):
                monsterbulletsdown = Monsterbulletsdown(self.rect.centerx, self.rect.bottom)
                all_sprites.add(monsterbulletsdown)
                #monsterbullets.add(monsterbulletsdown)
                monsterbulletsdown.add(monsterbullets)

        class Bouncyballmobleft (pygame.sprite.Sprite):                 #Zal ik dit toevoegen?
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seakrakenleft#pygame.Surface((50, 50))
                #self.image.fill(RED5)
                self.rect = self.image.get_rect()
                self.rect.x = -20#random.randrange(-60, -50)  # -730,-710
                self.rect.y = random.randrange(100,500)#300#WIDTH / 2 - 200
                self.speedx = 5#7  # -x = shit gaat naar links
                self.speedy = 2

            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.x >= 700: #and self.rect.y == 300:
                    self.speedx = random.randrange(-6,-3)              #-5#7
                    self.speedy = random.randrange(-3,-1)              #-2
                elif self.rect.x >= 700:
                    self.speedx = random.randrange(-6,-3)               #-5#7
                if self.rect.x <= 0:
                    self.speedx = random.randrange(3,6)              #5#7
                if self.rect.y <= 0:
                    self.speedy = random.randrange(3,6)               #5#7
                if self.rect.y >= 600:
                    self.speedy = random.randrange(-6,-3)              #-5#7

        class Bouncyballmobright(pygame.sprite.Sprite):  # Zal ik dit toevoegen?
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seakrakenright#pygame.Surface((50, 50))
                #self.image.fill(RED5)
                self.rect = self.image.get_rect()
                self.rect.x = 720  # random.randrange(-60, -50)  # -730,-710
                self.rect.y = random.randrange(100, 500)  # 300#WIDTH / 2 - 200
                self.speedx = -5  # 7  # -x = shit gaat naar links
                self.speedy = -2

            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.x >= 700:  # and self.rect.y == 300:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                    self.speedy = random.randrange(-3, -1)  # -2
                elif self.rect.x >= 700:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                if self.rect.x <= 0:
                    self.speedx = random.randrange(3, 6)  # 5#7
                if self.rect.y <= 0:
                    self.speedy = random.randrange(3, 6)  # 5#7
                if self.rect.y >= 600:
                    self.speedy = random.randrange(-6, -3)  # -5#7

        class Bouncyballmobup(pygame.sprite.Sprite):  # Zal ik dit toevoegen?
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seakrakenleft#pygame.Surface((50, 50))
                #self.image.fill(RED5)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(100, 500)  # -730,-710
                self.rect.y = -10  # 300#WIDTH / 2 - 200
                self.speedx = -2  # 7  # -x = shit gaat naar links
                self.speedy = -5

            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.x >= 700:  # and self.rect.y == 300:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                    self.speedy = random.randrange(-3, -1)  # -2
                elif self.rect.x >= 700:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                if self.rect.x <= 0:
                    self.speedx = random.randrange(3, 6)  # 5#7
                if self.rect.y <= 0:
                    self.speedy = random.randrange(3, 6)  # 5#7
                if self.rect.y >= 600:
                    self.speedy = random.randrange(-6, -3)  # -5#7

        class Bouncyballmobdown(pygame.sprite.Sprite):  # Zal ik dit toevoegen?
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = seakrakenright#pygame.Surface((50, 50))
                #self.image.fill(RED5)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(100, 500)  # -730,-710
                self.rect.y = 610  # 300#WIDTH / 2 - 200
                self.speedx = 2  # 7  # -x = shit gaat naar links
                self.speedy = 5

            def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.x >= 700:  # and self.rect.y == 300:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                    self.speedy = random.randrange(-3, -1)  # -2
                elif self.rect.x >= 700:
                    self.speedx = random.randrange(-6, -3)  # -5#7
                if self.rect.x <= 0:
                    self.speedx = random.randrange(3, 6)  # 5#7
                if self.rect.y <= 0:
                    self.speedy = random.randrange(3, 6)  # 5#7
                if self.rect.y >= 600:
                    self.speedy = random.randrange(-6, -3)  # -5#7


        #
        #                 #monsterkogel = random.randrange(1, 30)
        #                 #if monsterkogel <= 3:
        #                 #    monsterbulletleft = Monsterbulletsleft(self.rect.centerx - 30, self.rect.top + 35)
        #                 #    all_sprites.add(monsterbulletleft)
        #                 #    monsterbullets.add(monsterbulletleft)


        #bullet classes

        #player bullet classes
        class Playerbulletsup(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageup#pygame.Surface((10,20))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10                               # kogelsnelheid en righting
            def update(self):
                self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()

        class Playerbulletsdown(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imagedown#pygame.Surface((10,20))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.centerx = x
                self.speedy = 10                               # kogelsnelheid en righting
            def update(self):
                self.rect.y += self.speedy
                if self.rect.top > 600:
                    self.kill()

        class Playerbulletsright(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageright#pygame.Surface((20,10))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.centerx = x
                self.speedx = 10                               # kogelsnelheid en righting
            def update(self):
                self.rect.x += self.speedx
                if self.rect.right > 710:
                    self.kill()

        class Playerbulletsleft(pygame.sprite.Sprite):
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageleft#pygame.Surface((20,10))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.centerx = x
                self.speedx = -10                               # kogelsnelheid en righting
            def update(self):
                self.rect.x += self.speedx
                if self.rect.right < -10:
                    self.kill()

        #monster bullet classes
        class Monsterbulletsleft(pygame.sprite.Sprite):                                 #BIGMOBLEFT
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageleft#pygame.Surface((20,10))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.centerx = x
                self.speedx = -4                               # kogelsnelheid en righting
            def update(self):
                self.rect.x += self.speedx
                if self.rect.right < -4:
                    self.kill()

        class Monsterbulletsright(pygame.sprite.Sprite):  # BIGMOBRRIGHT
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageright#pygame.Surface((20, 10))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.centerx = x
                self.speedx = 4  # kogelsnelheid en righting

            def update(self):
                self.rect.x += self.speedx
                if self.rect.left > 705:
                    self.kill()

        class Monsterbulletsup(pygame.sprite.Sprite):  # BIGMOBRUP
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imageup #pygame.Surface((10, 20))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -4  # kogelsnelheid en righting

            def update(self):
                self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()

        class Monsterbulletsdown(pygame.sprite.Sprite):  # BIGMOBRdown
            def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_imagedown#pygame.Surface((10, 20))
                #self.image.fill(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = 4  # kogelsnelheid en righting

            def update(self):
                self.rect.y += self.speedy
                if self.rect.top > 630:
                    self.kill()


        #powerup classes

        class Powerupmorebullets(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = moreammo#pygame.Surface((30,30))
                #self.image.fill(YELLOW)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(1,690)
                self.rect.y = random.randrange(2,590)

        class Invinsible(pygame.sprite.Sprite):                 #deze doet het nog niet
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((40, 40))
                self.image.fill(YELLOW2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(2, 690)
                self.rect.y = random.randrange(2, 590)

        class Powerupextraleven(pygame.sprite.Sprite):                 #deze doet het nog niet
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = morelives#pygame.Surface((30,30))
                #self.image.fill(YELLOW2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(2, 690)
                self.rect.y = random.randrange(2, 590)

        class Powerupbonusscoreleft(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = morescore#pygame.Surface((50,50))
                #self.image.fill(GREEN2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(710,730)
                self.rect.y = random.randrange(8,590)
                #self.speedy = random.randrange(-2, 2)          hij hoeft niet naar boven of naar beneden
                self.speedx = -5                                # om mee te testen
            def update(self):
                self.rect.x += self.speedx
                #self.rect.y += self.speedy
                if self.rect.right < -10:
                    self.kill()

        class Powerupbonusscoreright(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = morescore#pygame.Surface((50,50))
                #self.image.fill(GREEN2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(-30,-5)
                self.rect.y = random.randrange(2,598)
                #self.speedy = random.randrange(-2, 2)          hij hoeft niet naar boven of naar beneden
                self.speedx = 5                                # om mee te testen
            def update(self):
                self.rect.x += self.speedx
                #self.rect.y += self.speedy
                if self.rect.right > 710:
                    self.kill()

        class Powerupbonusscoreup(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = morescore#pygame.Surface((50,50))
                #self.image.fill(GREEN2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                #self.speedy = random.randrange(-2, 2)          hij hoeft niet naar boven of naar beneden
                self.speedy = 5                                # om mee te testen
            def update(self):
                self.rect.y += self.speedy
                #self.rect.y += self.speedy
                if self.rect.top > 600:
                    self.kill()

        class Powerupbonusscoredown(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = morescore#pygame.Surface((50,50))
                #self.image.fill(GREEN2)
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(700,800)
                #self.speedy = random.randrange(-2, 2)          hij hoeft niet naar boven of naar beneden
                self.speedy = -5                                # om mee te testen
            def update(self):
                self.rect.y += self.speedy
                #self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()


        all_sprites     = pygame.sprite.Group()
        xandermob       = pygame.sprite.Group()
        bullets         = pygame.sprite.Group()
        monsterbullets  = pygame.sprite.Group()

        all_sprites.add(monsterbullets)
        xanderplayer    = Xanderplayer()
        all_sprites.add(xanderplayer)
        xanderplayertwee = Xanderplayer()
        #all_sprites.add(xanderplayertwee)

        #individual mob groups
        xandermobup     = pygame.sprite.Group()
        xandermobdown   = pygame.sprite.Group()
        xandermobright  = pygame.sprite.Group()
        xandermobleft   = pygame.sprite.Group()

        xandersbigmobleft = pygame.sprite.Group()                                       #BIGMOBLEFT
        xandersbigmobright = pygame.sprite.Group()                                       #BIGMOBRIGHT
        xandersbigmobup    = pygame.sprite.Group()                                      #BIGMOBUP
        xandersbigmobdown  = pygame.sprite.Group()

        bouncyballmobleft   = pygame.sprite.Group()
        bouncyballmobright  = pygame.sprite.Group()
        bouncyballmobup     = pygame.sprite.Group()
        bouncyballmobdown   = pygame.sprite.Group()

        #powerups
        powerup1        = pygame.sprite.Group()
        powerup2        = pygame.sprite.Group()
        powerup3        = pygame.sprite.Group()

        #dit spawned de eerste 4 monsters
        for i in range(1):
            m = Xandermobup()
            all_sprites.add(m)
            xandermob.add(m)
            xandermobup.add(m)#Test

            n = Xandermobdown()
            all_sprites.add(n)
            xandermob.add(n)
            xandermobdown.add(n)#Test

            o = Xandermobright()
            all_sprites.add(o)
            xandermob.add(o)
            xandermobright.add(o)#Test

            p = Xandermobleft()
            all_sprites.add(p)
            xandermob.add(p)
            xandermobleft.add(p)#Test

        eensec = 1
        tiensec = 10
        vijftiensec = 15
        twintigsec = 20
        veertigsec = 40
        achtsec = 8

        randomgetal = random.randrange(20,60)           #
        randomgetaltwee = random.randrange(55,110)       #
        randomgetaldrie = random.randrange(40,80)
        randomgetalvier = random.randrange(35,75)
        randomgetalvierrichtingen = random.randrange(1,5)
        randomgetalvijf = random.randrange(30,80)                                            #BIGMOBLINKS
        randomgetalbounce = random.randrange(5,20)                                         #BOUNCE

        aapa = randomgetal
        aapb = randomgetaltwee
        aapc = randomgetaldrie
        aapd = randomgetalvierrichtingen
        aape = randomgetalvijf                                                              #BIGMOBLINKS
        aapf = randomgetalvier

        aapbounce = randomgetalbounce

        variabelea = aapa
        variabeleb = aapb
        variabelec = aapc
        variabeled = aapd
        variabelee = aape                                                                   #BIGMOBLINKS

        variabelebounce = aapbounce

        bigmoblivesup = 8
        bigmoblivesdown = 8
        bigmoblivesright = 8
        bigmoblivesleft = 8

        bouncyballmoblivesleft = 4
        bouncyballmoblivesright = 4
        bouncyballmoblivesup = 4
        bouncyballmoblivesdown = 4
        BMsec = aapf
        BMshooting = BMsec + 3
        start_ticks=pygame.time.get_ticks()
        score = 0
        mobster = 0
        xanderplayerlives = 3
        anotherlife = 50
        kogels = 10
        ait = False
        #mortal = True
        #immortalseconds =




        #pygame.mixer.music.load("C:/Users/Xander/AppData/Local/Programs/Python/Python36-32/Scripts/Run")
        #pygame.mixer.music.play(0)

        background_image = pygame.image.load("C:/Users/Xander/AppData/Local/Programs/Python/Python36-32/Scripts/Seaofdreadfinalbackgroundsmall2.jpg").convert()


        pygame.mouse.set_visible(False)

        # Gameloop Begint hieronder
        running = True

        while running:
            # keep loop running at the right speed
            clock.tick(FPS)
            #seconden timer
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            #if seconds == eensec:
            music        #    music.playrandomsong(music)                                                                       # dit draait de muziek
            #    print("musicshouldbeplaying")
            if seconds > eensec:
                eensec = eensec + 1
                score += 1
            if seconds > vijftiensec:
                vijftiensec = vijftiensec + 15
                minumumrspeedyup    =   minumumrspeedyup    +   int(0.25)                # dat int is voor comma getallen
                minumumrspeedydown  =   minumumrspeedydown  -   int(0.9)                # dit verhoogd de min en max snelheid van de mobs elke zoveel minuten
                minumumrspeedxright =   minumumrspeedxright +   int(0.25)
                minimumrspeedxleft  =   minimumrspeedxleft  -   int(0.9)

                maximumrspeedyup    =   maximumrspeedyup    +   int(0.9)
                maximumrspeedydown  =   maximumrspeedydown  -   int(0.25)
                maximumrspeedxright =   maximumrspeedxright +   int(0.9)
                maximumrspeedxleft  =   maximumrspeedxleft  -   int(0.25)



            if seconds > tiensec:
                tiensec = tiensec + 10
                m = Xandermobup()
                n = Xandermobdown()
                o = Xandermobright()
                p = Xandermobleft()

                if mobster == 0:
                    all_sprites.add(m)
                    xandermob.add(m)
                    xandermobup.add(m)
                    mobster = mobster + 1
                elif mobster == 1:
                    all_sprites.add(n)
                    xandermob.add(n)
                    xandermobdown.add(n)
                    mobster = mobster + 1
                elif mobster == 2:
                    all_sprites.add(o)
                    xandermob.add(o)
                    xandermobright.add(o)
                    mobster = mobster + 1
                elif mobster == 3:
                    all_sprites.add(p)
                    xandermob.add(p)
                    xandermobleft.add(p)
                    mobster = mobster - 3

            if seconds > variabelebounce:
                variabelebounce = variabelebounce + aapbounce + 30
                randomgetalbounce = random.randrange(40, 80)
                aapbounce = randomgetalbounce
                print("loaded")
                if aapd == 1:
                    bml = Bouncyballmobleft()
                    bouncyballmobleft.add(bml)
                    all_sprites.add(bml)
                    print("right")
                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif aapd == 2:
                    bmr = Bouncyballmobright()
                    bouncyballmobright.add(bmr)
                    all_sprites.add(bmr)
                    print("right")
                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif aapd == 3:
                    bmu = Bouncyballmobup()
                    bouncyballmobup.add(bmu)
                    all_sprites.add(bmu)
                    print("up")
                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif aapd == 4 or aapd == 5:
                    bmd = Bouncyballmobdown()
                    bouncyballmobdown.add(bmd)
                    all_sprites.add(bmd)
                    print("down")
                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen


            if seconds > variabelea:
                variabelea = variabelea + aapa + 20
                randomgetal = random.randrange(20, 60)
                aapa = randomgetal

                q = Powerupmorebullets()
                all_sprites.add(q)
                powerup1.add(q)

            if seconds > variabeleb:
                variabeleb = variabeleb + aapb + 40
                randomgetaltwee = random.randrange(55, 110)
                aapb = randomgetaltwee

                r = Powerupextraleven()
                all_sprites.add(r)
                powerup2.add(r)

            if seconds > variabelec:
                variabelec = variabelec + aapc
                randomgetaldrie = random.randrange(40, 60)
                aapc = randomgetaldrie

                if variabeled == 1:
                    saa = Powerupbonusscoreleft()
                    all_sprites.add(saa)
                    powerup3.add(saa)

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif variabeled == 2:
                    sbb = Powerupbonusscoreright()
                    all_sprites.add(sbb)
                    powerup3.add(sbb)

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif variabeled == 3:
                    scc = Powerupbonusscoreup()
                    all_sprites.add(scc)
                    powerup3.add(scc)

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                elif variabeled == 4 or variabeled == 5:
                    sdd = Powerupbonusscoredown()
                    all_sprites.add(sdd)
                    powerup3.add(sdd)

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen

            if seconds > variabelee:                                                        #BIGMOBLEFT
                variabelee = variabelee + aape
                randomgetalvijf = random.randrange(30, 80)
                aape = randomgetalvijf
                if variabeled == 1:                                                     #NOTE TO SELF: je gebruikt hier dezelfde variabele als voor extra punten
                    BMrechts = XanderBIGSHOOTERmobleft()                                #Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                    xandersbigmobleft.add(BMrechts)
                    all_sprites.add(BMrechts)

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                    variabeled = aapd
                elif variabeled == 2:
                    BMlinks = XanderBIGSHOOTERmobright()  # Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                    xandersbigmobright.add(BMlinks)
                    all_sprites.add(BMlinks)
                    print("links")

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                    variabeled = aapd
                elif variabeled == 3:
                    BMup = XanderBIGSHOOTERmobup()  # Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                    xandersbigmobup.add(BMup)
                    all_sprites.add(BMup)
                    print("boven")

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                    variabeled = aapd
                elif variabeled == 4 or variabeled == 5:
                    BMdown = XanderBIGSHOOTERmobdown()
                    xandersbigmobdown.add(BMdown)
                    all_sprites.add(BMdown)
                    print("onder")

                    randomgetalvierrichtingen = random.randrange(1, 5)
                    aapd = randomgetalvierrichtingen
                    variabeled = aapd


            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if kogels > 0:
                        if event.key == pygame.K_UP:
                            xanderplayer.shootup()
                            kogels = kogels - 1
                        if event.key == pygame.K_DOWN:
                            xanderplayer.shootdown()
                            kogels = kogels - 1
                        if event.key == pygame.K_RIGHT:
                            xanderplayer.shootright()
                            kogels = kogels - 1
                        if event.key == pygame.K_LEFT:
                            xanderplayer.shootleft()
                            kogels = kogels - 1

                    if event.key == pygame.K_ESCAPE:
                        running = False
                    #if event.key == pygame.K_p:
                        #print(bigmoblivesdown)
                        #pygame.time.delay(2000)
                    if event.key == pygame.K_SPACE:
                        print(variabelea,variabeleb,variabelec,randomgetalvierrichtingen,BMsec,variabelee,variabelebounce,seconds)
                        print(bouncyballmoblivesdown,bouncyballmoblivesup,bouncyballmoblivesright,bouncyballmoblivesleft)
                    #if event.key == pygame.K_0:
                        #music.randommuziek == 0
                        # BMup = XanderBIGSHOOTERmobup()  # Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                        # xandersbigmobup.add(BMup)
                        # all_sprites.add(BMup)
                        # BMrechts = XanderBIGSHOOTERmobleft()  # Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                        # xandersbigmobleft.add(BMrechts)
                        # all_sprites.add(BMrechts)
                        # BMlinks = XanderBIGSHOOTERmobright()  # Dit kan misschien problemen opleveren als ze op hetzelfde moment spawnen
                        # xandersbigmobright.add(BMlinks)
                        # all_sprites.add(BMlinks)
                        #BMdown = XanderBIGSHOOTERmobdown()
                        #xandersbigmobdown.add(BMdown)
                        #all_sprites.add(BMdown)
                        #bmd = Bouncyballmobdown()
                        #bouncyballmobdown.add(bmd)
                        #all_sprites.add(bmd)
                        #music.stopmusic()

            # Update

            all_sprites.update()
            #controleren of een bullet een mob raakt.
            hits = pygame.sprite.groupcollide(xandermobup, bullets, True,True)
            for hit in hits:
                score = score + 2
                m = Xandermobup()       #,Xandermobup(),Xandermobup(),Xandermobup(),Xandermobup() zo spawn je er meer
                all_sprites.add(m)
                xandermob.add(m)
                xandermobup.add(m)
            hits = pygame.sprite.groupcollide(xandermobdown, bullets, True, True)
            for hit in hits:
                score = score + 2
                n = Xandermobdown()
                all_sprites.add(n)
                xandermob.add(n)
                xandermobdown.add(n)
            hits = pygame.sprite.groupcollide(xandermobright, bullets, True, True)
            for hit in hits:
                score = score + 2
                o = Xandermobright()
                all_sprites.add(o)
                xandermob.add(o)
                xandermobright.add(o)
            hits = pygame.sprite.groupcollide(xandermobleft, bullets, True, True)
            for hit in hits:
                score = score + 2
                p = Xandermobleft()
                all_sprites.add(p)
                xandermob.add(p)
                xandermobleft.add(p)

            #controleren of een bullet een Bonuspuntenpowerup raakt.
            hits = pygame.sprite.groupcollide(powerup3, bullets, True, True)
            for hit in hits:
                score = score + 50

            #controleren of iets de speler raakt.
            hits = pygame.sprite.spritecollide(xanderplayer, powerup1, True)
            if hits:
                kogels = kogels + 20

            hits = pygame.sprite.spritecollide(xanderplayer, powerup2, True)
            if hits:
                xanderplayerlives = xanderplayerlives + 1


            hits = pygame.sprite.spritecollide(xanderplayer, xandermob, True)
            if hits:
                xanderplayerlives = xanderplayerlives - 1

            hits = pygame.sprite.groupcollide(bullets,xandersbigmobdown,True,False)            #hitpoints bigmob down
            for hit in hits:
                bigmoblivesdown = bigmoblivesdown - 1
            if bigmoblivesdown == 0:
                xandersbigmobdown.remove(BMdown)
                all_sprites.remove(BMdown)
                score = score + 25
                bigmoblivesdown = bigmoblivesdown + 8

            hits = pygame.sprite.groupcollide(bullets, xandersbigmobup, True, False)         # hitpoints bigmob up
            for hit in hits:
                bigmoblivesup = bigmoblivesup - 1
            if bigmoblivesup == 0:
                xandersbigmobup.remove(BMup)
                all_sprites.remove(BMup)
                score = score + 25
                bigmoblivesup = bigmoblivesup + 8

            hits = pygame.sprite.groupcollide(bullets, xandersbigmobright, True, False)  # hitpoints bigmob up
            for hit in hits:
                bigmoblivesright = bigmoblivesright - 1
            if bigmoblivesright == 0:
                xandersbigmobright.remove(BMlinks)
                all_sprites.remove(BMlinks)
                score = score + 25
                bigmoblivesright = bigmoblivesright + 8

            hits = pygame.sprite.groupcollide(bullets, xandersbigmobleft, True, False)  # hitpoints bigmob up
            for hit in hits:
                bigmoblivesleft = bigmoblivesleft - 1
            if bigmoblivesleft == 0:
                xandersbigmobleft.remove(BMrechts)
                all_sprites.remove(BMrechts)
                score = score + 25
                bigmoblivesleft = bigmoblivesleft + 8

            hits = pygame.sprite.spritecollide(xanderplayer, monsterbullets, True, False)
            for hit in hits:
                xanderplayerlives = xanderplayerlives - 0.5                     #1 streepje zijn namelijk 2 projectielen

                                                                                #ik kan hier nog wat instoppen waardoor je een extra mob spawned als je er 1 aanraakt,
                                                                                #   maar meh....

            hits = pygame.sprite.groupcollide(bullets,bouncyballmobleft,True,False) #kogels die de bouncymob raken
            for hit in hits:
                bouncyballmoblivesleft = bouncyballmoblivesleft - 1
            if bouncyballmoblivesleft == 0:
                bouncyballmobleft.remove(bml)
                all_sprites.remove(bml)
                score = score + 20
                bouncyballmoblivesleft = 4#bouncyballmoblivesleft + 4


            hits = pygame.sprite.spritecollide(xanderplayer,bouncyballmobleft,True,False)
            for hit in hits:
                xanderplayerlives = xanderplayerlives - 2

            hits = pygame.sprite.groupcollide(bullets, bouncyballmobright, True, False)  # kogels die de bouncymob raken
            for hit in hits:
                bouncyballmoblivesright = bouncyballmoblivesright - 1
            if bouncyballmoblivesright == 0:
                bouncyballmobleft.remove(bmr)
                all_sprites.remove(bmr)
                score = score + 20
                bouncyballmoblivesright = 4#bouncyballmoblivesright + 4

            hits = pygame.sprite.spritecollide(xanderplayer, bouncyballmobright, True, False)
            for hit in hits:
                xanderplayerlives = xanderplayerlives - 2

            hits = pygame.sprite.groupcollide(bullets, bouncyballmobup, True, False)  # kogels die de bouncymob raken
            for hit in hits:
                bouncyballmoblivesup = bouncyballmoblivesup - 1
            if bouncyballmoblivesup == 0:
                bouncyballmobup.remove(bmu)
                all_sprites.remove(bmu)
                score = score + 20
                bouncyballmoblivesup = 4#bouncyballmoblivesup + 4

            hits = pygame.sprite.spritecollide(xanderplayer, bouncyballmobup, True, False)
            for hit in hits:
                xanderplayerlives = xanderplayerlives - 2

            hits = pygame.sprite.groupcollide(bullets, bouncyballmobdown, True, False)  # kogels die de bouncymob raken
            for hit in hits:
                bouncyballmoblivesdown = bouncyballmoblivesdown - 1
            if bouncyballmoblivesdown == 0:
                bouncyballmobdown.remove(bmd)
                all_sprites.remove(bmd)
                score = score + 20
                bouncyballmoblivesdown = 4#bouncyballmoblivesdown + 4

            hits = pygame.sprite.spritecollide(xanderplayer, bouncyballmobdown, True, False)
            for hit in hits:
                xanderplayerlives = xanderplayerlives - 2


            if xanderplayerlives <= 0:
                running = False

            if score >= anotherlife:
                xanderplayerlives = xanderplayerlives + 1
                anotherlife = anotherlife * 2

            # Draw / render
            screen.blit(background_image, [0,0])
            #screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_text(screen, str(score), 18, WIDTH / 2, 10)    # dit tekent de score
            draw_text(screen, str(xanderplayerlives), 18, WIDTH - 10, 10)
            draw_text(screen, str(kogels), 18, WIDTH - 690, 10)
            # *after* drawing everything, flip the display
            pygame.display.flip()

        XEndscreen(score)       #dit stuurt de score door naar Xendscreen, en called XEndscreen ook gelijk al! dus je hoeft m onderaan niet te noemen
        #print("your score is: ")
        #print(score)

    def XEndscreen(text):
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/Xander/AppData/Local/Programs/Python/Python36-32/Scripts/Wahwahwah.mp3")
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.fadeout

        font_name = pygame.font.match_font('arial')

        def draw_text(surf, text, size, x, y):
            BLACK = (0, 0, 0)
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            surf.blit(text_surface, text_rect)

        WIDTH = 700
        HEIGHT = 600
        screentat = pygame.display.set_mode((WIDTH, HEIGHT))
        background_imagetwee = pygame.image.load(
            "C:/Users/Xander/AppData/Local/Programs/Python/Python36-32/Scripts/XanderspelGameover.jpg").convert()
        # Startmenu loop
        end_it = False
        while (end_it == False):
            # screentut.fill(BLACK)
            # myfont = pygame.font.SysFont("Britannic Bold", 40)
            # nlabel = myfont.render("Welcome Start Screen", 1, (255, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_it = True
                elif event.type == pygame.KEYDOWN:
                    print("end")
                    end_it = True
                    # if event.type== pygame.K_SPACE:
                    #    print("space2")
                    #    end_it=True
            screentat.blit(background_imagetwee, [0, 0])
            draw_text(screentat, str(text), 24, WIDTH / 2, 245)
            pygame.display.flip()
        print("your score is")
        print(text)
    XStartmenu()
    XGameloop()
    #XEndscreen('text')

    #print("your score is: ")
    #print(score)
    pygame.quit()

xandergame()