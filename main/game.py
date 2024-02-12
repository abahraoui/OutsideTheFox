import math
import pickle
import random
import sys
from copy import copy
from itertools import cycle
import startscreen

import pygame
import square as sq
import player
import tile as tile_class
from pygame.locals import *
import spritesheet
import userinputfield
import inputboxvalidator

# Event handler
def events():
    global paused, scroll, goal_scroll, scrolling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        # Start game handler
        elif event.type == KEYDOWN and event.key == K_F1:
            paused = False
        if P:
            # if event.type == KEYDOWN and event.key == K_h and not P.get_blocked_right() and not P.get_lerping() and scroll < (
            #         MAX_COLS * TILE_SIZE) - W:
            #     P.moveRight()
            #     if P.get_reach_right_boundary():
            #         goal_scroll = scroll + TILE_SIZE / 2 + W - 427.5
            #     else:
            #         goal_scroll = scroll + TILE_SIZE / 2
            #     scrolling = True
            #
            # elif event.type == KEYDOWN and event.key == K_f and not P.get_blocked_left() and not P.get_lerping() and scroll > 0:
            #     P.moveLeft(scroll)
            #     goal_scroll = scroll - TILE_SIZE / 2
            #     scrolling = True
            #
            # if event.type == KEYUP and (event.key == K_h or event.key == K_f):
            #     P.notMoving()
            #
            # if event.type == KEYDOWN and event.key == K_g:
            #     P.jump()
            if input_validator.isDone():

                if user_input.mouse_colliding(pygame.mouse.get_pos()):
                    user_input.set_mouse_over(True)
                    user_input.color = "red"
                else:
                    user_input.set_mouse_over(False)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_input.mouse_colliding(event.pos):
                        user_input.set_active(True)
                    else:
                        user_input.set_active(False)

                if event.type == pygame.KEYDOWN and user_input.get_active():
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        user_input.remove_text()

                    elif event.key == 13:  # Code for ENTER Key.
                        user_input.set_newline()
                        # Unicode standard is used for string
                    # formation
                    else:
                        user_input.add_text(event.unicode)


def spawnHandler():
    global squares
    global spawnCounter
    spawnCounter += 1
    '''Use clock ticks rather than this method for both Spawns and Player anims'''
    if spawnCounter % 100 == 0:
        squares.add(sq.Square(random.choice(colors), random.randint(0, W), 0, (W, H)))


# Draws and makes the background scrollable.
def draw_bg():
    screen.fill('crimson')
    width = bg.get_width()
    for x in range(4):
        screen.blit(bg, ((x * width) - scroll * 0.5, 0))
        screen.blit(md, ((x * width) - scroll * 0.8, 300))
        screen.blit(md, ((x * width) - scroll * 0.8 + 400, 300))
        screen.blit(md, ((x * width) - scroll * 0.8 + 780, 300))
        screen.blit(md, ((x * width) - scroll * 0.8, 492))
        screen.blit(md, ((x * width) - scroll * 0.8 + 442, 450))
        screen.blit(md, ((x * width) - scroll * 0.8 + 822, 450))


# Changes the scroll direction of the world.
def change_scroll_direction():
    global scroll
    if scroll_left and scroll > 0 and P.stop_scroll() != "L":
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - W and P.stop_scroll() != "R":
        scroll += 5 * scroll_speed


