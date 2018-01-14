import pygame
from zyclasses import *

def main_menu():
    WIDTH = 1280
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    WIDTH = 480
                    HEIGHT = 600
                    pygame.display.set_mode((WIDTH, HEIGHT))
                    g.new()
                    g.show_go_screen()
                    main_menu = False
                if event.key == pygame.K_2:
                    zy_mainloop()
                    main_menu = False


       # pygame.font.init()
       # myfont = pygame.font.SysFont('Arial', 30)
       # headertext = myfont.render('Main Menu', False, (0, 0, 0))
       # maintext = myfont.render('Press 1 to start the game', False, (0, 0, 0))
        screen.blit(mainmenu_img, mainmenu_rect)
       # screen.blit(headertext, (180, 0))
       # screen.blit(maintext, (180, 200))
        pygame.display.flip()


def game_over():
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
