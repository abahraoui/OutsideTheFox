class InputBoxValidator:

    def __init__(self, player):
        self.text_list = []
        self.player = player
        self.queue = []

    def set_text(self, text_to_validate):
        self.text_list = text_to_validate

    def validate(self, scroll):
        if self.text_list:
            for text in self.text_list:
                if "P.moveRight()" in text:
                        self.queue.append(0)
                        self.player.add_to_queue(0, scroll)
                elif "P.moveLeft()" in text:
                        self.queue.append(1)
                        self.player.add_to_queue(1, scroll)
                elif "P.jump()" in text:
                        self.queue.append(-1)
                        self.player.add_to_queue(2, scroll)
                else:
                        print("Validation input error !")

    def get_queue(self):
        return self.queue
