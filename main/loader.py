import os
from collections import OrderedDict
from itertools import cycle

import pygame

from main import spritesheet

"""
This module contains loading functions used in the game file.
"""


def read_file(file_path, offset=""):
    """
    Reads a file and returns its content as a string.

    Parameters
    ----------
    file_path : str
    offset : str, optional
        The offset to be optionally added at the end of each line.

    Returns
    -------
    str
        The content of the file as a string.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        text = ""
        for line in lines:
            text += line + offset
        return text


def load_background(width, height) -> tuple:
    """
    Loads and scales the background and middle ground images.

    Parameters
    ----------
    width : int
        The width to scale the images to.
    height : int
        The height to scale the images to.

    Returns
    -------
    tuple
        The scaled background and middle ground images.
    """
    bg = pygame.image.load('assets/back.png').convert_alpha()
    bg = pygame.transform.scale(bg, (width, height))
    md = pygame.image.load('assets/middle.png').convert_alpha()
    md = pygame.transform.scale(md, (500, 450))
    return bg, md


def load_sprite_animation(path, size, scale, color, steps):
    """
    Loads a sprite animation from a sprite sheet.

    Parameters
    ----------
    path : str
    size : int
        The size of each sprite in the sprite sheet.
    scale : int
    color : str
    steps : int
        The number of steps in the animation.

    Returns
    -------
    list
        The list of sprites in the animation.
    """
    animation_list = []
    sprite_sheet_image = pygame.image.load(path).convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    for k in range(steps):
        temp_img = sprite_sheet.get_image(k, size, size, scale, color)
        animation_list.append(temp_img)
    return animation_list


def load_tiles(tile_types, tile_size) -> list:
    """
    Loads and scales the tile images.

    Parameters
    ----------
    tile_types : int
        The number of different types of tiles.
    tile_size : int
        The normal size of a tile.
    Returns
    -------
    list
        The list of scaled tile images.
    """
    tiles_list = []
    for tile_num in range(tile_types):
        img = pygame.image.load(f'assets/tile/{tile_num}.png').convert_alpha()
        if tile_num == 14:
            img = pygame.transform.scale(img, (tile_size, 2 * tile_size))
        elif tile_num in [17, 25]:
            img = pygame.transform.scale(img, (5 * tile_size, 5 * tile_size))
        elif tile_num in [18, 15, 16]:
            img = pygame.transform.scale(img, (4 * tile_size, 4 * tile_size))
        elif tile_num in [19]:
            img = pygame.transform.scale(img, (3 * tile_size, 3 * tile_size))
        elif tile_num in []:
            img = pygame.transform.scale(img, (2 * tile_size, 2 * tile_size))
        else:
            img = pygame.transform.scale(img, (tile_size, tile_size))
        img.set_colorkey((0, 0, 0))
        tiles_list.append(img)
    return tiles_list


def load_world_coordinates(ROWS, MAX_COLS) -> tuple:
    """
    Initializes the world data and world coordinates.

    Parameters
    ----------
    ROWS : int
        The number of rows in the grid.
    MAX_COLS : int
        The number of columns in the grid.

    Returns
    -------
    tuple
        The initialized world coordinates and world data.
    """
    world_data = []
    world_coordinates = []
    for i in range(ROWS):
        row = [-1] * MAX_COLS
        coord_row = [(0, 0)] * MAX_COLS
        world_data.append(row)
        world_coordinates.append(coord_row)
    return world_coordinates, world_data


def reset_variables() -> tuple:
    """
    Resets game variables.

    Returns
    -------
    tuple
    """
    return OrderedDict(), OrderedDict(), 0, 0, 0, {}, False


def load_level_txt_files(restart, level, loaded_level, editor, user_manual, final_level, max_level) -> int:
    """
    Loads the level text files.

    Parameters
    ----------
    restart : bool
        Whether the game is being restarted.
    level : int
        The current level.
    loaded_level : int
        The level to load.
    editor : TextEditor
    user_manual : UserManual
    final_level : int
        The final level of the game.
    max_level : int
        The maximum unlocked level.

    Returns
    -------
    int
    """
    if not restart:
        file_path = f'main/level_data/level_code/level{level}_text.txt'
        if os.path.exists(file_path):
            final_text = read_file(file_path, " ")
            final_text = final_text[:-2]
            editor.set_user_answer(final_text)
    file_path = f'main/level_data/hint_txt/hint{loaded_level + 1}.txt'
    if os.path.exists(file_path):
        text = read_file(file_path)
        user_manual.set_hint_text(text)
    file_path = f'main/level_data/level_txt/level{loaded_level + 1}.txt'
    if os.path.exists(file_path):
        text = read_file(file_path)
        user_manual.set_level_text(text)

    with open(f'main/level_data/max_level.txt', 'r') as file:
        current_max_level = int(file.readline())
        if current_max_level < final_level + 1:
            max_level = int(current_max_level)
    return max_level


def load_player_animation_list() -> list:
    """
    Loads the player animation list.

    Returns
    -------
    list
    """
    animation_steps = [4, 6, 2, 2, 2, 4]
    animation_assets = ['assets/player_idle.png', 'assets/player_run.png', 'assets/player_jump.png',
                        'assets/player_hurt'
                        '.png',
                        'assets/player_crouch.png', 'assets/player_climb.png']

    player_animation_list = []
    for anim_num in range(len(animation_steps)):
        animation = animation_steps[anim_num]
        sprite_sheet_image = pygame.image.load(animation_assets[anim_num]).convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        temp_img_list = []
        for p in range(animation):
            temp_img_list.append(sprite_sheet.get_image(p, 32, 32, 3, "black"))
        player_animation_list.append(temp_img_list)
    return player_animation_list


def load_credits_music():
    """
    Loads and plays the credits music.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/music/640853__kjartan_abel__gonna-be-gone.wav")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.08)


def load_hud_assets() -> tuple:
    """
    Loads the HUD assets.

    Returns
    -------
    tuple
    """
    off = pygame.image.load("assets/music_off.png").convert_alpha()
    on = pygame.image.load("assets/music_on.png").convert_alpha()
    on.set_colorkey("black")
    level_icon = pygame.image.load("assets/level_icon.png").convert_alpha()
    music_assets = cycle(['assets/audio/music/611440__kjartan_abel__after-the-flu.wav',
                          'assets/audio/music/647212__kjartan_abel__boschs-garden.wav',
                          'assets/audio/music/686838__zhr__desert-ambient-music.wav'])
    return off, on, level_icon, music_assets
