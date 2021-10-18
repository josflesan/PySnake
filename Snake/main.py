# Snake Game coded in Python
# Coded by: Josflesan (https://github.com/josflesan)

import pygame, sys
import os.path

import scripts.snake as snake
import scripts.fruit as fruit
import scripts.pygame_textinput as pt

# pygame_textinput original creator: Nearoo on GitHub
# https://github.com/Nearoo/pygame-text-input

# FETCH NECESSARY FILES AND ASSETS -------------------------------------

def get_file(file, folder, main_dir):

    file = os.path.join(main_dir, folder, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit("The file %s could not be loaded: %s" %
                         (file, pygame.get_error()))
    return surface

# ---------------------------------------------------------------------

# CONSTANTS --------------------------------------

SCREEN_W = 300
SCREEN_H = 600
MARGIN_X = int(SCREEN_W * 0.05)
MARGIN_Y = int(SCREEN_H * 0.15)
SCREENRECT = pygame.Rect(0, 0, SCREEN_W+2, SCREEN_H+2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (209, 24, 24)
BLUE = (18, 57, 155)
PLAYER_COL = (23, 45, 123)
FRUIT_COL = (12, 234, 11)

# -------------------------------------------------

# VARIABLES ---------------------------------------

eaten = False  # Boolean to detect presence of fruit
points = 0  # Points obtained by the user

# -------------------------------------------------

# SETUP -------------------------------------------

main_dir = os.path.split(os.path.abspath(__file__))[0]  # ROOT PATH
pygame.init()
winstyle = 0 
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
pygame.display.set_caption("Python Snake")
clock = pygame.time.Clock()

# MUSIC AND SFX SETUP
pygame.mixer.music.load(os.path.join(os.getcwd() + "\\Snake\\music\\bgmusic.wav"))
sfx = pygame.mixer.Sound(os.path.join(os.getcwd() + "\\Snake\\music\\munch.wav"))

#---------------------------------------------------

# SPRITES AND ASSETS ------------------------------------------
head = snake.Snake(PLAYER_COL, 47 + MARGIN_X, 47 + MARGIN_Y)
f0 = fruit.Fruit(FRUIT_COL, SCREEN_W, SCREEN_H, MARGIN_X, MARGIN_Y)

# IMAGES
title_screen = get_file("MenuScreen.png", "graphics", main_dir)
death_screen = get_file("DeathScreen.png", "graphics", main_dir)
bg = get_file("ArcadeMachine.png", "graphics", main_dir)
bg = pygame.transform.scale(bg, [SCREEN_W, SCREEN_H])

# FONTS
font = pygame.font.Font(os.path.join(os.getcwd() + "\\Snake\\fonts\\Chocolate Cavalcade.otf"), 20)
insert_coin = pygame.font.Font(os.path.join(os.getcwd() + "\\Snake\\fonts\\Chocolate Cavalcade.otf"), 30)
deathfont = pygame.font.Font(os.path.join(os.getcwd() + "\\Snake\\fonts\\Chocolate Cavalcade.otf"), 16)

# ----------------------------------------------------------------

# GAME, MENU & DEATHSCREEN ---------------------------------------------------------------

def menu():

    game_start = False
    blink = 0
    pygame.mixer.music.play(loops=-1)  # Play background music indefinitely

    while not game_start:

        blink += 1  # Variable controlling "insert coin" animation

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game_start = False
                close()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game()

        background = pygame.Surface(SCREENRECT.size) 
        background.fill(BLACK)

        txt = insert_coin.render("INSERT COIN", True, RED)
        txt.set_colorkey(BLACK)

        background.blit(bg, [0, 0])
        screen.blit(background, [0, 0])
        screen.blit(title_screen, [MARGIN_X, MARGIN_Y])
        if (blink % 5) == 0:
            screen.blit(txt, [75, 400])

        pygame.display.flip()
        clock.tick(5)

        if blink > 100:
            blink = 0

    close()


def game():

    is_running = True

    player_dx, player_dy = [0, 0]
    unit = True  # Keep track of whether head is the only body part for movement

    global head, f0

    snake_body = [head, ]
    fruits = [f0, ]
    
    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_running = False

            elif event.type == pygame.KEYDOWN:  

                if len(snake_body) > 1:
                    unit = False

                if event.key == pygame.K_w:
                    if player_dy != 1 or unit:
                        player_dx, player_dy = [0, -1]
                        pygame.time.wait(10)
                elif event.key == pygame.K_s:
                    if player_dy != -1 or unit:
                        player_dx, player_dy = [0, 1]
                        pygame.time.wait(10)
                elif event.key == pygame.K_d:
                    if player_dx != -1 or unit:
                        player_dx, player_dy = [1, 0]
                        pygame.time.wait(10)
                elif event.key == pygame.K_a:
                    if player_dx != 1 or unit:
                        player_dx, player_dy = [-1, 0]
                        pygame.time.wait(10)

        # Frame setup ------------------------------------------------------------

        global points  # Points variable 

        background = pygame.Surface(SCREENRECT.size)
        background.fill(BLACK)
        
        scoreBoard = font.render(str(points), True, BLUE)  # Render text onto surface
        scoreBoard.set_colorkey(WHITE)  # Make surface transparent on white background

        all = pygame.sprite.RenderUpdates()  # Group containing all sprites in use

        all.clear(screen, background)  # Clear scene

        for row in range(MARGIN_Y, SCREEN_H-MARGIN_Y+10, 30):
            pygame.draw.line(background, WHITE, [MARGIN_X, row], [SCREEN_W-MARGIN_X, row], 2)
            for col in range(MARGIN_X, SCREEN_W-MARGIN_X+10, 30):
                pygame.draw.line(background, WHITE, [col, MARGIN_Y], [col, SCREEN_H-MARGIN_Y], 2)

        background.blit(bg, [0, 0])

        screen.blit(background, [0, 0])
        screen.blit(scoreBoard, [57, 565])

        # -----------------------------------------------------------------------

        # FRAME CHANGE ----------------------------------------------------------

        for f in fruits:

            if f.eaten(snake_body[0], SCREEN_W, SCREEN_H, sfx, fruits):

                body_len = len(snake_body)+1 
                points += (50 * (body_len//2) + 25)  # Algorithm to add points 

                # If all the fruit has been eaten...
                if len(fruits) == 0:
                    for i in range(body_len//3 + 1):
                        i = fruit.Fruit(FRUIT_COL, SCREEN_W, SCREEN_H, MARGIN_X, MARGIN_Y)  # Spawn more fruit
                        fruits.append(i)  # Add it to the list

                # Track current head (x, y) position
                head_x = head.rect.x
                head_y = head.rect.y

                body_part = snake.Snake(PLAYER_COL, (head_x - (30 * body_len * player_dx)),
                                        (head_y - (30 * body_len * player_dy)))
                snake_body.append(body_part)

            f.update(screen)         

        # Move head and other parts
        head.move(player_dx, player_dy, snake_body)
        head.game_over(death, snake_body)

        for part in snake_body:
            # Display all of the body parts
            part.update(screen, SCREEN_W, SCREEN_H, MARGIN_X, MARGIN_Y)
            part.check_bound(SCREEN_W, SCREEN_H, MARGIN_X, MARGIN_Y)  # Wrap around for all snake pieces

        update = all.draw(screen)
        pygame.display.update(update)
        pygame.display.flip()
        clock.tick(10)

        # -----------------------------------------------------------------------

    close()


def death():

    finished = False
    updateScores = False
    data = []  # Array to contain high score data
    pygame.mixer.music.stop()

    Scorefile = os.path.join(main_dir, "data", "hiScores.txt")  # Access data folder

    with open(Scorefile) as f1:
        lines = f1.readlines()
        for l in range(len(lines)):
            cont = lines[l].split(",")
            data.append([cont[0], cont[1].rstrip("\n")])
    f1.close()

    # Create input box
    input_box = pt.TextInput(initial_string="Player Name")

    while not finished:
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game_start = False
                close()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restore points
                global points
                points = 0
                menu()

        background = pygame.Surface(SCREENRECT.size)
        background.fill(BLACK)

        hi_score = pygame.Surface([SCREEN_W-(2*MARGIN_X) - 20, 108])
        hi_score.set_colorkey(BLACK)

        inputScore = pygame.Surface([SCREEN_W - (2*MARGIN_X) - 20, 25])
        inputScore.fill(WHITE)

        # Blit input_box surface onto inputSurface
        inputScore.blit(input_box.get_surface(), [10, 0])

        scoreBoard = font.render(str(points), True, [18, 57, 155])
        scoreBoard.set_colorkey(WHITE)

        for i in range(len(data)):
            TopScore = deathfont.render(str(data[i][0] + " .......... " + data[i][1]), True, [18, 57, 155])
            hi_score.blit(TopScore, [40, 18*i + 5])

        background.blit(bg, [0, 0])
        screen.blit(background, [0, 0])
        screen.blit(scoreBoard, [57, 565])
        screen.blit(death_screen, [MARGIN_X, MARGIN_Y])
        screen.blit(hi_score, [MARGIN_X+10, 270])
        screen.blit(inputScore, [25, SCREEN_H - MARGIN_Y - 60])

        if input_box.update(events):  # User pressed RETURN key
            updateScores = True
            playerName = input_box.get_text()[:7]
            finished = True

        pygame.display.flip()
        clock.tick(10)

    # Update data list
    if updateScores:
        # Check to see if score higher than any in the file
        for d in data:
            if int(d[1]) < points:
                d[0] = playerName  # Change Name, get first 7 chars 
                newScore = str(points)
                # Change points, pad with 0s so 6 chars in total
                d[1] = newScore.zfill(6)
                break

    # Update SCOREFILE
    with open(Scorefile, "w") as f1:
        for line in data:
            f1.write(line[0] + "," + line[1] + "\n")
    f1.close()

    close()

def close():
    pygame.quit()
    quit()

if __name__ == "__main__":
    menu()  
