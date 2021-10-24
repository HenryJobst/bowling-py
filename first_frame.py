from frame import Frame


class FirstFrame(Frame):
    def __init__(self):
        super().__init__(1, None)

    def game_score(self):
        return self.frame_score()
