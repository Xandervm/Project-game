import pygame
import random
import os

pygame.init()

myfont = pygame.font.SysFont("timesnewroman", 20)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

screen = pygame.display.set_mode((800,600))

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Prototype I')

gameExit = False

lead_x = 400
lead_y = 300
lead_x_change = 0
lead_y_change = 0

z = random.randint(1,3)


clock = pygame.time.Clock()

while not gameExit:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        gameExit = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                lead_x_change = -2
                        elif event.key == pygame.K_RIGHT:
                                lead_x_change = 2

                        elif event.key == pygame.K_UP:
                                lead_y_change = -2
                        elif event.key == pygame.K_DOWN:
                                lead_y_change = 2
                        elif event.key == pygame.K_ESCAPE:
                                gameExit = True
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                lead_x_change = 0
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                                lead_y_change = 0
                        

        lead_x += lead_x_change
        lead_y += lead_y_change
        background_image = pygame.image.load("bg.jpg")
        screen.blit(background_image, [0,0])
        pygame.draw.rect(gameDisplay, white, [lead_x,lead_y,10,10])
        if z == 1:
                pygame.draw.rect(gameDisplay, black, [100,100,10,10])
                label = myfont.render("hint #1", 1, (255,255,0))
                screen.blit(label, (700, 10))
        elif z == 2:
                pygame.draw.rect(gameDisplay, black, [200,300,10,10])
                label = myfont.render("hint #2", 1, (255,255,0))
                screen.blit(label, (700, 10))
        elif z == 3:
                pygame.draw.rect(gameDisplay, black, [150,50,10,10])
                label = myfont.render("hint #3", 1, (255,255,0))
                screen.blit(label, (700, 10))
        if z == 1:
                if (lead_x,lead_y) == (100,100) and event.key == pygame.K_SPACE:
                        gameExit = True
        elif z == 2:
                if (lead_x,lead_y) == (200,300) and event.key == pygame.K_SPACE:
                        gameExit = True
        elif z == 3:
                if (lead_x,lead_y) == (150,50) and event.key == pygame.K_SPACE:
                        gameExit = True
                        
                        
        pygame.display.update()
        clock.tick(180)

pygame.quit()
quit()
