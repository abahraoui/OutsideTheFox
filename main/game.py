import math
import pickle
import sys
from itertools import cycle
import startscreen

import pygame
import player
import tile as tile_class
from pygame.locals import *
import spritesheet
import userinputfield
import inputboxvalidator
import usermanual
import cherry_tile
import music_button as music_button_class
import button
import bridge as bridge_class
from collections import OrderedDict


# Event handler
def events():
    global paused, scroll, goal_scroll, scrolling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            save_level_data(user_input.get_text_saved())
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
            if input_validator.isDone() and not start_screen.get_paused():

                if user_manual.mouse_colliding(pygame.mouse.get_pos()):
                    # if not user_manual.get_active():
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

                elif user_input.mouse_colliding(pygame.mouse.get_pos()):
                    if not user_input.get_active():
                        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    user_input.set_mouse_over(True)
                    user_input.color = "red"
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    user_input.set_mouse_over(False)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_input.mouse_colliding(event.pos):
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                        user_input.set_active(True)
                    else:
                        user_input.set_active(False)
                    if user_manual.mouse_colliding(event.pos):
                        user_manual.change_state("M")
                        user_manual.flip_active()
                    if sign_pressed:
                        user_manual.change_state("L")
                        user_manual.flip_active()

                if event.type == pygame.KEYDOWN and user_input.get_active():
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
                        user_input.remove_text()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Check if Ctrl+V is pressed
                        clipboard_content = pygame.scrap.get(pygame.SCRAP_TEXT).decode()
                        if len(clipboard_content) > 1:
                            if clipboard_content[-1] == '\x00':
                                clipboard_content = clipboard_content[:-1]
                            if clipboard_content[-1] == " ":
                                clipboard_content = clipboard_content[:-1]
                            user_input.paste_clipboard(clipboard_content)
                            user_input.start_feedback("Pasted")
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        text = user_input.get_copy_text()
                        if len(text) > 0:
                            pygame.scrap.put(pygame.SCRAP_TEXT, text)
                            user_input.start_feedback("Copied")
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        user_input.increment_offset()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        user_input.decrement_offset()
                    else:
                        user_input.add_text(event.unicode)
                elif event.type == pygame.MOUSEBUTTONDOWN and not user_input.is_copy_rect() and user_input.get_active():
                    user_input.set_copy_rect_start_pos(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEMOTION and user_input.is_copy_rect() and user_input:
                    user_input.set_copy_rect_end_pos(pygame.mouse.get_pos())
                else:
                    user_input.void_copy_rect_pos()


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
    global coordinates_filled, score, finished_level, current_bridge_problem, current_sign, arrow, sign_pressed, cherry_count
    ground.empty()
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):

            if world_coordinates[y][x] == (0, 0) and not coordinates_filled:
                world_coordinates[y][x] = (x * TILE_SIZE, y * TILE_SIZE)
                if (x, y) == (149, 15):
                    coordinates_filled = True
            if tile >= 0:
                t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (W, H), tiles_list[tile], tile)

                if tile == 14:
                    t.draw()
                    # pygame.draw.rect(screen, "blue", (x * TILE_SIZE - scroll, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
                    if P and t.colliderect(P):
                        finished_level = True
                        P.set_finished()
                elif tile == 21:
                    if (y, x) not in cherry_data:
                        cherry = cherry_tile.Cherry(x * TILE_SIZE - scroll, y * TILE_SIZE, cherry_animation_list,
                                                    (y, x))
                        cherry_data[(y, x)] = cherry
                    elif cherry_data[(y, x)] != "Removed":
                        cherry_data[(y, x)].set_location((x * TILE_SIZE - scroll, y * TILE_SIZE))
                    if cherry_data[(y, x)] != "Removed":
                        cherry_data[(y, x)].draw()
                        if P and cherry_data[(y, x)].colliderect(P):
                            jump_sound = pygame.mixer.Sound("assets/audio/sounds/348112__matrixxx__crunch.wav")
                            jump_sound.play()
                            jump_sound.set_volume(1)
                            cherry_data[(y, x)] = "Removed"
                            score += 50
                            cherry_count += 1
                elif tile == 22:
                    if (y, x) not in sign_list:
                        sign_list[(y, x)] = t
                    elif (y, x) in sign_list:
                        sign_list[(y, x)] = t
                        b_list = list(bridge_list.items())
                        s_list = list(sign_list.items())
                        if problem_index < len(b_list) and b_list[problem_index][1][0] is not None:
                            current_bridge_problem = b_list[problem_index][0]
                            current_sign = s_list[problem_index][0]
                            if bridge_list and not b_list[problem_index][1][0].completed and sign_list[current_sign] == t:
                                pos = pygame.mouse.get_pos()
                                t.draw()
                                if user_input.get_mode() == "Player":
                                    if arrow is None:
                                        arrow = cherry_tile.Cherry(x * TILE_SIZE - scroll - 45, y * TILE_SIZE - 125, arrow_animation_list,
                                                               "arrow")
                                elif user_input.get_mode() == "Problem":
                                    arrow = None
                                if t.get_rect().collidepoint(pos):
                                    sign_pressed = True
                                    b_list[problem_index][1][0].set_hovering(True)
                                    if pygame.mouse.get_pressed()[0] == 1:
                                        match b_list[problem_index][1][0].id:
                                            case 8:
                                                input_validator.set_mode("Bridge")
                                                input_validator.set_problem_size(b_list[problem_index][1][0].get_problem_size())
                                            case 23:
                                                input_validator.set_mode("Ladder")
                                                input_validator.set_problem_size(b_list[problem_index][1][0].get_problem_size())
                                            case 24:
                                                input_validator.set_mode("Spike")
                                                input_validator.set_problem_size(b_list[problem_index][1][0].get_problem_size())

                                        user_input.set_mode("Problem")
                                else:
                                    sign_pressed = False
                                    b_list[problem_index][1][0].set_hovering(False)

                elif tile == 8:
                    if "8" not in bridge_list:
                        bridge_list["8"] = None, {}
                    if (y, x) not in bridge_list["8"][1]:
                        bridge_list["8"][1][(y, x)] = tile
                    elif (y, x) in bridge_list["8"][1]:
                        bridge_list["8"][1][(y, x)] = tile
                        if len(bridge_list["8"][1]) > 0 and bridge_list["8"][0] is None:
                            bridge = bridge_class.Bridge(W, H, bridge_list["8"][1], False, TILE_SIZE, 8, bridge_list["8"][1])
                            bridge_list["8"] = bridge, bridge_list["8"][1]
                        if "8" in bridge_list and len(bridge_list["8"][1]) > 0:
                            bridge_list["8"][0].draw(P, scroll, TILE_SIZE, tiles_list)
                elif tile == 23:
                    if "23" not in bridge_list:
                        bridge_list["23"] = None, {}
                    if (y, x) not in bridge_list["23"][1]:
                        bridge_list["23"][1][(y, x)] = tile
                    elif (y, x) in bridge_list["23"][1]:
                        bridge_list["23"][1][(y, x)] = tile
                        if len(bridge_list["23"][1]) > 0 and bridge_list["23"][0] is None:
                            bridge = bridge_class.Bridge(W, H, bridge_list["23"][1], False, TILE_SIZE, 23, bridge_list["23"][1])
                            bridge_list["23"] = bridge, bridge_list["23"][1]
                        if "23" in bridge_list and len(bridge_list["23"][1]) > 0:
                            bridge_list["23"][0].draw(P, scroll, TILE_SIZE, tiles_list)
                elif tile == 24:
                    if "24" not in bridge_list:
                        bridge_list["24"] = None, {}
                    if (y, x) not in bridge_list["24"][1]:
                        bridge_list["24"][1][(y, x)] = tile
                    elif (y, x) in bridge_list["24"][1]:
                        bridge_list["24"][1][(y, x)] = tile
                        if len(bridge_list["24"][1]) > 0 and bridge_list["24"][0] is None:
                            bridge = bridge_class.Bridge(W, H, bridge_list["24"][1], False, TILE_SIZE, 24, bridge_list["24"][1])
                            bridge_list["24"] = bridge, bridge_list["24"][1]
                        if "24" in bridge_list and len(bridge_list["24"][1]) > 0:
                            bridge_list["24"][0].draw(P, scroll, TILE_SIZE, tiles_list)
                elif tile == 9:
                    t.draw()
                    if P and t.colliderect(P):
                        P.add_ladder((y, x))
                    else:
                        P.remove_ladder((y, x))

                elif tile not in background_tiles:
                    t.draw()
                    if P and t.colliderect(P):
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
        # if P.last_collider():
        #     draw_text(f"Collider X: {P.last_collider()[0][0]}", font, 'navy', 250, H + 40)
        #     draw_text(f"Collider Y: {P.last_collider()[0][1]}", font, 'navy', 675, H + 40)
        #     draw_text(f"Num Coll: {P.last_collider()[1]}", font, 'navy', 1100, H + 40)
        draw_text(f"Blocked Above: {P.get_blocked_above()}", font, 'navy', 250, H + 40)
        draw_text(f"Blocked Below: {P.get_blocked_below()}", font, 'navy', 800, H + 40)
        draw_text(f"Blocked Left: {P.blocked_left_right()[0]}", font, 'navy', 250, H + 65)
        draw_text(f"Blocked Right: {P.blocked_left_right()[1]}", font, 'navy', 800, H + 65)
        draw_text(f"Scroll:{scroll}", font, 'indigo', 700, H + 15)


