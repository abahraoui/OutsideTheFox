import ast
import threading
from threading import Thread
from time import sleep

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
                allowed_vars = {"fox": self}
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
                    # feedback point player blocked right
                    self.queue.pop(0)
                    return 0, False
            case 1:
                if not self.player.get_blocked_left() and not self.player.get_lerping() and scroll > 0 and not self.player.jumping:
                    self.player.moveLeft(scroll)
                    goal_scroll = scroll - self.tileSize / 2
                    scrolling = True
                    self.queue.pop(0)
                    return goal_scroll, scrolling
                elif self.player.get_blocked_left() or scroll == 0:
                    # feedback point player blocked left (maybe hurt visually)
                    self.queue.pop(0)
                    return 0, False
            case 2:
                if not self.player.get_lerping() and not self.player.jumping and not self.player.falling:
                    self.player.jump()
                    self.queue.pop(0)
                    scrolling = False
                    return 0, scrolling
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
