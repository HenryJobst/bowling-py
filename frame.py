MAX_PINS = 10


class Frame:

    def __init__(self, frame_number, previous_frame):
        self.first_roll = -1
        self.second_roll = -1
        self.bonus = 0
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

    def second_roll_score(self, as_int=True):
        if self.second_roll_empty():
            if as_int:
                return 0
            else:
                return "-"
        return self.second_roll

    def frame_empty(self):
        return self.first_roll_empty()

    def frame_finished(self):
        return not self.second_roll_empty() or self.frame_cleared()

    def frame_cleared(self):
        return self.frame_score() >= MAX_PINS

    def is_spare(self):
        return self.frame_cleared() and not self.second_roll_empty()

    def is_strike(self):
        return self.frame_cleared() and self.second_roll_empty()

    def frame_score(self):
        if self.first_roll_empty():
            return 0
        elif self.second_roll_empty():
            return self.first_roll + self.bonus
        else:
            return self.first_roll + self.second_roll + self.bonus

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

    def add_bonus(self, score):
        self.bonus += score
        if self.bonus > 2 * MAX_PINS:
            raise ValueError

    def log_to_console(self):
        print("----------")
        print("      Frame:", self.frame_number)
        print("    1. Roll:", self.first_roll_score())
        print("    2. Roll:", self.second_roll_score(False))
        self.log_to_console_3rd()
        print("      Bonus:", self.bonus)
        print("Frame-Score:", self.frame_score())
        print(" Game-Score:", self.game_score())

    def log_to_console_3rd(self):
        pass

    def add_bonus_to_previous_frames(self):
        if self.previous_frame.frame_cleared():
            self.add_bonus_for_first_roll()
        if self.previous_frame.is_strike():
            self.add_bonus_for_second_roll()

    def add_bonus_for_first_roll(self):
        self.previous_frame.add_bonus(self.first_roll_score())
        if self.previous_frame.is_strike():
            self.add_bonus_to_second_previous_frame(self.first_roll_score())

    def add_bonus_for_second_roll(self):
        self.previous_frame.add_bonus(self.second_roll_score())

    def add_bonus_to_second_previous_frame(self, pins):
        prev_previous_frame = self.previous_frame.previous_frame
        if prev_previous_frame and prev_previous_frame.is_strike():
            # double strike -> add bonus to second previous frame
            self.previous_frame.previous_frame.add_bonus(pins)