def load_level_data(menu=False):
    global scroll, world_data, coordinates_filled, world_coordinates, cherry_data, level, bridge_list, sign_list, \
        current_bridge_problem, current_bridge_problem, current_sign,problem_index
    bridge_list = OrderedDict()
    sign_list = OrderedDict()
    current_bridge_problem = 0
    current_sign = 0
    problem_index = 0
    cherry_data = {}
    coordinates_filled = False
    world_data = []
    world_coordinates = []

    for i in range(ROWS):
        row = [-1] * MAX_COLS
        coord_row = [(0, 0)] * MAX_COLS
        world_data.append(row)
        world_coordinates.append(coord_row)
    loaded_level = level
    scroll = 0
    if menu:
        loaded_level = 10
    else:
        with open(f'main/level_data/level_code/level{level}_text.txt', 'r') as file:
            lines = file.readlines()
            final_text = ""
            for line in lines:
                text = line.__str__()
                final_text += text + " "
            final_text = final_text[:-2]
            user_input.set_user_text(final_text)
    pickle_in = open(f'./main/level_data/level{loaded_level}_data', 'rb')
    world_data = pickle.load(pickle_in)


def save_level_data(text):
    file = open(f'main/level_data/level_code/level{level}_text.txt', 'w')
    for t in text:
        file.write(t + " ")
    file.close()


