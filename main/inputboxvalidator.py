import ast
import pickle
import subprocess
import sys

import pygame

import user_execution_visitor
from pathlib import Path


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
            file = open('main/user_execution.py', 'w')
            for text in self.text_list:
                print(text)
                try:

                    ast.parse(text)  # + "\nP")
                    # print("y")
                    # print(ast.parse(text).type_comment)

                except:
                    print("")
                    # print(sys.exc_info()[0])
                # print(text + "\nP")
                # print("Done")
                file.write(text + "\n")
                # if "P.moveRight()" in text:
                #     self.queue.append(0)
                # elif "P.moveLeft()" in text:
                #     self.queue.append(1)
                # elif "P.jump()" in text:
                #     self.queue.append(2)
                # else:
                #     print("")  # print("Validation input error !")
            file.close()
            file = open('main/user_execution.py', 'r').read()
            node = ast.parse(file.__str__())
            for elem in node.body:
                self.visitor.visit(elem)
                if elem.value and isinstance(elem.value,ast.Pass):
                    node.body.remove(elem)
            print(ast.dump(node))
            fox = self
            obj = compile(node, filename="<ast>", mode="exec")
            exec(obj)

    def process_queue(self, scroll):
        match self.queue[0]:
            case 0:
                print(self.player.get_location(),"PLAYER")
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
                if not self.player.get_blocked_left() and not self.player.get_lerping() and scroll > 0 and not self.player.jumping:
                    self.player.moveLeft(scroll)
                    goal_scroll = scroll - self.tileSize / 2
                    scrolling = True
                    self.queue.pop(0)
                    return goal_scroll, scrolling
                elif self.player.get_blocked_left() or scroll == 0:
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
