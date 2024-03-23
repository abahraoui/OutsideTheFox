from abc import abstractmethod, ABC

import pygame


class ProblemInterface(ABC):
    """
    An abstract base class used to represent a problem in a pygame application.

    ...

    Attributes
    ----------
    tile_list : list
        The list of images for the tiles of the problem.
    size : int
        The number of tiles in the problem.
    tile_size : int
        The size of each tile.
    completed : bool
        Whether the problem has been completed.
    id : int, str
        The identification number of the problem.
    hovering : bool
        Whether the mouse cursor is hovering over the problem.
    show_feedback : bool
        Whether to show feedback for the problem.
    feedback_timer : int
        The time when feedback was last shown for the problem.
    problem : object
        The current problem.
    starting_pos : tuple
        The starting position of the problem.

    Methods
    -------
    init_problem():
        Initializes the problem. To be implemented in a concrete class.
    process_problem(player, scroll, TILE_SIZE, tiles_list):
        Processes the problem. To be implemented in a concrete class.
    validate_problem(attempt):
        Validates an attempt at the problem. To be implemented in a concrete class.
    draw_rect(TILE_SIZE, scroll, color):
        Draws a rectangle around the problem. To be implemented in a concrete class.
    get_problem_size():
        Returns the size of the problem. To be implemented in a concrete class.
    complete_problem():
        Marks the problem as completed.
    set_hovering(value):
        Sets whether the mouse cursor is hovering over the problem.
    set_problem_try(value):
        Sets the current problem and shows feedback for it.
    draw(player, scroll, tile_size, tiles_list):
        Draws the problem and its feedback on the display surface.
    get_show_feedback():
        Returns whether feedback is being shown for the problem.
    get_completed():
        Returns whether the problem has been completed.
    get_id():
        Returns the identification number of the problem.
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
        self.tile_list = image_list
        self.size = len(image_list)
        self.tile_size = tile_size
        self.completed = False
        self.id = identification
        self.hovering = False
        self.show_feedback = False
        self.feedback_timer = pygame.time.get_ticks()
        self.problem = None
        self.starting_pos = (0, 0)
        self.init_problem()

    @abstractmethod
    def init_problem(self):
        """
        Initializes the problem. To be implemented in a concrete class.
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def process_problem(self, player, scroll, TILE_SIZE, tiles_list):
        """
        Processes the problem. To be implemented in a concrete class.

        Parameters
        ----------
        player : object
            The player object.
        scroll : int or float
            The scroll offset.
        TILE_SIZE : int
            The size of each tile.
        tiles_list : list
            The list of tiles.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def validate_problem(self, attempt):
        """
        Validates an attempt at the problem. To be implemented in a concrete class.

        Parameters
        ----------
        attempt : object
            The attempted solution.
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def draw_rect(self, TILE_SIZE, scroll, color):
        """
        Draws a rectangle around the problem to display visual feedback on attempts.
         To be implemented in a concrete class.

        Parameters
        ----------
        TILE_SIZE : int
            The size of each tile.
        scroll : int or float
            The scroll offset.
        color : tuple, str
            The color of the rectangle.
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def get_problem_size(self) -> object:
        """
        Returns the size of the problem. To be implemented in a concrete class.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    def complete_problem(self):
        """
        Marks the problem as completed.
        """
        self.completed = True

    def set_hovering(self, value):
        """
        Sets whether the mouse cursor is hovering over the problem.

        Parameters
        ----------
        value : bool
        """
        self.hovering = value

    def set_problem_try(self, value):
        """
        Sets the current attempt and shows feedback for it.

        Parameters
        ----------
        value : object
            The current attempt.
        """
        self.show_feedback = True
        self.feedback_timer = pygame.time.get_ticks()
        self.problem = value

    def draw(self, player, scroll, tile_size, tiles_list):
        """
        Draws the problem and its feedback on the display surface.

        Parameters
        ----------
        player : object
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

    def get_show_feedback(self) -> bool:
        """
        Returns whether feedback is being shown for the problem.

        Returns
        -------
        bool
        """
        return self.show_feedback

    def get_completed(self) -> bool:
        """
        Returns whether the problem has been completed.

        Returns
        -------
        bool
        """
        return self.completed

    def get_id(self) -> int:
        """
        Returns the identification number of the problem.

        Returns
        -------
        int
        """
        return self.id
