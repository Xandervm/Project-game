import pygame, sys, os
from pygame.locals import *
from zyclasses import *
from zysettings import *
from alpsprites import *

mus_dir = path.join(path.dirname(__file__), 'mus')

def main_menu():
    WIDTH = 1280
    HEIGHT = 800
    pygame.event.get()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock.tick(FPS)

    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    WIDTH = 480
                    HEIGHT = 600
                    pygame.event.get()
                    pygame.display.set_mode((WIDTH, HEIGHT))
                    g.show_start_screen()
                    while g.running:
                        g.new()
                        g.show_go_screen()
                    main_menu = False
                if event.key == pygame.K_2:
                    zytutorial()
                    main_menu = False
                if event.key == pygame.K_3:
                    mkGame()
                    main_menu = False
                if event.key == pygame.K_4:
                    xandergame()
                    main_menu = False
            

       # pygame.font.init()
       # myfont = pygame.font.SysFont('Arial', 30)
       # headertext = myfont.render('Main Menu', False, (0, 0, 0))
       # maintext = myfont.render('Press 1 to start the game', False, (0, 0, 0))
        screen.blit(mainmenu_img, mainmenu_rect)
       # screen.blit(headertext, (180, 0))
       # screen.blit(maintext, (180, 200))
        pygame.display.flip()

def start_screen():
    WIDTH = 1280
    HEIGHT = 800
    pygame.event.get()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock.tick(FPS)

    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    main_menu()
                    start_screen = False

        screen.blit(startscreen_img, startscreen_rect)
        pygame.display.flip()

def game_over_noscore():
    WIDTH = 1280
    HEIGHT = 800
    pygame.event.get()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(gameovernoscore_img, noscore_rect)
    pygame.display.flip()

    gameover_screen = True
    while gameover_screen:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    gameover_screen = False
                    main_menu()

# ----------------------------------------------------------------------------------- #
# --------------------------------- Alperens code ----------------------------------- #

