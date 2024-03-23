import pygame


class SpriteSheet:
    """
    A class used to represent a sprite sheet in a pygame application.

    ...

    Methods
    -------
    __init__(image):
        Constructs all the necessary attributes for the sprite sheet object.
    get_image(frame, width, height, scale, colour):
        Extracts a specific image from the sprite sheet.
    """
    def __init__(self, image):
        """ 
        Parameters
        ----------
        image : pygame.Surface
            The image of the sprite sheet.
        """
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour) -> pygame.Surface:
        """
        Extracts a specific image from the sprite sheet.

        Parameters
        ----------
        frame : int
            The frame number of the image in the sprite sheet.
        width : int
            The width of the image.
        height : int
            The height of the image.
        scale : int
            The scale factor to apply to the image.
        colour : tuple, str
            The color to set as transparent in the image.

        Returns
        -------
        pygame.Surface
            The extracted image.
        """
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
