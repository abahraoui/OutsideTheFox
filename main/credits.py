import pygame


class Credits:

    def __init__(self, W, H):
        self.screen = pygame.display.get_surface()
        self.credits_text_list = []
        with open("assets/txt_files/credits.txt") as file:
            lines = file.readlines()
            for line in lines:
                self.credits_text_list.append(line.__str__()[:-1])
        self.credits_surfaces = []
        self.credits_rect = []
        self.font = pygame.font.Font('assets/joystix monospace.otf', 24)
        self.W = W
        self.H = H
        for credit_text in self.credits_text_list:
            credit_surface = self.font.render(credit_text, True, "navy")
            rect = pygame.Rect(self.W / 2 - credit_surface.get_width() / 2, H - 50, credit_surface.get_width(), credit_surface.get_height())
            self.credits_surfaces.append(credit_surface)
            self.credits_rect.append(rect)

        self.counter = 0
        self.counter_timer = pygame.time.get_ticks()
        self.done = False
        self.check_count_timer = None

    def draw(self):
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


    def get_done(self):
        return self.done


