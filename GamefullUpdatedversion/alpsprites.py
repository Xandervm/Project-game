import pygame as pg
from alpsettings import *
from random import choice, randrange
vec = pg.math.Vector2

class alpSpritesheet:
    def __init__(self, filename):
        self.alp_spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.alp_spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 6, height // 6))
        return image

class alpSpritesheet2:
    def __init__(self, filename):
        self.alp_spritesheet2 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.alp_spritesheet2, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 1 // 2, height * 1 // 2))
        return image

class alpSpritesheet3:
    def __init__(self, filename):
        self.alp_spritesheet3 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.alp_spritesheet3, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 13 // 40, height // 2))
        return image

class alpSpritesheet4:
    def __init__(self, filename):
        self.alp_spritesheet4 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.alp_spritesheet4, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 5, height // 5))
        return image

class alpPlayer(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.alp_all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.alp_spritesheet.get_image(0, 0, 690, 640)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -4:
                self.vel.y = -4

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.alp_platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.alp_jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class alpPlatform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.alp_all_sprites, game.alp_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.alp_spritesheet2.get_image(0, 0, 163, 62), (self.game.alp_spritesheet3.get_image(0,0,337, 60))]
        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            alpPow(self.game, self)

class alpPow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.alp_all_sprites, game.alp_powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])
        self.image = self.game.alp_spritesheet4.get_image(0,0, 400, 300)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.bottom  - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.alp_platforms.has(self.plat):
            self.kill()