# Draws the grid.
def draw_grid():
    #
    # for col in range(MAX_COLS + 1):
    #     pygame.draw.line(screen, WHITE, (col * TILE_SIZE - scroll, 0), (col * TILE_SIZE - scroll, H))
    #
    # for row in range(MAX_COLS + 1):
    #     pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (W, row * TILE_SIZE))

    # draws cols
    for col in range(MAX_COLS + 1):
        x = col * TILE_SIZE - scroll
        y = col * TILE_SIZE
        rounded_p_x = P.get_location()[0] + scroll + TILE_SIZE / 2
        if P.get_location()[0] + TILE_SIZE * 5 >= x >= P.get_location()[0] - TILE_SIZE * 5:
            rounded_p_y = P.get_location()[1] - P.get_location()[1] % TILE_SIZE  # Is the rounded up perfect tile y.
            offset_y = col * TILE_SIZE
            if offset_y >= rounded_p_x:
                offset_y = offset_y - 2 * (offset_y - rounded_p_x) - TILE_SIZE

            pygame.draw.line(screen, WHITE, (x, rounded_p_y + (offset_y) - (rounded_p_x - 225) + TILE_SIZE),
                             (x, rounded_p_y - offset_y + (rounded_p_x - 225)))
    # draws rows
    for row in range(MAX_COLS + 1):
        y = row * TILE_SIZE
        rounded_p_y = P.get_location()[1] - P.get_location()[1] % TILE_SIZE
        if P.get_location()[1] + TILE_SIZE * 5 >= y >= P.get_location()[1] - TILE_SIZE * 5:
            rounded_p_x = P.get_location()[0]
            offset_x = (rounded_p_x - rounded_p_x % TILE_SIZE) - abs(row * TILE_SIZE - rounded_p_y) + 5 * TILE_SIZE
            if rounded_p_y < y:
                offset_x += TILE_SIZE
            if not (rounded_p_x / TILE_SIZE).is_integer():
                offset_x += TILE_SIZE / 2
            offset_x = offset_x - (offset_x % TILE_SIZE)
            if scroll != int(scroll):
                offset_x -= 22.5
            start_x = rounded_p_x - (offset_x - rounded_p_x)
            pygame.draw.line(screen, WHITE, (start_x, y), (offset_x, y))


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
pygame.scrap.init()
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
TILE_TYPES = 25
level = 0
max_level = 5
run_tries = 0
finished_level = False
score = 0
cherry_count = 0
background_tiles = [2, 15, 16, 17, 18, 19, 20, 22]
bridge_list = OrderedDict()
sign_list = OrderedDict()
sign_pressed = False
current_bridge_problem = 0
current_sign = 0
problem_index = 0

