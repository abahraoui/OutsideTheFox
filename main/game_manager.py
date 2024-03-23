import math
import pygame
from main import player as player_class, code_runner
from main.tiles import animated_tile


def reset_score() -> tuple:
    """
    Resets variables.

    Returns
    -------
    tuple
    """
    score = 0
    run_tries = 0
    cherry_count = 0
    arrow = None
    return score, run_tries, cherry_count, arrow


def reset_level(editor, player_animation_list, player_start_pos, W, H, TILE_SIZE) -> tuple:
    """
    Sets up the game level.

    Parameters
    ----------
    editor : TextEditor
    player_animation_list : list
    player_start_pos : tuple
    W : int
        The width of the game screen.
    H : int
        The height of the game screen.
    TILE_SIZE : int
        The size of each tile in the game.

    Returns
    -------
    tuple
    """
    editor.set_mode("Player")
    scroll = 0
    scrolling = False
    goal_scroll = 0
    player = player_class.Player(3, 30, player_animation_list, (W, H), TILE_SIZE)
    player.set_location(player_start_pos[0] - TILE_SIZE / 2, player_start_pos[1])
    runner = code_runner.Runner(player)
    runner.subscribe(editor)
    return scroll, scrolling, goal_scroll, runner, player


def completed_problem(problem_index, runner, editor) -> int:
    """
    Marks a problem as completed and updates the game state.

    Parameters
    ----------
    problem_index : int
        The index of the completed problem.
    runner : Runner
    editor : TextEditor

    Returns
    -------
    int
    """
    problem_index += 1
    runner.set_mode("Player")
    runner.say("Well done ! Now reach the door to beat the level.")
    editor.set_mode("Player")
    runner.set_problem_completed(False)
    return problem_index


def attempt_problem(problem_list, current_problem_index, runner):
    """
    Attempts a problem and updates the problem list.

    Parameters
    ----------
    problem_list : OrderedDict
        The list of problems in the current level.
    current_problem_index : int
        The index of the current problem.
    runner : Runner
    """
    problem_list[current_problem_index][0].set_problem_try(runner.get_problem_try())
    runner.set_problem_try(None)


def deactivate_editor(editor):
    """
    Deactivates the game editor.

    Parameters
    ----------
    editor : TextEditor
        The game editor.
    """
    editor.set_mouse_over(False)
    editor.set_active(False)


def run_editor(runner, run_tries, score, editor) -> tuple:
    """
    Start the execution process and updates score variables accordingly.

    Parameters
    ----------
    runner : Runner
    run_tries : int
    score : int
    editor : TextEditor

    Returns
    -------
    tuple
    """
    runner.validate(editor.get_user_answer())
    run_tries += 1
    score -= 10
    return run_tries, score


def process_scrolling(runner, player, TILE_SIZE, scroll, scrolling, goal_scroll) -> tuple:
    """
    Handles the game scrolling.

    Parameters
    ----------
    runner : Runner
    player : Player
    TILE_SIZE : int
        The size of each tile in the game.
    scroll : int or float
        The current scroll position of the game screen.
    scrolling : bool
        Whether the worlds needs to scroll.
    goal_scroll : int or float
        The goal scroll position of the game screen.

    Returns
    -------
    tuple
    """
    if scrolling:
        scroll = pygame.math.lerp(scroll, goal_scroll, 0.05)
        if math.ceil(scroll) == math.ceil(goal_scroll) or math.floor(scroll) == math.floor(goal_scroll):
            scrolling = False
            scroll = goal_scroll
            runner.set_busy(False)

    if len(runner.get_queue()) > 0 and not player.get_lerping() and not scrolling:
        answer = runner.process_queue()
        if answer:
            goal_scroll += answer[0] * TILE_SIZE / 2
            scrolling = answer[1]
            if scrolling:
                runner.set_busy(True)

    return scroll, scrolling, goal_scroll


def start_problem(b_list, problem_index, runner, editor):
    b_list[problem_index][1][0].set_hovering(True)
    if pygame.mouse.get_pressed()[0] == 1:
        runner.set_mode("Problem")
        runner.set_problem(b_list[problem_index][1][0])
        editor.set_mode("Problem")


def process_cherry_tile(x, y, scroll, TILE_SIZE, cherry_data, cherry_animation_list, player, cherry_count, score):
    if (y, x) not in cherry_data:
        cherry = animated_tile.AnimatedTile(x * TILE_SIZE - scroll, y * TILE_SIZE, cherry_animation_list,
                                            cherry_animation_list[0], None)
        cherry_data[(y, x)] = cherry
    elif cherry_data[(y, x)] != "Removed":
        cherry_data[(y, x)].set_location((x * TILE_SIZE - scroll, y * TILE_SIZE))
    if cherry_data[(y, x)] != "Removed":
        cherry_data[(y, x)].draw()
        if player and cherry_data[(y, x)].collide_rect(player):
            crunch_sound = pygame.mixer.Sound("assets/audio/sounds/348112__matrixxx__crunch.wav")
            crunch_sound.play()
            crunch_sound.set_volume(1)
            cherry_data[(y, x)] = "Removed"
            score += 50
            cherry_count += 1
    return cherry_data, score, cherry_count