# Draw each tile based on position in the grid.
def draw_world():
    global coordinates_filled
    ground.empty()
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):

            if world_coordinates[y][x] == (0, 0) and not coordinates_filled:
                world_coordinates[y][x] = (x * TILE_SIZE, y * TILE_SIZE)
                if (x, y) == (149, 15):
                    coordinates_filled = True
            if tile >= 0:
                if tile not in background_tiles:
                    t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (W, H), tiles_list[tile])
                    ground.add(t)
                    t.draw()
                    dummy = copy(P)
                    if P.get_direction() == 'R':
                        dummy.rect.x += 1
                    else:
                        dummy.rect.x -= 1
                    if P and t.colliderect(dummy) and ground.__contains__(t):
                        P.is_colliding((t.x, t.y), (y, x))
                    elif P:
                        P.not_colliding((y, x))
                else:
                    screen.blit(tiles_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# Helper function to draw some text.
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Makes the side and lower part of the GUI visible.
def draw_debug_console():
    #  pygame.draw.rect(screen, '#E6E6FA', (W, 0, SIDE_MARGIN, H))
    pygame.draw.rect(screen, '#E6E6FA', (0, H, W + SIDE_MARGIN, LOWER_MARGIN))
    draw_text(f"level: {level}", font, 'navy', 0, H + 20)
    if P:
        draw_text(f"Player X: {P.get_location()[0]}", font, 'navy', 250, H + 15)
        draw_text(f"Player Y: {P.get_location()[1]}", font, 'navy', 1100, H + 15)
        if P.last_collider():
            draw_text(f"Collider X: {P.last_collider()[0][0]}", font, 'navy', 250, H + 40)
            draw_text(f"Collider Y: {P.last_collider()[0][1]}", font, 'navy', 675, H + 40)
            draw_text(f"Num Coll: {P.last_collider()[1]}", font, 'navy', 1100, H + 40)
        draw_text(f"Blocked Left: {P.blocked_left_right()[0]}", font, 'navy', 250, H + 65)
        draw_text(f"Blocked Right: {P.blocked_left_right()[1]}", font, 'navy', 800, H + 65)
        draw_text(f"Scroll:{scroll}", font, 'indigo', 700, H + 15)


def load_level_data():
    global scroll
    global world_data

    scroll = 0
    world_data = []
    pickle_in = open(f'./main/level_data/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)


# Draws the grid.
def draw_grid():
    for col in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (col * TILE_SIZE - scroll, 0), (col * TILE_SIZE - scroll, H))

    for row in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (W, row * TILE_SIZE))


def scroll_world_free_movement():
    global scroll_left
    global scroll_right
    change_scroll_direction()
    if P.get_direction() == 'R' and P.get_moving():
        scroll_right = True
        scroll_left = False
    elif P.get_direction() == 'L' and P.get_moving():
        scroll_left = True
        scroll_right = False
    else:
        scroll_left = False
        scroll_right = False


# display surface
W, H = 1280, 720
HW, HH = W / 2, H / 2
LOWER_MARGIN, SIDE_MARGIN = 100, 300

# pygame setup
pygame.init()
screen = pygame.display.set_mode((W + SIDE_MARGIN, H + LOWER_MARGIN))
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Outside The Fox")
FPS = 120
WHITE = (255, 255, 255, 255)

# Scroll variables.
scroll_left = False
scroll_right = False
scrolling = False
goal_scroll = 0
scroll = 0
scroll_speed = 1
reset_scroll = False

# Grid variables.
ROWS = 16
MAX_COLS = 150
TILE_SIZE = H // ROWS
TILE_TYPES = 14
level = 0
background_tiles = [2]

# Loads the tiles for the level editor.
tiles_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_colorkey((0, 0, 0))
    tiles_list.append(img)

# Init the world_data list.
world_data = []
world_coordinates = []
coordinates_filled = False
for i in range(ROWS):
    row = [-1] * MAX_COLS
    coord_row = [(0, 0)] * MAX_COLS
    world_data.append(row)
    world_coordinates.append(coord_row)

colors = ["crimson", "indigo", "navy", "violet", "slategrey", "lawngreen"]
squares = pygame.sprite.Group()
ground = pygame.sprite.Group()
ground_rect_list = [[]]
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font('assets/joystix monospace.otf', 32)
start_text = font.render('Press F1 to Start', True, green, blue)
start_rect = start_text.get_rect()
start_rect.center = (HW, HH)
paused = True
spawnCounter = 1
player_action_queue = []
# Will pause the game until F1 is pressed

