class Frame:

    def __init__(self, frame_number, previous_frame):
        self.first_roll = -1
        self.second_roll = -1
        self.addition = 0
        self.frame_number = frame_number
        self.previous_frame = previous_frame

    def first_roll_empty(self):
        return self.first_roll == -1

    def second_roll_empty(self):
        return self.second_roll == -1

    def first_roll_score(self):
        if self.first_roll_empty():
            return 0
        return self.first_roll

    def second_roll_score(self):
        if self.second_roll_empty():
            return 0
        return self.second_roll

    def frame_empty(self):
        return self.first_roll_empty()

    def frame_finished(self):
        return not self.second_roll_empty() or self.frame_cleared()

    def frame_cleared(self):
        return self.frame_score() >= 10

    def is_spare(self):
        return self.frame_cleared() and not self.second_roll_empty()

    def frame_score(self):
        if self.first_roll_empty():
            return 0
        elif self.second_roll_empty():
            return self.first_roll + self.addition
        else:
            return self.first_roll + self.second_roll + self.addition

    def game_score(self):
        return self.frame_score() + self.previous_frame.game_score()

    def roll(self, pins):
        if self.first_roll_empty():
            self.first_roll = pins
            return True  # consumed
        elif self.second_roll_empty():
            self.second_roll = pins
            return True  # consumed

        return False

    def add_score(self, score):
        self.addition += score
        if self.addition > 20:
            raise ValueError

    def log_to_console(self) -> str:
        print("----------")
        print("      Frame:", self.frame_number)
        print("    1. Roll:", self.first_roll_score())
        print("    2. Roll:", self.second_roll_score())
        self.log_to_console_3rd()
        print("   Addition:", self.addition)
        print("Frame-Score:", self.frame_score())
        print(" Game-Score:", self.game_score())

    def log_to_console_3rd(self):
        pass
