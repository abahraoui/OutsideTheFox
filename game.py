import pickle
import sys
from itertools import cycle
from collections import OrderedDict
import pygame

from main import menu, player as player_class, code_editor, code_runner, \
    usermanual, credits as credits_class, loader as loader_class, renderer, game_manager
from main.buttons import button, music_button as music_button_class
from main.tiles import animated_tile, tile as tile_class, level_completion_door, ladder_tile

"""
This module contains the game main loop, which handles the game's events, drawing, and logic, and variables.
"""


# Event handler
def events():
    """Handles all input events in the game."""

    def __handle_editor_keys():
        if event.key == pygame.K_BACKSPACE:
            # Check if BACKSPACE is pressed
            editor.remove_text()
        elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Check if Ctrl+V is pressed
            clipboard_content = pygame.scrap.get(pygame.SCRAP_TEXT).decode()
            if len(clipboard_content) > 1:
                if clipboard_content[-1] == '\x00':
                    clipboard_content = clipboard_content[:-1]
                if clipboard_content[-1] == " ":
                    clipboard_content = clipboard_content[:-1]
                editor.paste_clipboard(clipboard_content)
                editor.start_feedback("Pasted")
        elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Check if Ctrl+C is pressed
            text = editor.get_copy_text()
            if len(text) > 0:
                pygame.scrap.put(pygame.SCRAP_TEXT, text)
                editor.start_feedback("Copied")
        elif event.key == pygame.K_LEFT:
            # Check if LEFT is pressed
            editor.increment_offset()
        elif event.key == pygame.K_RIGHT:
            # Check if RIGHT is pressed
            editor.decrement_offset()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        #     editor.increment_offset_up()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        #     editor.decrement_offset_down()
        else:
            editor.add_text(event.unicode)

    def __handle_editor_copy_rect():
        if event.type == pygame.MOUSEBUTTONDOWN and not editor.is_copy_rect() and editor.get_active():
            editor.set_copy_rect_start_pos(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION and editor.is_copy_rect() and editor:
            editor.set_copy_rect_end_pos(pygame.mouse.get_pos())
        else:
            editor.void_copy_rect_pos()

    def __handle_activating_components():
        if user_manual.mouse_colliding(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif editor.mouse_colliding(pygame.mouse.get_pos()):
            if not editor.get_active():
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            editor.set_mouse_over(True)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            editor.set_mouse_over(False)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if editor.mouse_colliding(event.pos):
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                editor.set_active(True)
            else:
                editor.set_active(False)
            if user_manual.mouse_colliding(event.pos):
                user_manual.change_state("LEVEL")
                user_manual.flip_active()

    def __handle_in_game_keys():
        if event.type == pygame.KEYDOWN:
            if user_manual.get_active() and event.key == pygame.K_RIGHT:
                user_manual.change_page("RIGHT")
            elif event.key == pygame.K_LEFT:
                user_manual.change_page("LEFT")

            if not editor.get_active():
                return
            __handle_editor_keys()

    def __handle_menu_keys():
        if event.type == pygame.KEYDOWN and (menu.get_state() == "LEVEL_SELECTION" or menu.get_state() == "HELP"):
            if event.key == pygame.K_RIGHT:
                menu.change_page("RIGHT")
            elif event.key == pygame.K_LEFT:
                menu.change_page("LEFT")

    def __handle_quitting_the_game():
        if event.type == pygame.QUIT or menu.get_quitting():  # or (event.type == KEYDOWN and event.key == K_ESCAPE):
            save_level_data(editor.get_user_answer())
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        """
        Handles keys when in menu and saving then quitting the game.
        """
        __handle_quitting_the_game()
        __handle_menu_keys()

        if not player:
            continue
        if not runner.is_done() or menu.get_paused():
            continue
        """
        If player is instantiated and the runner is done, then handle the following events.
        """
        __handle_activating_components()
        __handle_in_game_keys()
        __handle_editor_copy_rect()


def draw_world():
    """
    This function iterates over each tile in the world data and draws it at the appropriate position on the screen.
    It also handles special behavior for certain types of tiles, such as doors, problems, cherries, ladders, signs,
    and background tiles.
    """
    global coordinates_filled

    def process_door():
        global finished_level
        door = level_completion_door.Door(x * TILE_SIZE - scroll,
                                          y * TILE_SIZE, tiles_list[tile], tile)
        door.draw()
        if player and door.collide_rect(player):
            finished_level = True
            player.set_finished()

    def process_problem():
        renderer.draw_problem(x, y, tile, str(tile), problem_list, player, scroll, TILE_SIZE, tiles_list)

    def process_cherry():
        global cherry_data, score, cherry_count
        cherry_data, score, cherry_count = game_manager.process_cherry_tile(x, y, scroll, TILE_SIZE, cherry_data,
                                                                            cherry_animation_list, player, cherry_count,
                                                                            score)

    def process_ladder():
        ladder = ladder_tile.Ladder(x * TILE_SIZE - scroll, y * TILE_SIZE, tiles_list[tile], tile)
        ladder.draw()
        if player and ladder.collide_rect(player):
            player.add_ladder((y, x))
        else:
            player.remove_ladder((y, x))

    def process_sign():
        global current_problem_index, current_sign, arrow, sign_pressed
        if (y, x) not in sign_list:
            sign_list[(y, x)] = current_tile
        elif (y, x) in sign_list:
            sign_list[(y, x)] = current_tile
            p_list = list(problem_list.items())
            s_list = list(sign_list.items())

            if problem_index >= len(p_list):
                return
            current_problem_index = p_list[problem_index][0]
            current_sign = s_list[problem_index][0]
            if (not problem_list and p_list[problem_index][1][0].get_completed() and
                    sign_list[current_sign] != current_tile):
                return
            pos = pygame.mouse.get_pos()

            current_tile.draw()
            if editor.get_mode() == "Player":
                if arrow is None:
                    arrow = animated_tile.AnimatedTile(x * TILE_SIZE - scroll - 45,
                                                       y * TILE_SIZE - 125,
                                                       arrow_animation_list, arrow_animation_list[0], "arrow")
            elif editor.get_mode() == "Problem":
                arrow = None
            if current_tile.get_rect().collidepoint(pos):
                sign_pressed = True
                game_manager.start_problem(p_list, problem_index, runner, editor)
            elif p_list[problem_index][1][0] is not None:
                sign_pressed = False
                p_list[problem_index][1][0].set_hovering(False)

    def process_colliding_tiles():
        current_tile.draw()
        if player and current_tile.collide_rect(player):
            player.is_colliding((current_tile.x, current_tile.y), (y, x))
        elif player:
            player.not_colliding((y, x))

    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):

            if tile < 0:
                continue

            if world_coordinates[y][x] == (0, 0) and not coordinates_filled:
                world_coordinates[y][x] = (x * TILE_SIZE, y * TILE_SIZE)
                if (x, y) == (MAX_COLS - 1, ROWS - 1):
                    coordinates_filled = True

            current_tile = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, tiles_list[tile], tile)

            if tile == 14:  # Level completion door
                process_door()

            elif tile in [8, 23, 24]:  # Problem tiles
                process_problem()

            elif tile == 21:  # Cherry tile
                process_cherry()

            elif tile == 9:  # Ladder tile
                process_ladder()

            elif tile == 22:  # Sign tile
                process_sign()

            elif tile not in background_tiles:  # All other tiles not in the background
                process_colliding_tiles()

            else:  # Background tiles
                screen.blit(tiles_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


def draw_hud():
    global loaded_game_level
    renderer.draw_hud(screen, user_manual, level, FONT,
                      cherry_animation_list, cherry_count, music_button, level_button, menu, run_tries,
                      max_level)

    if pause_button.draw(screen):
        editor.set_mode("Player")
        menu.set_state("MENU")
        menu.set_paused()
        loaded_game_level = False
        load_level_data(True, False)
        user_manual.reset_page()


def load_level_data(going_to_menu=False, restart=False):
    """
    Loads the level data using the loader file, it loads relevant level and hint text, world data, and variables.
    10 is the menu level. Can be changed.
    """
    global world_data, coordinates_filled, world_coordinates, cherry_data, problem_list, sign_list, \
        current_problem_index, current_sign, problem_index, max_level

    problem_list, sign_list, current_problem_index, current_sign, \
        problem_index, cherry_data, coordinates_filled = loader_class.reset_variables()

    world_coordinates, world_data = loader_class.load_world_coordinates(ROWS, MAX_COLS)

    loaded_level = level
    if going_to_menu:
        loaded_level = "menu"
    else:
        max_level = loader_class.load_level_txt_files(restart, level, loaded_level, editor, user_manual,
                                                      FINAL_LEVEL, max_level)

    with open(f'./main/level_data/level{loaded_level}_data', 'rb') as pickle_in:
        world_data = pickle.load(pickle_in)


def save_level_data(text):
    """
    Saves the level data, user's code, and score to the appropriate files.
    """
    file = open(f'main/level_data/level_code/level{level}_text.txt', 'w')
    for word in text:
        file.write(word + " ")
    file.close()

    if level < 9:
        with open('main/level_data/max_level.txt', 'r') as file:
            current_max_level = int(file.readline())
        if current_max_level < max_level:
            with open('main/level_data/max_level.txt', 'w') as file:
                file.write(str(max_level))
            file.close()

        with open(f'main/level_data/level_score/level{level}_score.txt', 'r') as file:
            current_score = int(file.readline())
        if current_score < score:
            with open(f'main/level_data/level_score/level{level}_score.txt', 'w') as file:
                file.write(str(score))
            file.close()


def prepare_level_change():
    save_level_data(editor.get_user_answer())
    user_manual.reset_page()
    user_manual.set_active(True)


def reset_score():
    """
    This function resets the score, run tries, cherry count, arrow; using the game manager's reset_level function.
    """
    global score, run_tries, cherry_count, arrow
    score, run_tries, cherry_count, arrow = game_manager.reset_score()


def reset_level():
    """
    This function resets the scroll, scrolling, goal scroll, runner, and player; and initialises them to level's relevant values using the game manager's reset_level function.
    """
    global scroll, scrolling, goal_scroll, player, runner

    scroll, scrolling, goal_scroll, runner, player = game_manager.reset_level(
        editor, player_animation_list, player_start_pos, W, H, TILE_SIZE)


def reset_score_level():
    reset_score()
    reset_level()


def finishing_level():
    """
    This function clears the editor text, plays the victory sound, prepares for a level change, increments the level, loads the level data, sets the level wanted, and resets the score and the level.
    """
    global level
    editor.clear_text()
    victory_sound = pygame.mixer.Sound("assets/audio/sounds/342751__rhodesmas__coins-purchase-3.wav")
    victory_sound.play()
    victory_sound.set_volume(1)
    prepare_level_change()
    level += 1
    load_level_data(False, False)
    menu.set_level_wanted(level)
    reset_score_level()


def roll_credits(credits_player):
    """
    This function rolls the credits by doing the appropriate actions when the credits are reached.
    """
    global scroll, level, credits_reached, player
    credits_screen.draw()
    credits_player.moving = True
    credits_player.climbing = False
    credits_player.crouching = False
    credits_player.jumping = False
    editor.clear_text()
    game_manager.deactivate_editor(editor)
    if not credits_screen.get_done():
        scroll += 0.3
    else:
        """This moves the player to the right of the screen when the credits are done."""
        credits_player.x += 3
    if credits_player.x > W + SIDE_MARGIN + 100:
        """This ends the credits when the player goes outside the screen."""
        player = None
        menu.set_state("MENU")
        scroll = 0
        level = 0
        load_level_data(True, False)
        menu.set_paused()
        credits_reached = False


if __name__ == '__main__':
    """
    The entry point of the game.

    This script initializes the game, sets up the game window, loads all the game assets, and runs the game loop.

    Needed variables are initialised as global variables. This module makes classes communicate with each other, and uses them to create wanted behavior.

    The game loop runs continuously until the game is closed. It draws the game world, processes game events, updates the game state, renders the game screen, and more.
    """
    # Display variables
    W, H = 1280, 720  # 1300, 900
    HW, HH = W / 2, H / 2
    LOWER_MARGIN, SIDE_MARGIN = 100, 300

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(
        (W + SIDE_MARGIN, H))  # + LOWER_MARGIN))  # Add 'LOWER_MARGIN' to H to see console when drawing it.
    pygame.scrap.init()
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
    TILE_TYPES = 26

    # Game variables.
    level = 0
    max_level = 0
    FINAL_LEVEL = 8
    run_tries = 0
    finished_level = False
    score = 0
    cherry_count = 0
    background_tiles = [2, 15, 16, 17, 18, 19, 20, 22, 25]
    problem_list = OrderedDict()
    sign_list = OrderedDict()
    sign_pressed = False
    current_problem_index = 0
    current_sign = 0
    problem_index = 0

    # Similar informative variables with a few differences.
    manual_text = loader_class.read_file("assets/txt_files/manual.txt")
    help_manual_text = loader_class.read_file("assets/txt_files/help_manual.txt")

    # Loads the tiles for the level editor.
    tiles_list = loader_class.load_tiles(TILE_TYPES, TILE_SIZE)

    '''Init the world and game variables.'''
    world_data = []
    cherry_data = {}
    world_coordinates = []
    coordinates_filled = False

    editor = code_editor.TextEditor("Player Editor", 24, 56, H - 56, 9)

    load_level_data(True, False)

    GREEN = (0, 255, 0)
    BLUE = (0, 0, 128)
    FONT = pygame.font.Font('assets/joystix monospace.otf', 32)
    start_text = FONT.render('Press F1 to Start', True, GREEN, BLUE)
    start_rect = start_text.get_rect()
    start_rect.center = (HW, HH)

    background, middle_ground = loader_class.load_background(W, H)
    last_update = pygame.time.get_ticks()
    cherry_animation_list = loader_class.load_sprite_animation('assets/cherry_anim.png', 21, 2, "black", 5)

    arrow_animation_list = loader_class.load_sprite_animation('assets/arrow_sheet.png', 32, 4, "white", 4)

    player_animation_list = loader_class.load_player_animation_list()

    icon = pygame.transform.scale(player_animation_list[0][0], (24, 24))
    pygame.display.set_icon(icon)

    player_run_cycle = cycle(player_animation_list[1])

    menu = menu.Menu(pygame.time.get_ticks(), player_run_cycle, start_text, start_rect,
                     (W + SIDE_MARGIN, H), help_manual_text, FINAL_LEVEL)
    menu.set_max_level_unlocked(max_level)
    menu.set_level_wanted(level)

    off, on, level_icon, music_assets = loader_class.load_hud_assets()

    pygame.mixer.music.load(next(music_assets))
    pygame.mixer.music.stop()

    player = player_class.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
    draw_world()

    player_start_pos = world_coordinates[14][5]
    player.set_location(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])

    runner = code_runner.Runner(player)
    runner.subscribe(editor)
    user_manual = usermanual.UserManual(980, 0, manual_text)

    music_button = music_button_class.MusicButton(50, 225, on, off, 2, "red", "blue", music_assets, on)
    pygame.mixer.music.play()  # Uncomment for music
    pygame.mixer.music.set_volume(0.03)

    level_button = button.Button(5, 235, level_icon, 1.5, "lightgreen", (0, 0, 128))

    menu_text = FONT.render('Menu', True, "white")
    pause_button = button.Button(5, 180, menu_text, 1, "lightgreen", (0, 0, 128))

    arrow = None

    restart_text = FONT.render('Restart', True, "white")
    restart_button = button.Button(5, 125, restart_text, 1, "lightgreen", (0, 0, 128))

    credits_screen = credits_class.Credits(W, H)
    credits_reached = False
    loaded_game_level = False

    # Game loop
    while True:
        renderer.draw_background(screen, background, middle_ground, scroll)
        events()
        # Handles starting the game and changing levels.
        if not menu.get_paused() and player:
            if not loaded_game_level:
                load_level_data(False, False)
                reset_score_level()
                loaded_game_level = True
            if menu.get_level_wanted() != level:
                prepare_level_change()
                level = menu.get_level_wanted()
                load_level_data(False, False)
                editor.set_error_processed()
                reset_score_level()

            # Handles the game's problem system.
            draw_world()
            if runner.is_done():
                if runner.get_mode() != "Player" and runner.get_problem_try() is not None and not \
                        problem_list[current_problem_index][0].get_show_feedback():
                    game_manager.attempt_problem(problem_list, current_problem_index, runner)
                if runner.get_problem_completed():
                    problem_index = game_manager.completed_problem(problem_index, runner, editor)
                if not credits_reached:
                    renderer.draw_grid(screen, player, TILE_SIZE, MAX_COLS, scroll)
                if arrow is not None:
                    arrow.draw()
            # Starts the execution process.
            if editor.draw():
                run_tries, score = game_manager.run_editor(runner, run_tries, score, editor)
            if player.do():
                player = None
            elif credits_reached:
                roll_credits(player)
            else:
                draw_hud()
                scroll, scrolling, goal_scroll = game_manager.process_scrolling(
                    runner, player, TILE_SIZE, scroll, scrolling, goal_scroll)
                # print(pygame.mouse.get_pos()) # Uncomment to debug mouse position
                if restart_button.draw(screen):
                    player = None
                    load_level_data(False, True)
                    score, run_tries, cherry_count, arrow = game_manager.reset_score()

        elif player is None and not finished_level:
            reset_level()
            runner.say("Oh no that got me let's try over!")

        elif finished_level:
            finished_level = False
            if level == FINAL_LEVEL:
                # If final level beaten, here the eight one, then roll credits.
                credits_reached = True
                finishing_level()
                loader_class.load_credits_music()
            else:
                # Finishing a level
                max_level += 1
                menu.set_end_text(f"Well done on finishing the level, your score was: {score}!")
                finishing_level()
                menu.set_state("END_SCREEN")
                menu.set_paused()
        else:
            draw_world()
            menu.draw(pygame.time.get_ticks())

        '''Uncomment to see debug console after adding 'LOWER_MARGIN' to 'H' to see console when drawing it.'''
        # renderer.draw_debug_console(screen, player, H, W, SIDE_MARGIN, LOWER_MARGIN, FONT, level, scroll)
        pygame.display.update()
        clock.tick(FPS)
