import ast

import fox_class
import pygame
import user_execution_visitor


def execute_code(obj, allowed):
    exec(obj, allowed)


class InputBoxValidator:

    def __init__(self, player, tile_size, W):
        self.text_list = []
        self.player = player
        self.queue = []
        self.tileSize = tile_size
        self.W = W
        self.visitor = user_execution_visitor.UserExecutionVisitor()
        self.finished = True
        self.lastCooldown = 0
        self.lastQueueCooldown = 0
        self.fox = fox_class.Fox(self)

    def set_text(self, text_to_validate):
        self.text_list = text_to_validate

    def validate(self):
        self.finished = False
        if self.text_list:
            try:
                file = open('main/user_execution.py', 'w')
                for text in self.text_list:
                    # print(ast.parse(text).type_comment)

                    # print(sys.exc_info()[0])
                    file.write(text + "\n")

                file.close()
                file = open('main/user_execution.py', 'r').read()
                node = ast.parse(file.__str__())
                for elem in node.body:
                    self.visitor.visit(elem)
                    if isinstance(elem, ast.Expr) and elem.value and isinstance(elem.value, ast.Pass):
                        node.body.remove(elem)
                    # removes import statements
                    elif isinstance(elem, ast.Import):
                        node.body.remove(elem)

                obj = compile(node, filename="<ast>", mode="exec")
                # restricts the allowed variables to 'fox'.
                allowed_vars = {"fox": self.fox}
                execute_code(obj, allowed_vars)
                # thread = threading.Thread(target=execute_code, args=(obj, allowed_vars))
                # thread.start()
                # timer = threading.Timer(2, thread.terminate)
                # try:
                #     # Start the timer
                #     timer.start()
                #
                #     # Wait for the thread to finish
                #     thread.join()
                #
                # except Exception as e:
                #     print(f"An error occurred: {e}")
                #
                # finally:
                #     # Cancel the timer
                #     timer.cancel()


            except Exception as e:
                # feedback point e
                print(f"Yo it's {e.args}")

    def process_queue(self, scroll):
        match self.queue[0]:
            case 0:
                if not self.player.get_lerping() and not self.player.get_blocked_right() and not self.player.jumping and self.player.finishedCrouching:
                    self.player.moveRight()
                    if self.player.get_reach_right_boundary():
                        goal_scroll = scroll + self.tileSize / 2 + self.W - 427.5
                    else:
                        goal_scroll = 1
                    scrolling = True
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return goal_scroll, scrolling
                elif self.player.get_blocked_right() and self.player.finishedCrouching and not self.player.get_lerping():
                    # TODO feedback point player blocked right
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, False
            case 1:
                if not self.player.get_blocked_left() and not self.player.get_lerping() and scroll > 0 and not self.player.jumping and self.player.finishedCrouching:
                    self.player.moveLeft(scroll)
                    goal_scroll = - 1
                    scrolling = True
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return goal_scroll, scrolling
                elif self.player.get_blocked_left() or scroll == 0 and self.player.finishedCrouching and not self.player.get_lerping():
                    # TODO feedback point player blocked left (maybe hurt visually)
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, False
            case 2:
                # print(self.player.get_blocked_above(), self.player.finishedCrouching, self.player.get_lerping())
                if not self.player.get_lerping() and not self.player.get_blocked_above() and not self.player.jumping and not self.player.falling and self.player.finishedCrouching:
                    self.player.jump()
                    self.queue.pop(0)
                    scrolling = False
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, scrolling
                # TODO feedback point player blocked above
                elif self.player.get_blocked_above() and self.player.finishedCrouching and not self.player.get_lerping():
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, False

            case 3:
                if not self.player.get_lerping() and not self.player.jumping and not self.player.falling:
                    self.player.crouch()
                    self.queue.pop(0)
                    scrolling = False
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, scrolling
            case 4:
                if not self.player.get_lerping() and not self.player.jumping and not self.player.falling:
                    self.player.climbUp()
                    self.queue.pop(0)
                    scrolling = False
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, scrolling
                # TODO feedback point player cant climb
                elif not self.player.canClimb:
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, False
            case 5:
                print(self.player.get_lerping(), self.player.jumping, self.player.falling, self.player.get_blocked_below(), self.player.canClimb)
                if not self.player.get_lerping() and not self.player.jumping and not self.player.get_blocked_below() and self.player.canClimb:
                    self.player.climbDown()
                    self.queue.pop(0)
                    scrolling = False
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, scrolling
                # TODO feedback point player cant climb or cant climb
                elif self.player.get_blocked_below() or not self.player.canClimb and pygame.time.get_ticks() > self.lastQueueCooldown + 500:
                    print(self.player.ladders)
                    print(self.player.get_blocked_below() or not self.player.canClimb and pygame.time.get_ticks() > self.lastQueueCooldown + 500)
                    self.queue.pop(0)
                    self.lastQueueCooldown = pygame.time.get_ticks()
                    return 0, False

            case _:
                print("Not an action.")

    def get_queue(self):
        if not self.queue and not self.finished:
            self.finished = True
            self.lastCooldown = pygame.time.get_ticks()
        return self.queue

    def isDone(self):
        if self.finished and pygame.time.get_ticks() > self.lastCooldown + 800:
            return True
        else:
            return False

    def moveRight(self):
        self.queue.append(0)

    def moveLeft(self):
        self.queue.append(1)

    def jump(self):
        self.queue.append(2)

    def crouch(self):
        self.queue.append(3)

    def climbUp(self):
        self.queue.append(4)

    def climbDown(self):
        self.queue.append(5)
