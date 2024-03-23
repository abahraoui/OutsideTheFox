import pygame

from main.buttons.button import Button


def scale_img(scale, color, img) -> pygame.Surface:
    """
    Scales the given image by the given scale factor and sets its color key.

    Parameters
    ----------
    scale : float
        The scale factor to apply to the image.
    color : tuple, str
        The color to set as the color key of the image.
    img : pygame.Surface
        The image to scale and set the color key of.

    Returns
    -------
    pygame.Surface
        The scaled image with the color key set.
    """
    new_img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
    new_img.set_colorkey(color)
    return new_img


class MusicButton(Button):
    """
    A class used to represent an interactive music button in a pygame application.

    ...

    Attributes
    ----------
    img_active : pygame.Surface
        The image to display on the button when it's active.
    img_passive : pygame.Surface
        The image to display on the button when it's passive.
    music_tracks : list
        The list of music tracks associated with the button.
    active : bool
        Whether the button is currently active.

    Methods
    -------
    __handle_mouse_click():
        Handles a mouse click event.
    __handle_music():
        Handles the music playback.
    draw(screen):
        Draws the button on the given screen.
    """
    def __init__(self, x, y, img_active, img_passive, scale, color_active, color_passive, music_assets, image):
        """
        Parameters
        ----------
            x : float
                The x-coordinate of the button's top left corner.
            y : float
                The y-coordinate of the button's top left corner.
            img_active : pygame.Surface
                The image to display on the button when it's active.
            img_passive : pygame.Surface
                The image to display on the button when it's passive.
            scale : float
                The scale factor to apply to the images.
            color_active : tuple, str
                The color of the button when it's active.
            color_passive : tuple, str
                The color of the button when it's passive.
            music_assets : cycle
                The list of music tracks associated with the button.
            image : pygame.Surface
                The image to display on the button.
        """
        super().__init__(x, y, image, scale, color_active, color_passive)
        self.clicked = None
        self.img_active = scale_img(scale, (255, 255, 255), img_active)
        self.img_passive = scale_img(scale, (255, 255, 255), img_passive)
        self.music_tracks = music_assets
        self.active = True

    def __handle_mouse_click(self):
        """
        Handles a mouse click event to turn on or off the music.
        This method checks whether the button is pressed.

        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.active = not self.active
                if self.active:
                    pygame.mixer.music.set_volume(0.03)
                else:
                    pygame.mixer.music.set_volume(0)
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def __handle_music(self):
        """

        Handles the ambient music.

        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(next(self.music_tracks))
            pygame.mixer.music.play()

    def draw(self, screen):
        """
        Draws the button on the given screen.
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface on which to draw the button.
        """
        self.__handle_music()
        self.__handle_mouse_click()

        if self.active:
            screen.blit(self.img_active, (self.rect.x, self.rect.y))
        elif not self.active:
            screen.blit(self.img_passive, (self.rect.x, self.rect.y))
