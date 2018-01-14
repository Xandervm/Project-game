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
            zyplayer.lives == 3
            zy_enemy.enemylives == 5
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

                pygame.display.flip()
        if zy_enemy.enemylives == 0:
            zyplayer.lives == 3
            zy_enemy.enemylives == 5
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

                pygame.display.flip()

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