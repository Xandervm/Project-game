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

# Sprite groups

zy_all_sprites = pygame.sprite.Group()
zy_enemybullets = pygame.sprite.Group()
zy_bullets = pygame.sprite.Group()
zy_enemies = pygame.sprite.Group()

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

def zy_mainloop():
    WIDTH = 480
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    zy_running = True
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
        if zyplayer.lives == 0:
            pygame.quit()
            # zy_running = False

        if zy_enemy.enemylives == 0:
            pygame.quit()
            # zy_running = False


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












