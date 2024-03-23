import pygame


class Credits:
    """
    A class used to represent the credits screen in a pygame application.

    ...

    Methods
    -------
    __init__(width, height):
        Constructs all the necessary attributes for the credits screen object.
    __init_credits():
        Initializes the credits screen.
    draw():
        Draws the credits on the display surface.
    get_done() -> bool:
        Checks if the credits have finished scrolling.
    """

    def __init__(self, width, height):
        """
        Parameters
        ----------
        width : int
            The width of the display surface.
        height : int
            The height of the display surface.
        """
        self.screen = pygame.display.get_surface()
        self.credits_text_list = []
        self.credits_surfaces = []
        self.credits_rect = []
        self.font = pygame.font.Font('assets/joystix monospace.otf', 24)
        self.width = width
        self.height = height
        self.counter = 0
        self.counter_timer = pygame.time.get_ticks()
        self.done = False
        self.check_count_timer = None
        self.__init_credits()

    def __init_credits(self):
        """
        Initializes the credits screen.

        Reads the credits from a text file and creates surfaces and rectangles for each line of text.
        """
        with open("assets/txt_files/credits.txt") as file:
            lines = file.readlines()
            for line in lines:
                self.credits_text_list.append(str(line[:-1]))
        for credit_text in self.credits_text_list:
            credit_surface = self.font.render(credit_text, True, "navy")
            rect = pygame.Rect(self.width / 2 - credit_surface.get_width() / 2, self.height - 50,
                               credit_surface.get_width(), credit_surface.get_height())
            self.credits_surfaces.append(credit_surface)
            self.credits_rect.append(rect)

    def draw(self):
        """
        Draws the credits on the display surface.

        Scrolls the credits upwards and checks if they have finished scrolling.
        """
        if self.check_count_timer is None:
            self.check_count_timer = pygame.time.get_ticks()

        if not self.done:
            count = 0
            for i in range(len(self.credits_surfaces)):
                if i < self.counter:
                    rect = self.credits_rect[i]
                    surface = self.credits_surfaces[i]
                    self.credits_rect[i].y -= 1
                    if rect.y <= 0:
                        continue
                    count += 1
                    print()
                    pygame.draw.rect(self.screen, "white", rect, 0, 3)
                    self.screen.blit(surface, rect)

            if pygame.time.get_ticks() > self.counter_timer + 2000:
                self.counter_timer = pygame.time.get_ticks()
                self.counter += 1

            if count == 0 and pygame.time.get_ticks() > self.check_count_timer + 5000:
                self.done = True

    def get_done(self) -> bool:
        """
        Returns
        -------
        bool
            True if the credits have finished scrolling, False otherwise.
        """
        return self.done
