import pygame
from main.problems import bridge_problem, ladder_problem, spike_problem

"""
This module contains drawing functions used in the game file.
"""


def draw_text(text, text_font, text_col, x, y, screen):
    """
    Renders the given text on the screen at the specified location.

    Parameters:
    ----------
    text : str
    text_font : pygame.font.Font
    text_col : tuple
    x : int
    y : int
    screen : pygame.Surface
    """
    image = text_font.render(text, True, text_col)
    screen.blit(image, (x, y))


def draw_debug_console(screen, player, height, width, side_margin, lower_margin, font, level, scroll):
    """
    Draws a debug console on the screen with information about the player's position and blockage status.

    Parameters
    ----------
    screen : pygame.Surface
    player : Player
    height : int
        The height of the game screen.
    width : int
        The width of the game screen.
    side_margin : int
        The side margin of the game screen.
    lower_margin : int
        The lower margin of the game screen.
    font : pygame.font.Font
    level : int
    scroll : float or int
        The current scroll position of the game screen.
    """
    pygame.draw.rect(screen, '#E6E6FA', (0, height, width + side_margin, lower_margin))
    draw_text(f"level: {level}", font, 'navy', 0, height + 20, screen)
    if player:
        draw_text(f"Player X: {player.get_location()[0]}", font, 'navy', 250, height + 15, screen)
        draw_text(f"Player Y: {player.get_location()[1]}", font, 'navy', 1100, height + 15, screen)
        draw_text(f"Blocked Above: {player.get_blocked_above()}", font, 'navy', 250, height + 40, screen)
        draw_text(f"Blocked Below: {player.get_blocked_below()}", font, 'navy', 800, height + 40, screen)
        draw_text(f"Blocked Left: {player.get_blocked_left()}", font, 'navy', 250, height + 65, screen)
        draw_text(f"Blocked Right: {player.get_blocked_right()}", font, 'navy', 800, height + 65, screen)
        draw_text(f"Scroll:{scroll}", font, 'indigo', 700, height + 15, screen)


def draw_hud(screen, user_manual, level, font,
             cherry_animation_list, cherry_count, music_button, level_button, menu, run_tries, max_level):
    """
    Draws the game's heads-up display (HUD), including the level, cherry count, run tries, and buttons for music volume handling and level selection.

    Parameters
    ----------
    screen : pygame.Surface
    user_manual : UserManual
    level : int
    font : pygame.font.Font
    cherry_animation_list : list
        The list of cherry animations.
    cherry_count : int
        The current count of cherries.
    music_button : Button
    level_button : Button
        The button to control the game level.
    menu : Menu
        The game menu.
    run_tries : int
    max_level : int
    """
    user_manual.draw()
    draw_text(f"Level: {level}", font, (0, 0, 128), 5, 0, screen)
    screen.blit(cherry_animation_list[0], (5, 60))
    draw_text(f"  {cherry_count}", font, (0, 0, 128), 5, 60, screen)
    draw_text(f"Tries: {run_tries}", font, (0, 0, 128), 250, 0, screen)
    music_button.draw(screen)

    if level_button.draw(screen):
        menu.set_state("LEVEL_SELECTION")
        menu.set_level_wanted(level)
        menu.set_max_level_unlocked(max_level)
        menu.set_paused()


