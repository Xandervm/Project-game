TITLE = "Pirate Jumper!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "alpplayer.png"
SPRITESHEET2 = "alpplatform.png"
SPRITESHEET3 = "alpplatform2.png"
SPRITESHEET4 = "alporangeboost2.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.7
PLAYER_JUMP = 22

# Game properties
BOOST_POWER = 37
POW_SPAWN_PCT = 5

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 50),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (400, 50),
                 (350, 200),
                 (200, 300)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE