import pygame

from main.tiles.tile import Tile


class Door(Tile):
    """
    A class used to represent a door tile in a pygame application.

    ...

    Methods
    -------
    __init__(x, y, img, identification):
        Constructs all the necessary attributes for the door tile object.
    draw():
        Draws the door tile on the display surface.
    """

    def __init__(self, x, y, img, identification):
        """
        Parameters
        ----------
        x : int
            The x-coordinate of the door tile.
        y : int
            The y-coordinate of the door tile.
        img : pygame.Surface
            The image of the door tile.
        identification : int
            The identification number of the door tile.
        """
        super().__init__(x, y, img, identification)

    def draw(self):
        """
        Draws the door tile on the display surface.
        """
        pygame.display.get_surface().blit(self.image, (self.x, self.y - 32))
        pygame.draw.rect(pygame.display.get_surface(), 'BLUE', self.rect, 3)