class alpGame:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "alpimg")
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.alp_spritesheet = alpSpritesheet(path.join(img_dir, SPRITESHEET))
        self.alp_spritesheet2 = alpSpritesheet2(path.join(img_dir, SPRITESHEET2))
        self.alp_spritesheet3 = alpSpritesheet3(path.join(img_dir, SPRITESHEET3))
        self.alp_spritesheet4 = alpSpritesheet4(path.join(img_dir, SPRITESHEET4))
        # load sound
        self.alp_snd_dir = path.join(self.dir, "alpsnd")
        self.alp_jump_sound = pg.mixer.Sound(path.join(self.alp_snd_dir, "alpjump1.wav"))
        self.alp_gameover_sound = pg.mixer.Sound(path.join(self.alp_snd_dir, "alpgameover.wav"))
        self.alp_powerups_sound = pg.mixer.Sound(path.join(self.alp_snd_dir, "alpboost.wav"))

    def new(self):
        # start a new game
        self.score = 0
        self.alp_all_sprites = pg.sprite.Group()
        self.alp_platforms = pg.sprite.Group()
        self.alp_powerups = pg.sprite.Group()
        self.alp_player = alpPlayer(self)
        for plat in PLATFORM_LIST:
            alpPlatform(self, *plat)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.alp_all_sprites.update()
        # check if player hits a platform - only if falling
        if self.alp_player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.alp_player, self.alp_platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.alp_player.pos.x < lowest.rect.right + 15 and self.alp_player.pos.x > lowest.rect.left - 15:
                    if self.alp_player.pos.y < lowest.rect.bottom:
                        self.alp_player.pos.y = lowest.rect.top
                        self.alp_player.vel.y = 0
                        self.alp_player.jumping = False

        # if player reaches top 1/4 of screen
        if self.alp_player.rect.top <= HEIGHT / 4:
            self.alp_player.pos.y += abs(self.alp_player.vel.y)
            for plat in self.alp_platforms:
                plat.rect.y += abs(self.alp_player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Powerup
        pow_hits = pg.sprite.spritecollide(self.alp_player, self.alp_powerups, True)
        for power in pow_hits:
                self.alp_player.vel.y = -BOOST_POWER
                self.alp_player.jumping = False
                self.alp_powerups_sound.play()

        # Die!
        if self.alp_player.rect.bottom > HEIGHT:
            for sprite in self.alp_all_sprites:
                sprite.rect.y -= max(self.alp_player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.alp_platforms) == 0:
            self.playing = False
            self.alp_gameover_sound.play()

        # spawn new platforms to keep same average number
        while self.score < 1250 and len(self.alp_platforms) < 7:
            width = random.randrange(50, 100)
            alpPlatform(self, random.randrange(0, WIDTH - width),
                        random.randrange(-75, -30))

        while self.score > 1250 and self.score < 3000 and len(self.alp_platforms) < 6:
            width = random.randrange(50,100)
            alpPlatform(self, random.randrange (0, WIDTH - width),
                        random.randrange(-75, -30))

        while self.score > 3000 and len(self.alp_platforms) < 5:
            width = random.randrange(50,100)
            alpPlatform(self, random.randrange (0, WIDTH - width),
                        random.randrange(-75, -30))

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.alp_player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.alp_player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.alp_all_sprites.draw(self.screen)
        self.screen.blit(self.alp_player.image, self.alp_player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        WIDTH = 1280
        HEIGHT = 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        gameover_screen = True
        while gameover_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        main_menu()
                        gameover_screen = False

            screen.blit(gameover_img, gameover_rect)
            self.draw_text(str(self.score), 50, WHITE, WIDTH / 2 + 70, HEIGHT / 2 - 8)
            pygame.display.flip()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = alpGame()

# ---------------------------------------------------------------- #
# ----------------------------Zylans Code------------------------- #
from zysettings import *

# 66 * 113
# Images
zyplayer_img = pygame.image.load(path.join(img_dir, "playership.png")).convert()
zyenemyship_img = pygame.image.load(path.join(img_dir, "enemyship.png")).convert()
zybullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
zyenemybullet_img = pygame.image.load(path.join(img_dir, "enemybullet.png")).convert()
zyplayer_mini_img = pygame.transform.scale(zyplayer_img, (20, 30))
zyplayer_mini_img.set_colorkey(BLACK)
zyenemy_mini_img = pygame.transform.scale(zyenemyship_img, (33, 57))
zyenemy_mini_img.set_colorkey(BLACK)
zy_background = pygame.image.load(path.join(img_dir, "background.jpg")).convert()
zy_background_rect = zy_background.get_rect()
startscreen_img = pygame.image.load(path.join(img_dir, "startscreen.png")).convert()
mainmenu_img = pygame.image.load(path.join(img_dir, "mainmenu.png")).convert()
gameover_img = pygame.image.load(path.join(img_dir, "gameover.png")).convert()
startscreen_rect = startscreen_img.get_rect()
mainmenu_rect = mainmenu_img.get_rect()
gameover_rect = gameover_img.get_rect()
gameovernoscore_img  = pygame.image.load(path.join(img_dir, "gameovernoscore.png")).convert()
noscore_rect = gameovernoscore_img.get_rect()
zytutorial_img = pygame.image.load(path.join(img_dir, "zytutorial.png")).convert()
zytutorial_rect = zytutorial_img.get_rect()

# Sprite groups


# Classes

class zyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(zyplayer_img, (33, 57))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
       # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.shotsfired = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom < 30:
            self.rect.bottom = 30

    def shoot(self):
        bullet = zyBullet(self.rect.centerx, self.rect.top)
        zy_all_sprites.add(bullet)
        zy_bullets.add(bullet)
        self.shotsfired += 1

class zyEnemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(zyenemybullet_img, (25, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 11
      #  pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange (4, 10)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -10 or self.rect.right > WIDTH + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 9)
            self.speedx = random.randrange(-2, 2)

class zyBullet(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(zybullet_img, (20, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 9
      #  pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -7

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < -50:
            self.kill()
            zyplayer.shotsfired -= 1

class zyEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = zyenemyship_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
      #  pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.y = 10
        self.speedx = 5
        self.enemylives = 5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x >= WIDTH - 38:
            self.speedx = (self.speedx + 1) * -1
        if self.rect.x <= 0:
            self.speedx = (self.speedx - 1) * -1
        if self.speedx >= 20:
            self.speedx = -6
        if self.speedx <= -20:
            self.speedx = 6
        if self.speedx > 14:
            zy_bul = 1
        if self.speedx < 14:
            zy_bul = 20

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 23 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_enemylives(surf, x, y, enemylives, img):
    for i in range(enemylives):
        img_rect = img.get_rect()
        img_rect.x = x + 26 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def zy_drawgame():
    screen.fill(BLACK)
    screen.blit(zy_background, zy_background_rect)
    zy_all_sprites.draw(screen)
    draw_lives(screen, WIDTH - 100, 5, zyplayer.lives, zyplayer_mini_img)
    draw_enemylives(screen, 0, 5, zy_enemy.enemylives, zyenemy_mini_img)
    pygame.display.flip()

zy_all_sprites = pygame.sprite.Group()
zy_enemybullets = pygame.sprite.Group()
zy_bullets = pygame.sprite.Group()
zy_enemies = pygame.sprite.Group()

def zy_mainloop():
    WIDTH = 480
    HEIGHT = 600
    pygame.event.get()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    zy_running = True
    score = 0

    while zy_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                zy_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and zyplayer.shotsfired <= 1:
                    zyplayer.shoot()

        # Update
        zy_all_sprites.update()

        # Hit Check
        hits = pygame.sprite.groupcollide(zy_bullets, zy_enemybullets, True, True, pygame.sprite.collide_circle)
        for hit in hits:
            m = zyEnemyBullet()
            zy_all_sprites.add(m)
            zy_enemybullets.add(m)
            zyplayer.shotsfired -= 1

        hits = pygame.sprite.spritecollide(zyplayer, zy_enemybullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            zyplayer.lives -= 1
            m = zyEnemyBullet()
            zy_all_sprites.add(m)
            zy_enemybullets.add(m)
        hits = pygame.sprite.groupcollide(zy_bullets, zy_enemies, True, False, pygame.sprite.collide_circle)
        for hit in hits:
            zy_enemy.enemylives -= 1
            zyplayer.shotsfired -= 1
        hits = pygame.sprite.spritecollide(zyplayer, zy_enemies, False, pygame.sprite.collide_circle)
        for hit in hits:
            zyplayer.lives -= 3

        # Win / Lose condition
        if zyplayer.lives <= 0:
            score = 50 - (zy_enemy.enemylives * 10)
            zy_running = False
            zyplayer.lives = 3
            zy_enemy.enemylives = 5
            zyplayer.rect.centerx = WIDTH / 2
            zyplayer.rect.bottom = HEIGHT - 10
            WIDTH = 1280
            HEIGHT = 800
            pygame.event.get()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            screen.blit(gameover_img, gameover_rect)
            pygame.font.init()
            myfont = pygame.font.SysFont('Arial', 50)
            headertext = myfont.render(str(score), False, (WHITE))
            screen.blit(headertext, (WIDTH / 2 + 70, HEIGHT / 2 - 8))
            pygame.display.flip()

            gameover_screen = True
            while gameover_screen:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            gameover_screen = False
                            main_menu()
        if zy_enemy.enemylives <= 0:
            score = 50 + (zyplayer.lives * 50)
            zy_running = False
            zyplayer.lives = 3
            zy_enemy.enemylives = 5
            zyplayer.rect.centerx = WIDTH / 2
            zyplayer.rect.bottom = HEIGHT - 10
            WIDTH = 1280
            HEIGHT = 800
            pygame.event.get()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            screen.blit(gameover_img, gameover_rect)
            pygame.font.init()
            myfont = pygame.font.SysFont('Arial', 50)
            headertext = myfont.render(str(score), False, (WHITE))
            screen.blit(headertext, (WIDTH / 2 + 70, HEIGHT / 2 - 8))
            pygame.display.flip()

            gameover_screen = True
            while gameover_screen:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:
                            gameover_screen = False
                            main_menu()

        # Draw
        zy_drawgame()

for i in range(8):
    zy = zyEnemyBullet()
    zy_enemybullets.add(zy)
    zy_all_sprites.add(zy)

zyplayer = zyPlayer()
zy_all_sprites.add(zyplayer)
zy_enemy = zyEnemy()
zy_all_sprites.add(zy_enemy)
zy_enemies.add(zy_enemy)

def zytutorial():
    WIDTH = 480
    HEIGHT = 600
    pygame.event.get()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    zy_tutorial = True
    while zy_tutorial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    zy_tutorial = False
                    zy_mainloop()
        screen.blit(zytutorial_img, zytutorial_rect)
        pygame.display.flip()


# --------------------------- Marks Code ----------------------- #

pygame.init()

myfont = pygame.font.SysFont("timesnewroman", 20)

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# set resolution
pygame.display.set_caption('Treasure Hunter')

z = random.randint(1, 5)

clock = pygame.time.Clock()

winning_screen = pygame.image.load(path.join(img_dir, "Treasure.png")).convert()

False_answer = pygame.image.load(path.join(img_dir, "wrong.png")).convert()

mkPlayer_img = pygame.image.load(path.join(img_dir, "mkPlayer.png")).convert()


class mkPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mkPlayer_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
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
        self.image = pygame.Surface((45, 45))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.center = (140, 170)


class TreasureII(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 45))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.center = (745, 292)


class TreasureIII(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 45))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.center = (208, 570)


class TreasureIV(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 45))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)


class TreasureV(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 45))
        self.image.fill(red)
        self.image.set_colorkey(red)
        self.rect = self.image.get_rect()
        self.rect.center = (670, 175)


# define sprites
all_sprites = pygame.sprite.Group()
treasures = pygame.sprite.Group()
player = mkPlayer()
Treasure = Treasure()
TreasureII = TreasureII()
TreasureIII = TreasureIII()
TreasureIV = TreasureIV()
TreasureV = TreasureV()
all_sprites.add(player)
treasures.add(Treasure, TreasureII, TreasureIII, TreasureIV, TreasureV)
# define keystate
keystate = pygame.key.get_pressed()


# mainloop

def mkGame():
    pygame.event.get()
    screen = pygame.display.set_mode((950, 600))
    gameDisplay = pygame.display.set_mode((950, 600))
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                gameExit = True

        background_image = pygame.image.load(path.join(img_dir, "bg - new.jpg")).convert()
        screen.blit(background_image, [0, 0])
        all_sprites.update()
        all_sprites.draw(screen)

        if z == 1:
            label = myfont.render("Y nbslt uif tqpu", 1, (255, 255, 0))
            screen.blit(label, (805, 10))
        elif z == 2:
            label = myfont.render("My eye is dark", 1, (255, 255, 0))
            screen.blit(label, (805, 10))
            label = myfont.render("My mane is", 1, (255, 255, 0))
            screen.blit(label, (805, 30))
            label = myfont.render("yellow", 1, (255, 255, 0))
            screen.blit(label, (805, 50))
            label = myfont.render("I am a bit", 1, (255, 255, 0))
            screen.blit(label, (805, 90))
            label = myfont.render("of a tropical", 1, (255, 255, 0))
            screen.blit(label, (805, 110))
            label = myfont.render("fellow", 1, (255, 255, 0))
            screen.blit(label, (805, 130))
        elif z == 3:
            label = myfont.render("255,0,0", 1, (255, 255, 0))
            screen.blit(label, (805, 10))
            label = myfont.render("220° (Compass)", 1, (255, 255, 0))
            screen.blit(label, (805, 30))
        elif z == 4:
            label = myfont.render("You've almost", 1, (255, 255, 0))
            screen.blit(label, (805, 10))
            label = myfont.render("given up", 1, (255, 255, 0))
            screen.blit(label, (805, 30))
            label = myfont.render("You're almost", 1, (255, 255, 0))
            screen.blit(label, (805, 50))
            label = myfont.render("done", 1, (255, 255, 0))
            screen.blit(label, (805, 70))
            label = myfont.render("then you realise", 1, (255, 255, 0))
            screen.blit(label, (805, 90))
            label = myfont.render("go back", 1, (255, 255, 0))
            screen.blit(label, (805, 130))
            label = myfont.render("to square one", 1, (255, 255, 0))
            screen.blit(label, (805, 150))
        elif z == 5:
            label = myfont.render("Adventurer Jim", 1, (255, 255, 0))
            screen.blit(label, (805, 10))
            label = myfont.render("The treasure was", 1, (255, 255, 0))
            screen.blit(label, (805, 50))
            label = myfont.render("his to earn", 1, (255, 255, 0))
            screen.blit(label, (805, 70))
            label = myfont.render("With excitement", 1, (255, 255, 0))
            screen.blit(label, (805, 90))
            label = myfont.render("filled to the brim", 1, (255, 255, 0))
            screen.blit(label, (805, 110))
            label = myfont.render("He took a wrong", 1, (255, 255, 0))
            screen.blit(label, (805, 130))
            label = myfont.render("turn", 1, (255, 255, 0))
            screen.blit(label, (805, 150))
            label = myfont.render("it was the death", 1, (255, 255, 0))
            screen.blit(label, (805, 190))
            label = myfont.render("of him", 1, (255, 255, 0))
            screen.blit(label, (805, 210))
        if z == 1:
            if pygame.sprite.collide_rect(player, Treasure) and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(winning_screen, [125, 0])
                game_over_noscore()
            if pygame.sprite.collide_rect(player, Treasure) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(False_answer, [100, 0])
        elif z == 2:
            if pygame.sprite.collide_rect(player, TreasureII) and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(winning_screen, [125, 0])
                game_over_noscore()
            if pygame.sprite.collide_rect(player, TreasureII) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(False_answer, [100, 0])
        elif z == 3:
            if pygame.sprite.collide_rect(player, TreasureIII) and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(winning_screen, [125, 0])
                game_over_noscore()
            if pygame.sprite.collide_rect(player, TreasureIII) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(False_answer, [100, 0])
        elif z == 4:
            if pygame.sprite.collide_rect(player, TreasureIV) and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(winning_screen, [125, 0])
                game_over_noscore()
            if pygame.sprite.collide_rect(player, TreasureIV) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(False_answer, [100, 0])
        elif z == 5:
            if pygame.sprite.collide_rect(player, TreasureV) and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(winning_screen, [125, 0])
                game_over_noscore()
            if pygame.sprite.collide_rect(player, TreasureV) == False and pygame.key.get_pressed()[pygame.K_SPACE]:
                screen.blit(False_answer, [100, 0])

        pygame.display.update()
        clock.tick(180)

# ----------------------------------------------------------------------------------- #
# --------------------------------- Xanders code ------------------------------------ #

os.environ['SDL_VIDEO_CENTERED'] = '1'  # dit spawnt het scherm in het midden van je scherm

def xandergame():
    def XStartmenu():
        pygame.mixer.init()
        pygame.mixer.music.load(path.join(mus_dir,"Flutey_World.mp3"))
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.fadeout
        WIDTH = 700
        HEIGHT = 600
        screentut = pygame.display.set_mode((WIDTH, HEIGHT))
        background_imagetwee = pygame.image.load(path.join(img_dir,"Xanderspelintroachtergrond.jpg")).convert()
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
            pygame.mixer.music.queue(path.join(mus_dir,"GasGasGas.mp3"))
            randommuziek = random.randrange(0,5)
            if randommuziek == 0:
                pygame.mixer.music.load(path.join(mus_dir,"Run.mp3"))
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 1:
                pygame.mixer.music.load(path.join(mus_dir,"Factory.mp3"))
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 2:
                pygame.mixer.music.load(path.join(mus_dir,"Radiocutter.mp3"))
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 3:
                pygame.mixer.music.load(path.join(mus_dir,"Twilighttechno.mp3"))
                pygame.mixer.music.play(0)
                print(randommuziek)
            elif randommuziek == 4:
                pygame.mixer.music.load(path.join(mus_dir,"Gloriousmorning.mp3"))
                pygame.mixer.music.play(0)
                print(randommuziek)
            #def stopmusic(self):
            #    pygame.mixer.music.rewind

        #playerimg Xander

        player_image =      pygame.image.load(path.join(img_dir,"Xanderspelschipplayergrootmelkzijlen.png")).convert_alpha()#.convert()
        bullet_imageleft =  pygame.image.load(path.join(img_dir,"Bulletgoingleft.png")).convert_alpha()
        bullet_imageright = pygame.image.load(path.join(img_dir,"Bulletgoingright.png")).convert_alpha()
        bullet_imageup =    pygame.image.load(path.join(img_dir,"Bulletgoingup.png")).convert_alpha()
        bullet_imagedown =  pygame.image.load(path.join(img_dir,"Bulletgoingdown.png")).convert_alpha()
        seadrakeleft =      pygame.image.load(path.join(img_dir,"seadrakered.png")).convert_alpha()
        seadrakeright =     pygame.image.load(path.join(img_dir,"seadrakeblue.png")).convert_alpha()
        seadrakedown =      pygame.image.load(path.join(img_dir,"seadrakeblue2.png")).convert_alpha()
        seadrakeup =        pygame.image.load(path.join(img_dir,"seadrakered2.png")).convert_alpha()
        seakrakenright =    pygame.image.load(path.join(img_dir,"seakrakenright.png")).convert_alpha()
        seakrakenleft =     pygame.image.load(path.join(img_dir,"seakrakenleft.png")).convert_alpha()
        badguyshipright =   pygame.image.load(path.join(img_dir,"Slechterikshiprechts.png")).convert_alpha()
        badguyshipleft =   pygame.image.load(path.join(img_dir,"Slechterikshiplinks.png")).convert_alpha()
        morelives   =       pygame.image.load(path.join(img_dir,"Morelives.png")).convert_alpha()
        moreammo    =       pygame.image.load(path.join(img_dir,"Moreammo.png")).convert_alpha()
        morescore   =       pygame.image.load(path.join(img_dir,"Morescore.png")).convert_alpha()




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

        background_image = pygame.image.load(path.join(img_dir,"Seaofdreadfinalbackgroundsmall2.jpg")).convert()


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
        pygame.mixer.music.load(path.join(mus_dir,"Wahwahwah.mp3"))
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
        background_imagetwee = pygame.image.load(path.join(img_dir,"XanderspelGameover.jpg")).convert()
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
                    main_menu()
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