with open("assets/txt_files/manual.txt") as file:
    manual_text = ""
    for line in file.readlines():
        manual_text += line.__str__()


# Loads the tiles for the level editor.
tiles_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'assets/tile/{x}.png').convert_alpha()
    if x == 14:
        img = pygame.transform.scale(img, (TILE_SIZE, 2 * TILE_SIZE))
    elif x in [17]:
        img = pygame.transform.scale(img, (5 * TILE_SIZE, 5 * TILE_SIZE))
    elif x in [18, 15, 16]:
        img = pygame.transform.scale(img, (4 * TILE_SIZE, 4 * TILE_SIZE))
    elif x in [19]:
        img = pygame.transform.scale(img, (3 * TILE_SIZE, 3 * TILE_SIZE))
    elif x in []:
        img = pygame.transform.scale(img, (2 * TILE_SIZE, 2 * TILE_SIZE))
    elif x == 13:
        img = pygame.transform.scale(img, (TILE_SIZE, 0.5 * TILE_SIZE))
    else:
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_colorkey((0, 0, 0))
    tiles_list.append(img)

# Init the world_data list.
world_data = []
cherry_data = {}
world_coordinates = []
coordinates_filled = False

user_input = userinputfield.UserInputField("Player Editor", 24, 56, H - 56, 9)

load_level_data(True)

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
BLACK = (0, 0, 0)
frame = 0
last_update = pygame.time.get_ticks()
cherry_animation_list = []

