import tile as tile_class


class Bridge:

    def __init__(self, W, H, image_list, completed, tile_size, id, starting_pos=None):
        self.tile_list = image_list
        self.size = len(image_list)
        self.tile_size = tile_size
        self.completed = completed
        self.id = id
        self.W = W
        self.H = H
        self.starting_pos = starting_pos
        self.ladder_problem = [[0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 1, 1, 1]]

    def validate_problem(self):
        self.completed = True

    def set_ladder_problem(self, value):
        self.ladder_problem = value
    def get_completed(self):
        return self.completed

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
                if player and t.colliderect(player):
                    player.is_colliding((t.x, t.y), key)
                elif player:
                    player.not_colliding(key)
        elif self.id == 23:
            indexes = []

            # Iterate through rows
            for i, row in enumerate(self.ladder_problem):
                # Iterate through columns
                for j, value in enumerate(row):
                    # Check if the value is equal to the target value
                    if value == 1:
                        indexes.append((i, j))
            print(indexes)
            starting_pos = 2, 0

            for index in indexes:
                # if self.completed:
                # print(starting_pos[1], index[1])
                y_offset = starting_pos[0] - index[0]
                x_offset = starting_pos[1] - index[1]
                tile = 9
                # else:
                #     tile = self.id
                #     y_offset = 0
                #     x_offset = 0
                # print(x_offset, y_offset)
                x = 12 - x_offset
                y = 14 - y_offset
                if self.completed:
                    x_offset += 1
                    y_offset -= 1
                t = tile_class.Tile(x * TILE_SIZE - scroll, y * TILE_SIZE, (self.W, self.H), tiles_list[tile], tile)
                t.draw()
                if self.completed:
                    if player and t.colliderect(player):
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
                    if player and t.colliderect(player):
                        player.set_finished()
                elif self.completed:
                    if player and t.colliderect(player):
                        player.is_colliding((t.x, t.y), key)
                    elif player:
                        player.not_colliding(key)
