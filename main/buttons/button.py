import pygame


class Button:
    """
    A class used to represent an interactive button in a pygame application.

    ...

    Attributes
    ----------
    img : pygame.Surface
        The image to display on the button.
    rect : pygame.Rect
        The rectangle representing the button's position and size.
    position : tuple
        The position of the button's top left corner.
    clicked : bool
        Whether the button has been clicked.
    color_active : tuple, str
        The color of the button when it's active.
    color_passive : tuple, str
        The color of the button when it's passive.
    color : tuple, str
        The current color of the button.
    time_at_pressed : int
        The time when the button was last pressed.
    colliding : bool
        Whether the mouse cursor is currently colliding with the button.

    Methods
    -------
    __handle_mouse_click():
        Handles a mouse click event.
    draw(screen):
        Draws the button on the given screen.
    is_finished():
        Checks whether the button's action is finished.
    """

    def __init__(self, x, y, image, scale, color_active, color_passive, rect=None, custom_position=None):
        """
        Parameters
        ----------
            x : float
                The x-coordinate of the button's top left corner.
            y : float
                The y-coordinate of the button's top left corner.
            image : pygame.Surface
                The image to display on the button.
            scale : float
                The scale factor to apply to the image.
            color_active : tuple, str
                The color of the button when it's active.
            color_passive : tuple, str
                The color of the button when it's passive.
            rect : pygame.Rect, optional
                The rectangle representing the button's position and size.
            custom_position : tuple, optional
                The optional position of the button.
        """
        img_width = image.get_width()
        img_height = image.get_height()
        self.img = pygame.transform.scale(image, (int(img_width * scale), int(img_height * scale)))
        self.rect = self.img.get_rect() if rect is None else rect
        self.rect.topleft = (x, y)
        self.position = (self.rect.x, self.rect.y) if custom_position is None else custom_position
        self.clicked = False
        self.color_active = color_active
        self.color_passive = color_passive
        self.color = self.color_passive
        self.time_at_pressed = pygame.time.get_ticks()
        self.colliding = False

    def __handle_mouse_click(self) -> tuple:
        """
        Handles a mouse click event.
        This method checks whether the button is pressed.

        Returns
        -------
        tuple
            A tuple containing a boolean indicating whether the button was clicked and an integer representing the border width.
        """
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.colliding = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True
        if not self.rect.collidepoint(pos) and self.colliding:
            self.colliding = False
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if action:
            self.color = self.color_active
            self.time_at_pressed = pygame.time.get_ticks()
        if self.time_at_pressed + 300 <= pygame.time.get_ticks():
            self.color = self.color_passive
        border = 0 if self.color == self.color_passive else 3
        return action, border

    def draw(self, screen) -> bool:
        """
        Draws the button on the given screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which to draw the button.

        Returns
        -------
        bool
            True if the button was clicked, False otherwise.
        """
        action, border = self.__handle_mouse_click()
        pygame.draw.rect(screen, self.color, self.rect, border, 3)
        screen.blit(self.img, self.position)
        return action

    def is_finished(self) -> bool:
        """
        Checks whether the button's action is finished.

        This method checks whether the button's color is its passive color. If it is, the button's action is considered finished.

        Returns
        -------
        bool
            True if the button's action is finished, False otherwise.
        """
        return self.color == self.color_passive
