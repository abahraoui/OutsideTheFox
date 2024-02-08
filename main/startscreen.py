import pygame.display


class StartScreen:

    def __init__(self, lastUpdate, playerRunCycle, text, textRect, screenSize):
        self.HW = screenSize[0]
        self.HH = screenSize[1]
        self.lastUpdate = lastUpdate
        self.playerRunCycle = playerRunCycle
        self.playerAnim = next(self.playerRunCycle)
        self.text = text
        self.textRect = textRect
        self.screen = pygame.display.get_surface()

    def start_screen_on(self, current_time):
        if current_time > self.lastUpdate + 100:
            self.playerAnim = next(self.playerRunCycle)
            self.lastUpdate = current_time
        self.screen.blit(self.playerAnim, (self.HW - 42, self.HH + 20))
        self.screen.blit(self.text, self.textRect)
