class InputBoxValidator:

    def __init__(self, player, tile_size, W):
        self.text_list = []
        self.player = player
        self.queue = []
        self.tileSize = tile_size
        self.W = W

    def set_text(self, text_to_validate):
        self.text_list = text_to_validate

    def validate(self):
        if self.text_list:
            for text in self.text_list:
                if "P.moveRight()" in text:
                    self.queue.append(0)
                elif "P.moveLeft()" in text:
                    self.queue.append(1)
                elif "P.jump()" in text:
                    self.queue.append(2)
                else:
                    print("")  # print("Validation input error !")

    def process_queue(self, scroll):
        match self.queue[0]:
            case 0:

                if not self.player.get_lerping() and not self.player.get_blocked_right() and not self.player.jumping:
                    self.player.moveRight()
                    if self.player.get_reach_right_boundary():
                        goal_scroll = scroll + self.tileSize / 2 + self.W - 427.5
                    else:
                        goal_scroll = scroll + self.tileSize / 2
                    scrolling = True
                    self.queue.pop(0)
                    return goal_scroll, scrolling
                elif self.player.get_blocked_right():
                    self.queue.pop(0)
                    return 0, False
            case 1:
                if not self.player.get_blocked_left() and not self.player.get_lerping() and scroll > 0:
                    self.player.moveLeft(scroll)
                    goal_scroll = scroll - self.tileSize / 2
                    scrolling = True
                    self.queue.pop(0)
                    return goal_scroll, scrolling
                elif self.player.get_blocked_left() or scroll == 0:
                    self.queue.pop(0)
                    return 0, False
            case 2:
                if not self.player.get_lerping() and not self.player.jumping:
                    self.player.jump()
                    self.queue.pop(0)
                    scrolling = False
                    return 0, scrolling
            case _:
                print("Not an action.")


    def get_queue(self):
        return self.queue