sprite_sheet_image = pygame.image.load('assets/cherry_anim.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
temp_img = None
for i in range(5):
    temp_img = sprite_sheet.get_image(i, 21, 21, 2, BLACK)
    cherry_animation_list.append(temp_img)

arrow_animation_list = []

sprite_sheet_image = pygame.image.load('assets/arrow_sheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
temp_img = None
for i in range(4):
    temp_img = sprite_sheet.get_image(i, 32, 32, 4, WHITE)
    arrow_animation_list.append(temp_img)

animation_cooldown = 500
animation_steps = [4, 6, 2, 2, 2, 4]
action = 0
animation_assets = ['assets/player_idle.png', 'assets/player_run.png', 'assets/player_jump.png', 'assets/player_hurt'
                                                                                                 '.png',
                    'assets/player_crouch.png', 'assets/player_climb.png']

player_animation_list = []
for x in range(len(animation_steps)):
    animation = animation_steps[x]
    sprite_sheet_image = pygame.image.load(animation_assets[x]).convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    temp_img_list = []
    for i in range(animation):
        temp_img_list.append(sprite_sheet.get_image(i, 32, 32, 3, BLACK))
    player_animation_list.append(temp_img_list)

pygame.display.set_icon(player_animation_list[1][0])

player_run_cycle = cycle(player_animation_list[1])
player_anim = next(player_run_cycle)

start_screen = startscreen.StartScreen(pygame.time.get_ticks(), player_run_cycle, start_text, start_rect,
                                       (W + SIDE_MARGIN, H), manual_text, "")
start_screen.set_max_level_unlocked(max_level)
start_screen.set_level_wanted(level)

music_assets = cycle(['assets/audio/music/611440__kjartan_abel__after-the-flu.wav',
                      'assets/audio/music/647212__kjartan_abel__boschs-garden.wav',
                      'assets/audio/music/686838__zhr__desert-ambient-music.wav'])

pygame.mixer.music.load(next(music_assets))
pygame.mixer.music.stop()  # pygame.mixer.music.play()

P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
draw_world()

player_start_pos = world_coordinates[14][5]
P.setLocation(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])

input_validator = inputboxvalidator.InputBoxValidator(P, TILE_SIZE, W, user_input.get_feedback_rect())
user_manual = usermanual.UserManual(980, 0, manual_text, "In this level, you have to reach the end!",
                                    "Try using 'fox.moveRight()' and 'fox.jump()' if you find yourself blocked by an obstacle!\n")

off = pygame.image.load("assets/music_off.png").convert_alpha()
on = pygame.image.load("assets/music_on.png").convert_alpha()
on.set_colorkey("black")

music_button = music_button_class.MusicButton(105, 170, on, off, 2, "red", "blue", music_assets)
pygame.mixer.music.play()  # Uncomment for music
pygame.mixer.music.set_volume(0.03)

level_icon = pygame.image.load("assets/level_icon.png").convert_alpha()
level_button = button.Button(5, 180, level_icon, 1.5, "lightgreen", (0, 0, 128))

pause_icon = pygame.image.load("assets/pause_icon.png").convert_alpha()
pause_button = button.Button(60, 180, pause_icon, 1.5, "lightgreen", (0, 0, 128))

arrow = None
restart_text = font.render('Restart', True, "white")
restart_button = button.Button(5, 125, restart_text, 1, "lightgreen", (0, 0, 128))

bridge = None

loaded_game_level = False
while True:
    draw_bg()
    events()
    if not start_screen.get_paused() and P:
        if not loaded_game_level:
            load_level_data()
            loaded_game_level = True
        if start_screen.get_level_wanted() != level:
            save_level_data(user_input.get_text_saved())
            level = start_screen.get_level_wanted()
            load_level_data()
            score = 0
            run_tries = 0
            cherry_count = 0
            user_input.set_error_processed()
            user_input.set_mode("Player")
            P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
            scroll = 0
            scrolling = False
            goal_scroll = 0
            P.setLocation(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])
            input_validator = inputboxvalidator.InputBoxValidator(P, TILE_SIZE, W, user_input.get_feedback_rect())
        draw_world()
        if input_validator.isDone():
            if input_validator.get_mode() != "Player" and input_validator.get_problem_try() is not None and not bridge_list[current_bridge_problem][0].get_show_feedback():
                bridge_list[current_bridge_problem][0].set_problem_try(input_validator.get_problem_try())
                input_validator.set_problem_try(None)
            if input_validator.get_problem_completed():
                bridge_list[current_bridge_problem][0].validate_problem()
                problem_index += 1
                input_validator.set_mode("Player")
                input_validator.say("Well done !")
                user_input.set_mode("Player")

                input_validator.set_problem_completed(False)
            draw_grid()
            if arrow is not None:
                arrow.draw()
        else:
            user_input.set_mouse_over(False)
            user_input.set_active(False)
        if user_input.draw():
            input_validator.set_text(user_input.get_text_saved())
            input_validator.validate()
            run_tries += 1
            score -= 10
        if input_validator.get_error_feedback():
            input_validator.draw_error_feedback()
        if input_validator.has_error() and not user_input.get_error_processed():
            user_input.set_error_line(input_validator.get_error_line())

        if P.do():
            P = None

        else:
            user_manual.draw()
            if input_validator.show_feedback:
                input_validator.draw_fox_feedback()
            # input_validator.draw_fox_feedback()
            draw_text(f"Level: {level}", font, (0, 0, 128), 5, 0)
            screen.blit(cherry_animation_list[0], (5, 60))
            draw_text(f"  {cherry_count}", font, (0, 0, 128), 5, 60)
            draw_text(f"Tries: {run_tries}", font, (0, 0, 128), 250, 0)

            # draw_text("Music:", font, (0, 0, 128), 5, 125)
            music_button.draw(screen)
            if level_button.draw(screen):
                start_screen.set_state("L")
                start_screen.start_screen_on(pygame.time.get_ticks())
                start_screen.set_level_wanted(level)
                start_screen.set_max_level_unlocked(max_level)
                start_screen.set_paused()

            if pause_button.draw(screen):
                user_input.set_mode("Player")
                start_screen.set_state("M")
                start_screen.start_screen_on(pygame.time.get_ticks())
                start_screen.set_paused()
                loaded_game_level = False
                load_level_data(True)
            # scroll_world_free_movement()  # Uncomment to scroll with Q-D movement

            if scrolling:
                scroll = pygame.math.lerp(scroll, goal_scroll, 0.05)
                if math.ceil(scroll) == math.ceil(goal_scroll) or math.floor(scroll) == math.floor(goal_scroll):
                    scrolling = False
                    scroll = goal_scroll

            if len(input_validator.get_queue()) > 0 and not P.get_lerping():
                answer = input_validator.process_queue(scroll)
                if answer:
                    # draw_world()
                    goal_scroll += answer[0] * TILE_SIZE / 2
                    scrolling = answer[1]

            if P.get_reach_right_boundary():  # P.get_location()[0] >= (W - 150):
                reset_scroll = True
            if reset_scroll:
                reset_scroll = False
                scroll = scroll + W - 360
                # P.setLocation(P.get_location()[0] - 850, P.get_location()[1])
                P.reset_right_boundary()
            # print(pygame.mouse.get_pos())
            if restart_button.draw(screen):
                P = None
                load_level_data()
                score = 0
                run_tries = 0
                cherry_count = 0

    elif P is None and not finished_level:
        # start_screen.start_screen_on(pygame.time.get_ticks())
        # start_screen.set_paused()
        P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
        user_input.set_mode("Player")
        scroll = 0
        scrolling = False
        goal_scroll = 0
        P.setLocation(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])
        input_validator = inputboxvalidator.InputBoxValidator(P, TILE_SIZE, W, user_input.get_feedback_rect())
        input_validator.say("Oh no that got me let's try over!")

    elif finished_level:
        finished_level = False
        if level > 5:
            pygame.quit()
            sys.exit()
        P = player.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
        save_level_data(user_input.get_text_saved())
        user_input.clear_text()
        user_input.increment_line_limit()
        level += 1
        start_screen.set_level_wanted(level)
        load_level_data()
        scroll = 0
        scrolling = False
        goal_scroll = 0
        P.setLocation(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])
        input_validator = inputboxvalidator.InputBoxValidator(P, TILE_SIZE, W, user_input.get_feedback_rect())
        user_input.set_mode("Player")
        start_screen.set_end_text(f"Well done on finishing the level, your score was: {score}!")
        score = 0
        run_tries = 0
        cherry_count = 0
        start_screen.set_state("E")
        start_screen.start_screen_on(pygame.time.get_ticks())
        start_screen.set_paused()

    else:
        draw_world()
        start_screen.start_screen_on(pygame.time.get_ticks())
    draw_debug_console()

    pygame.display.update()
    clock.tick(FPS)
