import pygame


class Cherry():

    def __init__(self, x, y, anim_list, identification):
        self.x = x
        self.y = y
        self.animation_list = anim_list
        self.current_anim = 0
        self.id = identification
        self.rect = self.animation_list[self.current_anim].get_rect()
        self.rect.center = (x + 25, y + 20)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 250
    def get_id(self):
        return self.id

    def set_location(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.rect.center = (self.x + 25, self.y + 20)

    def draw(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_anim += 1
            self.last_update = current_time
            if self.current_anim >= len(self.animation_list):
                self.current_anim = 0
        anim = self.animation_list[self.current_anim]
        pygame.display.get_surface().blit(anim, (self.x, self.y))
        # pygame.draw.rect(pygame.display.get_surface(), 'magenta', self.rect, 3)

    def colliderect(self, collided):
        if pygame.sprite.collide_rect(self, collided):
            return True
        return False