def draw_grid(screen, player, TILE_SIZE, MAX_COLS, scroll):
    """
    Draws a diamond-shaped grid on the screen based on the player's location.

    Parameters
    ----------
    screen : pygame.Surface
    player : Player
    TILE_SIZE : int
    MAX_COLS : int
    scroll : float or int
    """

    # draws cols
    player_loc_x, player_loc_y = player.get_location()

    rounded_p_y = player_loc_y - player_loc_y % TILE_SIZE  # The rounded up perfect tile y position.

    for col in range(MAX_COLS + 1):
        x = col * TILE_SIZE - scroll
        rounded_p_x = player_loc_x + scroll + TILE_SIZE / 2  # The rounded up tile x position with the scroll offset.
        if player_loc_x + TILE_SIZE * 5 >= x >= player_loc_x - TILE_SIZE * 5:
            rounded_p_y = player_loc_y - player_loc_y % TILE_SIZE  # Is the rounded up perfect tile y.
            offset_y = col * TILE_SIZE
            if offset_y >= rounded_p_x:
                offset_y = offset_y - 2 * (offset_y - rounded_p_x) - TILE_SIZE

            pygame.draw.line(screen, "WHITE", (x, rounded_p_y + offset_y - (rounded_p_x - 225) + TILE_SIZE),
                             (x, rounded_p_y - offset_y + (rounded_p_x - 225)))
    # draws rows
    for row in range(MAX_COLS + 1):
        y = row * TILE_SIZE
        if player_loc_y + TILE_SIZE * 5 >= y >= player_loc_y - TILE_SIZE * 5:
            offset_x = (player_loc_x - player_loc_x % TILE_SIZE) - abs(row * TILE_SIZE - rounded_p_y) + 5 * TILE_SIZE
            if rounded_p_y < y:
                offset_x += TILE_SIZE
            if not (player_loc_x / TILE_SIZE).is_integer():
                offset_x += TILE_SIZE / 2
            offset_x = offset_x - (offset_x % TILE_SIZE)
            if scroll != int(scroll):
                offset_x -= 22.5
            start_x = player_loc_x - (offset_x - player_loc_x)
            pygame.draw.line(screen, "WHITE", (start_x, y), (offset_x, y))


def draw_problem(x, y, tile, tile_id, problem_list, player, scroll, TILE_SIZE, tiles_list):
    """
    Draws a problem on the screen based on the tile ID and updates the problem list.

    Parameters
    ----------
    x : int
    y : int
    tile : Tile
        The tile object to be drawn.
    tile_id : str
    problem_list : OrderedDict
        The list of problems in the current level.
    player : Player
    scroll : int or float
    TILE_SIZE : int
        The size of a tile in the game.
    tiles_list : list
        The list of tiles in the game.
    """
    if tile_id not in problem_list:
        problem_list[tile_id] = None, {}
    if (y, x) not in problem_list[tile_id][1]:
        problem_list[tile_id][1][(y, x)] = tile
    elif (y, x) in problem_list[tile_id][1]:
        problem_list[tile_id][1][(y, x)] = tile
        if len(problem_list[tile_id][1]) > 0 and problem_list[tile_id][0] is None:
            match tile:
                case 23:
                    problem = ladder_problem.Ladder(problem_list[tile_id][1], TILE_SIZE, "ladder")
                case 8:
                    problem = bridge_problem.Bridge(problem_list[tile_id][1], TILE_SIZE, "bridge")
                case 24:
                    problem = spike_problem.Spike(problem_list[tile_id][1], TILE_SIZE, "spike", 24, 0)
                case _:
                    raise NotImplementedError("This problem is not yet implemented in here.")
            problem_list[tile_id] = problem, problem_list[tile_id][1]
        if tile_id in problem_list and len(problem_list[tile_id][1]) > 0:
            problem_list[tile_id][0].draw(player, scroll, TILE_SIZE, tiles_list)


def draw_background(screen, background, middle_ground, scroll):
    """
    Draws the game's background and middle ground on the screen, with parallax scrolling effect.

    Parameters
    ----------
    screen : pygame.Surface
    background : pygame.Surface
        The background image.
    middle_ground : pygame.Surface
        The middle ground image.
    scroll : int or float
    """
    screen.fill('crimson')
    width = background.get_width()
    for x in range(4):
        screen.blit(background, ((x * width) - scroll * 0.5, 0))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8, 300))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8 + 400, 300))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8 + 780, 300))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8, 492))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8 + 442, 450))
        screen.blit(middle_ground, ((x * width) - scroll * 0.8 + 822, 450))
