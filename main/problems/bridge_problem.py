import pygame

from main.problems.problem import ProblemInterface
from main.tiles import tile as tile_class


class Bridge(ProblemInterface):
    """
    A class used to represent a bridge problem in a pygame application.

    ...

    Methods
    -------
    __init__(image_list, tile_size, identification):
        Constructs all the necessary attributes for the bridge problem object.
    init_problem():
        Initializes the bridge problem.
    process_problem(player, scroll, TILE_SIZE, tiles_list):
        Processes the bridge problem.
    validate_problem(attempt):
        Validates an attempt at the bridge problem.
    draw_rect(TILE_SIZE, scroll, color):
        Draws a rectangle around the bridge problem.
    get_problem_size():
        Returns the size of the bridge problem.
    """

    def __init__(self, image_list, tile_size, identification):
        """
        Parameters
        ----------
        image_list : list
            The list of images for the tiles of the problem.
        tile_size : int
            The size of each tile.
        identification : int, str
            The identification number of the problem.
        """
        super().__init__(image_list, tile_size, identification)

    def init_problem(self):
        """
        Initializes the bridge problem.
        """
        self.problem = [False] * self.size
        smallest_elem = (0, 0)
        for tile in self.tile_list:
            if tile[0] > smallest_elem[0]:
                smallest_elem = tile[0], tile[1]
        self.starting_pos = smallest_elem[0] + 1, smallest_elem[1] + 1

    def process_problem(self, player, scroll, TILE_SIZE, tiles_list):
        """
        Processes the bridge problem.

        Parameters
        ----------
        player : pygame.sprite.Sprite
            The player object.
        scroll : int or float
            The scroll offset.
        TILE_SIZE : int
            The size of each tile.
        tiles_list : list
            The list of tiles.
        """
        if self.completed:
            offset = 3
        else:
            offset = 0
        for key in self.tile_list:
            tile = self.tile_list[key]
            x = key[1] + offset
            y = key[0] + offset
            if self.completed:
                offset -= 1
            t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, tiles_list[tile], tile)
            t.draw()
            if player and t.collide_rect(player):
                player.is_colliding((t.x, t.y), key)
            elif player:
                player.not_colliding(key)

    def validate_problem(self, attempt) -> tuple:
        """
        Validates an attempt at the bridge problem.

        Parameters
        ----------
        attempt : object
            The attempted solution.

        Returns
        -------
        tuple
            A tuple containing a boolean indicating whether the attempt was valid and a string with feedback.
        """
        valid = False
        text = "\n"
        self.set_problem_try(attempt)
        if isinstance(attempt, list) and len(attempt) == self.get_problem_size() and len(
                set(attempt)) == 1 and attempt[0] == "wood":
            valid = True
            self.complete_problem()
        else:
            if not isinstance(attempt, list):
                text += f"Your 'bridge' object is not an array\n"
            if len(attempt) != self.get_problem_size():
                text += f"Your 'bridge' array is too big or too small. Remember it should be of size" \
                        f" {self.get_problem_size()}\n"
            if len(set(attempt)) != 1:
                text += "You didn't represent a bridge's tile with the same kind of object.\n"
            if len(attempt) > 0 and attempt[0] != "wood":
                text += "Your bridge is not filled with 'wood'.\n"
        return valid, text

    def draw_rect(self, TILE_SIZE, scroll, color):
        """
        Draws a rectangle around the bridge problem to display visual feedback on attempts.

        Parameters
        ----------
        TILE_SIZE : int
            The size of each tile.
        scroll : int or float
            The scroll offset.
        color : tuple, str
            The color of the rectangle.
        """
        screen = pygame.display.get_surface()
        rect = pygame.Rect(self.starting_pos[1] * TILE_SIZE - scroll, (self.starting_pos[0]) * TILE_SIZE,
                           self.size * TILE_SIZE, TILE_SIZE)
        for i in range(self.size):
            start_x = (self.starting_pos[1] + i) * TILE_SIZE - scroll
            start_y = (self.starting_pos[0]) * TILE_SIZE
            end_x = (self.starting_pos[1] + i) * TILE_SIZE - scroll
            end_y = (self.starting_pos[0]) * TILE_SIZE + TILE_SIZE
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)
        pygame.draw.rect(screen, color, rect, 3)

    def get_problem_size(self) -> int:
        """
        Returns the size of the bridge problem.

        Returns
        -------
        int
        """
        return self.size
