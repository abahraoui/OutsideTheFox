import pygame


class Tile(pygame.sprite.Sprite):
    """
    A class used to represent a tile.

    ...

    Attributes

    ----------
    image : pygame.Surface
        The image to display for the tile.
    id : int
        The identification number of the tile.
    rect : pygame.Rect
        The rectangle representing the tile's position and size.
    x : int
        The x-coordinate of the tile's center.
    y : int
        The y-coordinate of the tile's center.

    Methods
    -------
    draw():
        Draws the tile on the display surface.
    collide_rect(collided):
        Checks whether the tile is colliding with another sprite.
    get_rect():
        Returns the rectangle representing the tile's position and size.
    get_id():
        Returns the identification number of the tile.
    """

    def __init__(self, x, y, img, identification):
        """
        Parameters
        ----------
            x : int
                The x-coordinate of the tile's center.
            y : int
                The y-coordinate of the tile's center.
            img : pygame.Surface
                The image to display for the tile.
            identification : int
                The identification object of the tile.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.id = identification
        self.rect = self.image.get_rect()
        self.rect.center = (x + 22, y + 22)
        self.x = x
        self.y = y

    def draw(self):
        """
        Draws the tile on the display surface.
        """
        pygame.display.get_surface().blit(self.image, (self.x, self.y))
        '''pygame.draw.rect(pygame.display.get_surface(), 'magenta', self.rect, 3) # Debug hit-box of tiles'''

    def collide_rect(self, collided) -> bool:
        """
        Checks whether the tile is colliding with another sprite.

        Parameters
        ----------
        collided : pygame.sprite.Sprite
            The sprite to check for collision with.

        Returns
        -------
        bool
            True if the tile is colliding with the sprite, False otherwise.
        """
        if pygame.sprite.collide_rect(self, collided):
            return True
        return False

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle representing the tile's position and size.

        Returns
        -------
        pygame.Rect
            The rectangle representing the tile's position and size.
        """
        return self.rect

    def get_id(self) -> int:
        """
        Returns the identification number of the tile.

        Returns
        -------
        int
            The identification number of the tile.
        """
        return self.id