bg = pygame.image.load('assets/back.png').convert_alpha()
bg = pygame.transform.scale(bg, (W, H))
md = pygame.image.load('assets/middle.png').convert_alpha()
md = pygame.transform.scale(md, (500, 450))

sprite_sheet_image = pygame.image.load('assets/player_idle.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
frame = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 500
animation_steps = [4, 6, 2, 2]
action = 0
animation_assets = ['assets/player_idle.png', 'assets/player_run.png', 'assets/player_jump.png', 'assets/player_hurt'
                                                                                                 '.png']
BLACK = (0, 0, 0)

player_animation_list = []
for x in range(len(animation_steps)):
    animation = animation_steps[x]
    sprite_sheet_image = pygame.image.load(animation_assets[x]).convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    temp_img_list = []
    for i in range(animation):
        temp_img_list.append(sprite_sheet.get_image(i, 32, 32, 3, BLACK))
    player_animation_list.append(temp_img_list)

player_run_cycle = cycle(player_animation_list[1])
player_anim = next(player_run_cycle)

start_screen = startscreen.StartScreen(pygame.time.get_ticks(), player_run_cycle, start_text, start_rect, (HW, HH))

load_level_data()
music_assets = cycle(['assets/audio/music/611440__kjartan_abel__after-the-flu.wav',
                      'assets/audio/music/647212__kjartan_abel__boschs-garden.wav',
                      'assets/audio/music/686838__zhr__desert-ambient-music.wav'])

pygame.mixer.music.load(next(music_assets))
pygame.mixer.music.stop()  # pygame.mixer.music.play()

P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
draw_world()

player_start_pos = world_coordinates[14][5]
P.setLocation(player_start_pos[0] - TILE_SIZE // 2, player_start_pos[1])

user_input = userinputfield.UserInputField("Player Editor", 24, 56, H - 56, 5)
input_validator = inputboxvalidator.InputBoxValidator(P, TILE_SIZE, W)

while True:
    # if not pygame.mixer.music.get_busy():
    #     pygame.mixer.music.load(next(music_assets))
    #     pygame.mixer.music.play()  # Uncomment for music
    pygame.mixer.music.set_volume(0.5)
    draw_bg()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events()
    if not paused and P:
        if input_validator.isDone():
            draw_grid()
        else:
            user_input.set_mouse_over(False)
            user_input.set_active(False)
        draw_world()
        if user_input.draw():
            input_validator.set_text(user_input.get_text_saved())
            input_validator.validate()
        if P.do():
            P = None

        else:
            # squares.update()
            # squares.draw(screen)
            # spawnHandler()

            # scroll_world_free_movement()  # Uncomment to scroll with Q-D movement
            for square in squares:
                if square.colliderect(P):
                    P.resetJump(square)

            if scrolling:
                scroll = pygame.math.lerp(scroll, goal_scroll, 0.05)
                if math.ceil(scroll) == math.ceil(goal_scroll) or math.floor(scroll) == math.floor(goal_scroll):
                    scrolling = False
                    scroll = goal_scroll

            if len(input_validator.get_queue()) > 0 and not P.get_lerping():
                answer = input_validator.process_queue(scroll)
                if answer:
                    draw_world()
                    goal_scroll = answer[0]
                    scrolling = answer[1]

            if P.get_reach_right_boundary():  # P.get_location()[0] >= (W - 150):
                reset_scroll = True
            if reset_scroll:
                reset_scroll = False
                scroll = scroll + W - 360
                # P.setLocation(P.get_location()[0] - 850, P.get_location()[1])
                P.reset_right_boundary()
            # print(pygame.mouse.get_pos())

    elif not P:
        start_screen.start_screen_on(pygame.time.get_ticks())
        P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
        scroll = 0
        scrolling = False
        P.setLocation(player_start_pos[0] - TILE_SIZE // 2, player_start_pos[1])
        paused = True

    else:
        start_screen.start_screen_on(pygame.time.get_ticks())
    draw_debug_console()

    pygame.display.update()
    clock.tick(FPS)
