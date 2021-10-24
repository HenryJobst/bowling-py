from frame import Frame, MAX_PINS


class LastFrame(Frame):
    def __init__(self, previous_frame):
        super().__init__(10, previous_frame)
        self.third_roll = -1

    def third_roll_empty(self):
        return self.third_roll == -1

    def third_roll_score(self):
        if self.third_roll_empty():
            return 0
        return self.third_roll

    def frame_score(self):
        if self.third_roll_empty():
            return super().frame_score()
        else:
            return super().frame_score() + self.third_roll

    def frame_cleared(self):
        return False

    def frame_finished(self):
        if not self.third_roll_empty():
            return True
        if not super().is_strike() and not self.second_roll_empty() and \
                super().frame_score() < MAX_PINS:
            return True

        return False

    def is_spare(self):
        return False

    def roll(self, pins):
        if not super().roll(pins):
            # not consumed
            self.third_roll = pins

    def log_to_console_3rd(self):
        print("    3. Roll:", self.third_roll_score())

    def add_bonus_to_previous_frames(self):
        super().add_bonus_to_previous_frames()
