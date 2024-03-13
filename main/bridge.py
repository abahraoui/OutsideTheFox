import pygame
from main import tile as tile_class


class Bridge:

    def __init__(self, W, H, image_list, completed, tile_size, id, problem):
        self.tile_list = image_list
        self.size = len(image_list)
        self.tile_size = tile_size
        self.completed = completed
        self.id = id
        self.W = W
        self.H = H
        self.hovering = False
        self.show_feedback = False
        self.feedback_timer = pygame.time.get_ticks()

        if self.id == 23:
            min = (1000, 0)
            for tile in self.tile_list:
                if tile[0] < min[0] and tile[1] > min[1]:
                    min = tile[0], tile[1] - 1
            self.starting_pos = min
            self.column_size = self.size + 1
            self.problem = [[0 for j in range(self.column_size)] for i in range(self.size)]
            for tile in self.tile_list:
                i = self.size - 1 + self.starting_pos[0] - tile[0]
                j = -(self.starting_pos[1] - tile[1])
                self.problem[i][j] = 1

            self.original_problem = self.problem.copy()

            count = 0
            for i in range(self.size):
                count += self.problem[i].count(1)
            self.count = count

        elif self.id == 8:
            self.problem = [False] * self.size
            min = (0, 0)
            for tile in self.tile_list:
                if tile[0] > min[0]:
                    min = tile[0], tile[1]
            self.starting_pos = min[0] + 1, min[1] + 1
        elif self.id == 24:
            self.problem = [True] * self.size
            min = (0, 1000)
            for tile in self.tile_list:
                if tile[1] < min[1]:
                    min = tile
            self.starting_pos = min

    def validate_problem(self):
        self.completed = True

    def set_hovering(self, value):
        self.hovering = value

    def set_problem_try(self, value):
        self.show_feedback = True
        self.feedback_timer = pygame.time.get_ticks()
        self.problem = value

    def get_problem_size(self):
        if self.id == 23:
            return self.size, self.column_size, self.count
        else:
            return self.size

    def get_show_feedback(self):
        return self.show_feedback

    def get_completed(self):
        return self.completed

    def draw_rect(self, TILE_SIZE, scroll, color):
        screen = pygame.display.get_surface()
        if self.id == 23:
            rect = pygame.Rect(self.starting_pos[1] * TILE_SIZE - scroll,
                               (self.starting_pos[0] - self.size + 1) * TILE_SIZE
                               , self.column_size * TILE_SIZE, self.size * TILE_SIZE)

            pygame.draw.rect(screen, color, rect, 3)
            for i in range(self.size):
                pygame.draw.line(screen, color, (
                    self.starting_pos[1] * TILE_SIZE - scroll, (self.starting_pos[0] - self.size + 1 + i) * TILE_SIZE),
                                 ((self.starting_pos[1] + self.column_size) * TILE_SIZE - scroll,
                                  (self.starting_pos[0] - self.size + 1 + i) * TILE_SIZE))
            for i in range(self.column_size):
                pygame.draw.line(screen, color, (
                    (self.starting_pos[1] + i) * TILE_SIZE - scroll,
                    (self.starting_pos[0] - self.size + 1) * TILE_SIZE),
                                 ((self.starting_pos[1] + i) * TILE_SIZE - scroll,
                                  (self.starting_pos[0] - self.size + 1) * TILE_SIZE + self.size * TILE_SIZE))
        elif self.id == 8 or self.id == 24:
            rect = pygame.Rect(self.starting_pos[1] * TILE_SIZE - scroll, (self.starting_pos[0]) * TILE_SIZE,
                               self.size * TILE_SIZE, TILE_SIZE)
            for i in range(self.size):
                start_x = (self.starting_pos[1] + i) * TILE_SIZE - scroll
                start_y = (self.starting_pos[0]) * TILE_SIZE
                end_x = (self.starting_pos[1] + i) * TILE_SIZE - scroll
                end_y = (self.starting_pos[0]) * TILE_SIZE + TILE_SIZE
                pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 3)
            pygame.draw.rect(screen, color, rect, 3)

    def draw(self, player, scroll, TILE_SIZE, tiles_list):
        if self.id == 8:
            if self.completed:
                offset = 3
            else:
                offset = 0
            for key in self.tile_list:
                tile = self.tile_list[key]
                x = key[1] + offset
                y = key[0] + offset
                if self.completed:
                    offset -= 1
                t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (self.W, self.H), tiles_list[tile], tile)
                t.draw()
                if player and t.collide_rect(player):
                    player.is_colliding((t.x, t.y), key)
                elif player:
                    player.not_colliding(key)

        elif self.id == 23:
            initial_pos = 2, 0
            indexes = []
            for i, row in enumerate(self.problem):
                for j, value in enumerate(row):
                    if value == 1:
                        indexes.append((i, j))

            for index in indexes:
                y_offset = initial_pos[0] - index[0]
                x_offset = initial_pos[1] - index[1]
                tile = 9
                x = self.starting_pos[1] - x_offset
                y = self.starting_pos[0] - y_offset
                if self.completed:
                    x_offset += 1
                    y_offset -= 1
                t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (self.W, self.H), tiles_list[tile], tile)
                t.draw()
                if self.completed:
                    if player and t.collide_rect(player):
                        player.add_ladder((y, x))
                    else:
                        player.remove_ladder((y, x))

        elif self.id == 24:
            if self.completed:
                tile = 0
            else:
                tile = self.id
            for key in self.tile_list:
                x = key[1]
                y = key[0]
                t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (self.W, self.H), tiles_list[tile], tile)
                t.draw()
                if not self.completed:
                    if player and t.collide_rect(player):
                        player.set_finished()
                elif self.completed:
                    if player and t.collide_rect(player):
                        player.is_colliding((t.x, t.y), key)
                    elif player:
                        player.not_colliding(key)

        if self.hovering and not self.show_feedback:
            self.draw_rect(TILE_SIZE, scroll, (255, 253, 208))
        if self.show_feedback:
            if self.completed:
                color = "green"
            else:
                color = "red"
            self.draw_rect(TILE_SIZE, scroll, color)
            if pygame.time.get_ticks() > self.feedback_timer + 2000:
                self.show_feedback = False
                if self.id == 23 and not self.completed:
                    self.problem = self.original_problem.copy()
