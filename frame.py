class Frame:

    def __init__(self, frame_number):
        self.first_roll = -1
        self.second_roll = -1
        self.third_roll = -1
        self.addition = 0
        self.frame_number = frame_number

    def first_roll_empty(self):
        return self.first_roll == -1

    def second_roll_empty(self):
        return self.second_roll == -1

    def frame_empty(self):
        return self.first_roll_empty()

    def frame_finished(self):
        if self.frame_number < 10:
            return not self.second_roll_empty() or self.frame_cleared()

        return False

    def frame_cleared(self):
        if self.frame_number < 10:
            return self.frame_score() >= 10

        return False

    def is_spare(self):
        return self.frame_cleared() and not self.second_roll_empty()

    def frame_score(self):
        if self.first_roll_empty():
            return 0 + self.addition
        elif self.second_roll_empty():
            return self.first_roll + self.addition
        elif self.third_roll == -1:
            return self.first_roll + self.second_roll + self.addition
        else:
            return self.first_roll + self.second_roll + self.third_roll + self.addition

    def roll(self, pins):
        if self.frame_empty():
            self.first_roll = pins
        elif self.second_roll_empty():
            self.second_roll = pins
        else:
            assert self.frame_number == 10
            self.third_roll = pins

    def add_score(self, score):
        self.addition += score
        if self.addition > 20:
            raise ValueError

