from main.tiles.tile import Tile


class Ladder(Tile):
    """
    A class used to represent a ladder tile in a pygame application.

    ...

    Methods
    -------
    __init__(x, y, img, identification):
        Constructs all the necessary attributes for the ladder tile object.
    collide_rect(collided):
        Checks if the ladder tile has collided with another object.
    """
    def __init__(self, x, y, img, identification):
        """
        Parameters
        ----------
        x : int
            The x-coordinate of the ladder tile.
        y : int
            The y-coordinate of the ladder tile.
        img : pygame.Surface
            The image of the ladder tile.
        identification : int
            The identification number of the ladder tile.
        """
        super().__init__(x, y, img, identification)

    def collide_rect(self, collided) -> bool:
        """
        Checks if the ladder tile has collided with another object.

        Parameters
        ----------
        collided :  object
            The object that potentially collided with the ladder tile.

        Returns
        -------
        bool
            True if the ladder tile has collided with the object, False otherwise.
        """
        x, y = collided.get_location()
        if self.x < x < self.x + 45 and (self.y < y or y >= self.y - 45):
            return True
        return False
