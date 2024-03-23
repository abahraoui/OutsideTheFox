import pygame
from main.problems.problem import ProblemInterface
from main.tiles import tile as tile_class


class Ladder(ProblemInterface):
    """
    A class used to represent a ladder problem in a pygame application.

    ...

    Methods
    -------
    __init__(image_list, tile_size, identification):
        Constructs all the necessary attributes for the ladder problem object.
    init_problem():
        Initializes the ladder problem.
    draw_rect(TILE_SIZE, scroll, color):
        Draws a rectangle around the ladder problem.
    process_problem(player, scroll, TILE_SIZE, tiles_list):
        Processes the ladder problem.
    validate_problem(attempt):
        Validates an attempt at the ladder problem.
    draw(player, scroll, tile_size, tiles_list):
        Draws the ladder problem and its feedback on the display surface.
    get_problem_size():
        Returns the size of the ladder problem.
    """

    def __init__(self, image_list, tile_size, identification):
        """
        Constructs all the necessary attributes for the ladder problem object.

        Parameters
        ----------
        image_list : list
            The list of images for the tiles of the problem.
        tile_size : int
            The size of each tile.
        identification : int, str
            The identification number of the problem.
        """
        self.original_problem = []
        self.column_size = 0
        self.count = 0
        super().__init__(image_list, tile_size, identification)

    def init_problem(self):
        """
        Initializes the ladder problem.
        """
        smallest_elem = (1000, 0)
        for tile in self.tile_list:
            if tile[0] < smallest_elem[0] and tile[1] > smallest_elem[1]:
                smallest_elem = tile[0], tile[1] - 1
        self.starting_pos = smallest_elem
        self.column_size = self.size + 1
        self.problem = [[0 for _ in range(self.column_size)] for _ in range(self.size)]
        for tile in self.tile_list:
            i = self.size - 1 + self.starting_pos[0] - tile[0]
            j = -(self.starting_pos[1] - tile[1])
            self.problem[i][j] = 1

        self.original_problem = self.problem.copy()

        count = 0
        for i in range(self.size):
            count += self.problem[i].count(1)
        self.count = count

    def draw_rect(self, TILE_SIZE, scroll, color):
        """
        Draws a rectangle around the ladder problem to display visual feedback on attempts.

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
        rect = pygame.Rect(self.starting_pos[1] * TILE_SIZE - scroll,
                           (self.starting_pos[0] - self.size + 1) * TILE_SIZE,
                           self.column_size * TILE_SIZE, self.size * TILE_SIZE)

        pygame.draw.rect(screen, color, rect, 3)
        for i in range(self.size):
            pygame.draw.line(screen, color, (
                self.starting_pos[1] * TILE_SIZE - scroll, (self.starting_pos[0] - self.size + 1 + i) * TILE_SIZE),
                             ((self.starting_pos[1] + self.column_size) * TILE_SIZE - scroll,
                              (self.starting_pos[0] - self.size + 1 + i) * TILE_SIZE))
        for i in range(self.column_size):
            pygame.draw.line(screen, color, (
                (self.starting_pos[1] + i) * TILE_SIZE - scroll,
                (self.starting_pos[0] - self.size + 1) * TILE_SIZE),
                             ((self.starting_pos[1] + i) * TILE_SIZE - scroll,
                              (self.starting_pos[0] - self.size + 1) * TILE_SIZE + self.size * TILE_SIZE))

    def process_problem(self, player, scroll, TILE_SIZE, tiles_list):
        """
        Processes the ladder problem.

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
        initial_pos = 2, 0
        indexes = []
        for i, row in enumerate(self.problem):
            for j, value in enumerate(row):
                if value == 1:
                    indexes.append((i, j))

        for index in indexes:
            y_offset = initial_pos[0] - index[0]
            x_offset = initial_pos[1] - index[1]
            tile = 9
            x = self.starting_pos[1] - x_offset
            y = self.starting_pos[0] - y_offset
            if self.completed:
                x_offset += 1
                y_offset -= 1
            t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, tiles_list[tile], tile)
            t.draw()
            if self.completed:
                if player and t.collide_rect(player):
                    player.add_ladder((y, x))
                else:
                    player.remove_ladder((y, x))

    def validate_problem(self, attempt) -> tuple:
        """
        Validates an attempt at the ladder problem.

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
        if isinstance(attempt, list):
            num_rows = len(attempt)

            if num_rows > 0 and isinstance(attempt[0], list):
                num_columns = len(attempt[0])
            else:
                num_columns = 0
            count = 0
            is_valid = False
            index_of_one = []
            for i in range(len(attempt)):
                if isinstance(attempt[i], list):
                    count += attempt[i].count(1)
                    if 1 in attempt[i]:
                        index_of_one.append(attempt[i].index(1))
            if len(index_of_one) == 3 and len(set(index_of_one)) == 1:
                is_valid = True
            if num_rows == self.get_problem_size()[0] and num_columns == \
                    self.get_problem_size()[1]:
                self.set_problem_try(attempt)
                if count == self.get_problem_size()[2] and is_valid:
                    valid = True
                    self.complete_problem()
                else:
                    if count != self.get_problem_size()[2]:
                        text += f"You are using too few or too many ladders, remember you have " \
                                f"{self.get_problem_size()[2]} ladders available.\n"
                    if not is_valid:
                        text += "Your ladder is not in a vertical and aligned valid position, try changing it.\n"
            else:
                if num_rows != self.get_problem_size()[0]:
                    text += "Your 'ladder' array has too many or too few rows.\n"
                if num_columns != self.get_problem_size()[1]:
                    text += "Your 'ladder' array has too many or too few columns.\n"
        else:
            text += "Your 'ladder' object, is not an array.\n"
        return valid, text

 
    def draw(self, player, scroll, tile_size, tiles_list):
        """
        Draws the ladder problem and its feedback on the display surface.
        Overrides the parent function.

        Parameters
        ----------
        player : pygame.sprite.Sprite
            The player object.
        scroll : int or float
            The scroll offset.
        tile_size : int
            The size of each tile.
        tiles_list : list
            The list of tiles.
        """
        self.process_problem(player, scroll, tile_size, tiles_list)
        if self.hovering and not self.show_feedback:
            self.draw_rect(tile_size, scroll, (255, 253, 208))
        if self.show_feedback:
            if self.completed:
                color = "green"
            else:
                color = "red"
            self.draw_rect(tile_size, scroll, color)
            if pygame.time.get_ticks() > self.feedback_timer + 2000:
                self.show_feedback = False
                if not self.completed:
                    self.problem = self.original_problem.copy()

    def get_problem_size(self) -> tuple:
        """
        Returns the size of the ladder problem.

        Returns
        -------
        tuple
            A tuple containing the number of rows, the number of columns, and the count of the ladder problem.
        """
        return self.size, self.column_size, self.count
