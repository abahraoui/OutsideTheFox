import pygame

from main.problems.problem import ProblemInterface
from main.tiles import tile as tile_class


class Spike(ProblemInterface):
    """
    A class used to represent a spike problem in a pygame application.

    ...

    Methods
    -------
    __init__(image_list, tile_size, identification, incomplete_tile_id, complete_tile_id):
        Constructs all the necessary attributes for the spike problem object.
    init_problem():
        Initializes the spike problem.
    process_problem(player, scroll, TILE_SIZE, tiles_list):
        Processes the spike problem.
    validate_problem(attempt):
        Validates an attempt at the spike problem.
    draw_rect(TILE_SIZE, scroll, color):
        Draws a rectangle around the spike problem.
    get_problem_size():
        Returns the size of the spike problem.
    """

    def __init__(self, image_list, tile_size, identification, incomplete_tile_id, complete_tile_id):
        """
        Parameters
        ----------
        image_list : list
            The list of images for the tiles of the problem.
        tile_size : int
            The size of each tile.
        identification : int, str
            The identification number of the problem.
        incomplete_tile_id : int
            The identification number of the incomplete tile.
        complete_tile_id : int
            The identification number of the complete tile.
        """
        super().__init__(image_list, tile_size, identification)
        self.incomplete_tile_id = incomplete_tile_id
        self.complete_tile_id = complete_tile_id

    def init_problem(self):
        """
        Initializes the spike problem.
        """
        self.problem = [True] * self.size
        smallest_elem = (0, 1000)
        for tile in self.tile_list:
            if tile[1] < smallest_elem[1]:
                smallest_elem = tile
        self.starting_pos = smallest_elem

    def process_problem(self, player, scroll, TILE_SIZE, tiles_list):
        """
        Processes the spike problem.

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
            tile_id = self.complete_tile_id
        else:
            tile_id = self.incomplete_tile_id
        for key in self.tile_list:
            x = key[1]
            y = key[0]
            t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, tiles_list[tile_id], tile_id)
            t.draw()
            if not self.completed:
                if player and t.collide_rect(player):
                    player.set_finished()
            elif self.completed:
                if player and t.collide_rect(player):
                    player.is_colliding((t.x, t.y), key)
                elif player:
                    player.not_colliding(key)

    def validate_problem(self, attempt) -> tuple:
        """
        Validates an attempt at the spike problem.

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
                set(attempt)) == 1 and bool(attempt[0]) is False:
            valid = True
            self.complete_problem()
        else:
            if not isinstance(attempt, list):
                text += f"Your 'spike' object is not an array\n"
            if len(attempt) != self.get_problem_size():
                text += f"Your 'spike' array is too big or too small. Remember it should be of size" \
                        f" {self.get_problem_size()}\n"
            if len(set(attempt)) != 1:
                text += "You didn't represent a spike's tile with the same kind of object.\n"
            if len(attempt) > 0 and bool(attempt[0]) is not False:
                text += "Your spike's tiles are not a 'False' object.\n"
        return valid, text

    def draw_rect(self, TILE_SIZE, scroll, color):
        """
        Draws a rectangle around the spike problem to display visual feedback on attempts.

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
        Returns the size of the spike problem.

        Returns
        -------
        int
            The size of the spike problem.
        """
        return self.size
