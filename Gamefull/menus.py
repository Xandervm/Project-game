import pygame, sys
from pygame.locals import *
from zyclasses import *
from zysettings import *
from alpsprites import *

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

