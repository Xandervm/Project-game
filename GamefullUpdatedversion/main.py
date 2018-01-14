from menus import *

# Main loop
game_running = True
while game_running:
    clock.tick(FPS)
    pygame.init()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False


    start_screen()

