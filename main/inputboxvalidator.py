import ast
import sys
import usermanual

import fox_class
import pygame
import user_execution_visitor


def execute_code(obj, allowed):
    return exec(obj, allowed)


class InputBoxValidator:

    def __init__(self, player, tile_size, W, error_rect):
        self.text_list = []
        self.player = player
        self.queue = []
        self.tileSize = tile_size
        self.W = W
        self.visitor = user_execution_visitor.UserExecutionVisitor()
        self.user_error_feedback_rect = error_rect
        self.finished = True
        self.lastCooldown = 0
        self.lastQueueCooldown = 0
        self.fox = fox_class.Fox(self)
        self.error_feedback = []
        self.errorLine = None
        self.screen = pygame.display.get_surface()
        self.feedback_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        self.fox_feedback = []
        self.fox_feedback_surfaces = []
        self.fox_feedback_rect = None
        self.show_feedback = False
        self.show_feedback_timer = pygame.time.get_ticks()
        self.mode = "Player"
        self.problem_completed = False
        self.problem_try = None
        self.problem_size = 0

    def set_text(self, text_to_validate):
        self.text_list = text_to_validate
        self.error_feedback = []
        self.errorLine = None

    def set_problem_completed(self, value):
        self.problem_completed = value

    def set_mode(self, value):
        self.mode = value

    def validate(self):
        self.finished = False
        if self.text_list:
            try:
                file = open('main/user_execution.py', 'w')
                for text in self.text_list:
                    file.write(text + "\n")
                if self.mode == "Bridge":
                    file.write("fox.validate(bridge)")
                elif self.mode == "Ladder":
                    file.write("fox.validate(ladder)")
                elif self.mode == "Spike":
                    file.write("fox.validate(spike)")
                file.close()
                file = open('main/user_execution.py', 'r').read()
                node = ast.parse(file.__str__())
                for elem in node.body:
                    self.visitor.visit(elem)
                    if isinstance(elem, ast.Expr) and elem.value and isinstance(elem.value, ast.Pass):
                        print(elem)
                        node.body.remove(elem)
                    # removes import statements
                    elif isinstance(elem, ast.Import):
                        node.body.remove(elem)
                obj = compile(node, filename="<ast>", mode="exec")
                # restricts the allowed variables to 'fox'.
                allowed_vars = {"fox": self.fox}
                if self.mode == "Bridge":
                    allowed_vars = {"fox": self.fox, "bridge": []}
                elif self.mode == "Ladder":
                    allowed_vars = {"fox": self.fox, "ladder": [[0, 0, 0, 0],[0, 0, 0, 0],[0, 1, 1, 1]]}
                elif self.mode == "Spike":
                    allowed_vars = {"fox": self.fox, "spike": [True, True, True]}

                execute_code(obj, allowed_vars)

            except Exception as e:
                # feedback point e
                print(f"Yo it's {e.args}")
                print(sys.exc_info())
                # for info in sys.exc_info():
                exc_type, exc_value, exc_traceback = sys.exc_info()

                if not issubclass(e.__class__, SyntaxError):
                    while exc_traceback.tb_next:
                        exc_traceback = exc_traceback.tb_next

                    line_number = exc_traceback.tb_lineno
                else:
                    line_number = exc_value.end_lineno

                self.error_feedback.append(f"Error occurred at line {line_number}")
                self.errorLine = line_number
                self.error_feedback.append(str(exc_value))
            if self.errorLine is not None:
                self.queue = []

    def has_error(self):
        return self.errorLine is not None

    def get_mode(self):
        return self.mode
    def get_error_line(self):
        return self.errorLine

    def get_error_feedback(self):
        return self.error_feedback

    def draw_error_feedback(self):
        start_y = self.user_error_feedback_rect.top
        text_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render(self.error_feedback[0], True,
                                                                                   (255, 255, 255))
        self.screen.blit(text_surface, (self.user_error_feedback_rect.left + 30, start_y))
        text_surfaces = []
        limit = self.user_error_feedback_rect.bottom - 10
        usermanual.parse_text(self.error_feedback[1], text_surfaces, self.feedback_font, limit,
                              self.user_error_feedback_rect.width)

        for i in range(len(text_surfaces)):
            current_surface = text_surfaces[i]
            self.screen.blit(current_surface[0], (self.user_error_feedback_rect.left + 30, start_y + 25 * (i + 1)))

    def process_fox_feedback(self):
        x, y = self.player.get_location()
        self.fox_feedback_surfaces = []
        self.fox_feedback_rect = pygame.Rect(x - 100, y - 300, 500, 200)
        current_text = self.fox_feedback[0]
        text = self.fox_feedback[0]
        match current_text:
            case "canClimb":
                text = str(self.canClimb()) + (", I can climb." if self.canClimb() else ", I cannot climb.")
            case "canMoveRight":
                text = str(self.canMoveRight()) + (", I can move right." if self.canMoveRight() else ", I cannot move right.")
            case "canMoveLeft":
                text = str(self.canMoveLeft()) + (", I can move left." if self.canMoveLeft() else ", I cannot move left.")
            case "canJump":
                text = str(self.canJump()) + (", I can jump." if self.canJump() else ", I cannot jump.")
            case _:
                text = current_text
        if not isinstance(text, str):
            text = "This is not a valid string."
        limit = self.fox_feedback_rect.height - 50
        usermanual.parse_text(text, self.fox_feedback_surfaces, self.feedback_font, limit,
                              self.fox_feedback_rect.width)
        self.fox_feedback.pop(0)
        self.show_feedback = True
        self.show_feedback_timer = pygame.time.get_ticks()

    def draw_fox_feedback(self):
        navy = (0, 0, 128)
        page = 1
        start_y = self.fox_feedback_rect.top + 5
        x, y = self.player.get_location()
        pygame.draw.polygon(self.screen, navy,
                            [(x + 35, y - 40), (x + 100, y - 100), (x + 400, y - 100), (x + 400, y - 300),
                             (x - 100, y - 300), (x - 100, y - 100), (x + 35, y - 100)])
        self.fox_feedback_rect = pygame.Rect(x - 100, y - 300, 500, 200)

        pygame.draw.rect(self.screen, 'green', self.fox_feedback_rect, 3, 3)
        pygame.draw.line(self.screen, 'green', (x + 35, y - 40), (x + 100, y - 100), 3)
        pygame.draw.line(self.screen, 'green', (x + 35, y - 40), (x + 35, y - 100), 3)
        text_surfaces = [x for x in self.fox_feedback_surfaces if x[1] == page]
        for i in range(len(text_surfaces)):
            current_surface = text_surfaces[i]
            self.screen.blit(current_surface[0], (self.fox_feedback_rect.topleft[0] + 5, start_y + 25 * i))
        if self.mode != 'Player':
            cooldown = 3000
        else:
            cooldown = 1500
        if pygame.time.get_ticks() > self.show_feedback_timer + cooldown:
            self.show_feedback = False

    def process_queue(self, scroll):
        if pygame.time.get_ticks() > self.lastQueueCooldown + 750:
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
                        self.set_fox_feedback("Ouch I cannot move right, I am blocked!")
                        self.process_fox_feedback()
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
                        self.set_fox_feedback("Unfortunately I cannot move left, I am blocked!")
                        self.process_fox_feedback()
                        self.queue.pop(0)
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, False
                case 2:
                    if not self.player.get_lerping() and not self.player.get_blocked_above() and not self.player.jumping and not self.player.falling and self.player.finishedCrouching:
                        self.player.jump()
                        self.queue.pop(0)
                        scrolling = False
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, scrolling
                    elif self.player.get_blocked_above() and self.player.finishedCrouching and not self.player.get_lerping():
                        self.set_fox_feedback("Oops I cannot jump above, I am blocked!")
                        self.process_fox_feedback()
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
                    if not self.player.get_lerping() and not self.player.jumping and not self.player.falling and self.player.canClimb:
                        self.player.climbUp()
                        self.queue.pop(0)
                        scrolling = False
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, scrolling
                    elif not self.player.canClimb:
                        self.set_fox_feedback("Sadly I cannot climb up, there is no valid ladder!")
                        self.process_fox_feedback()
                        self.queue.pop(0)
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, False
                case 5:
                    if not self.player.get_lerping() and not self.player.jumping and not self.player.get_blocked_below() and self.player.canClimb:
                        self.player.climbDown()
                        self.queue.pop(0)
                        scrolling = False
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, scrolling
                    elif self.player.get_blocked_below() or not self.player.canClimb:  # and pygame.time.get_ticks() >
                        # self.lastQueueCooldown + 500:
                        self.set_fox_feedback("Darn I cannot climb down, there is no ladder or a floor tile is blocking me!")
                        self.process_fox_feedback()
                        self.queue.pop(0)
                        self.lastQueueCooldown = pygame.time.get_ticks()
                        return 0, False
                case 6:
                    if not self.show_feedback:
                        self.process_fox_feedback()
                        self.queue.pop(0)
                        return 0, False
                case _:
                    print("Not an action.")

    def get_queue(self):
        if not self.queue and not self.finished:
            self.finished = True
            self.lastCooldown = pygame.time.get_ticks()
        return self.queue

    def get_problem_completed(self):
        return self.problem_completed

    def get_problem_try(self):
        return self.problem_try

    def isDone(self):
        if self.finished and pygame.time.get_ticks() > self.lastCooldown + 800:
            return True
        else:
            return False

    def set_problem_size(self, value):
        self.problem_size = value

    def get_problem_size(self):
        return self.problem_size

    def set_fox_feedback(self, text):
        self.fox_feedback.insert(0, text)

    '''Callback functions used by the fox_class.'''

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

    def canClimb(self):
        return self.player.canClimb

    def canMoveRight(self):
        return not self.player.get_blocked_right()

    def canMoveLeft(self):
        return not self.player.get_blocked_left()

    def canJump(self):
        return not self.player.get_blocked_above()

    def say(self, text):
        self.queue.append(6)
        self.set_fox_feedback(text)

    def set_problem_try(self, value):
        self.problem_try = value
