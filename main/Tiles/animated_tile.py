import pygame
from main.tiles.tile import Tile


class AnimatedTile(Tile):
    """
    A class used to represent an animated tile in a pygame application.

    ...

    Attributes
    ----------
    animation_list : list
        The list of animations for the tile.
    current_anim : int
        The index of the current animation in the animation list.
    last_update : int
        The time when the animation was last updated.
    animation_cooldown : int
        The cooldown time between animation updates.
    rect : pygame.Rect
        The rectangle representing the tile's position and size.
    x : int
        The x-coordinate of the tile's center.
    y : int
        The y-coordinate of the tile's center.

    Methods
    -------
    set_location(coordinates):
        Sets the location of the tile.
    draw():
        Draws the tile on the display surface.
    """

    def __init__(self, x, y, anim_list, img, identification):
        """
        Parameters
        ----------
            x : int
                The x-coordinate of the tile's center.
            y : int
                The y-coordinate of the tile's center.
            anim_list : list
                The list of animations for the tile.
            img : pygame.Surface
                The image to display for the tile.
            identification : int, str
                The identification object of the tile.
        """
        super().__init__(x, y, img, identification)
        self.animation_list = anim_list
        self.current_anim = 0
        self.rect = self.animation_list[self.current_anim].get_rect()
        self.rect.center = (x + 25, y + 20)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250

    def set_location(self, coordinates):
        """
        Sets the location of the tile.

        Parameters
        ----------
        coordinates : tuple
            The new coordinates of the tile's center.
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.rect.center = (self.x + 25, self.y + 20)

    def draw(self):
        """
        Draws the tile on the display surface.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_anim += 1
            self.last_update = current_time
            if self.current_anim >= len(self.animation_list):
                self.current_anim = 0
        anim = self.animation_list[self.current_anim]
        pygame.display.get_surface().blit(anim, (self.x, self.y))
        '''pygame.draw.rect(pygame.display.get_surface(), 'magenta', self.rect, 3) # Debug hit-box.'''
