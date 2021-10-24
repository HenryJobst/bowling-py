from first_frame import FirstFrame
from frame import Frame
from last_frame import LastFrame


class Game:

    def __init__(self):
        self.double_next = False
        self.frames = []
        self.actual_frame = None

    def next_frame(self) -> Frame:
        if len(self.frames) > 0:
            previous_frame = self.get_previous_frame()
            previous_frame_number = previous_frame.frame_number
            if previous_frame_number == 9:
                self.frames.append(LastFrame(previous_frame))
            else:
                self.frames.append(Frame(previous_frame_number + 1, previous_frame))
        else:
            self.frames.append(FirstFrame())

        return self.frames[-1]

    def log_to_console(self):
        print("\n--- Bowling-Game ---", flush=True)
        for frame in self.frames:
            frame.log_to_console()

    def get_previous_frame(self):
        if not self.frames or len(self.frames) < 1:
            return None

        return self.frames[-1]

    def get_last_finished_frame(self):
        if not self.frames or len(self.frames) < 1:
            return None

        frames_reversed = self.frames.copy()
        frames_reversed.reverse()
        for frame in frames_reversed:
            if frame.frame_finished():
                return frame

        return None

    def maybe_start_new_frame(self, pins) -> bool:
        if not self.actual_frame or self.actual_frame.frame_finished():
            # new frame started
            last_frame = self.get_last_finished_frame()
            if last_frame and last_frame.frame_cleared():
                # double first roll for last frame clearing
                last_frame.add_score(pins)
                if last_frame.frame_number == 9:
                    self.double_next = False
                if not last_frame.is_spare() and pins == 10:
                    if last_frame.frame_number < 9:
                        last_frame.add_score(pins)
                        if last_frame.frame_number < 9:
                            self.double_next = True
                elif not last_frame.is_spare() and last_frame.frame_number < 9:
                    self.double_next = True

            elif not self.actual_frame and pins == 10:
                # strike on first roll
                self.double_next = True

            self.actual_frame = self.next_frame()
            return True

        return False

    def roll(self, pins):
        new_frame_started = self.maybe_start_new_frame(pins)
        if not new_frame_started and self.double_next:
            last_frame = self.get_last_finished_frame()
            last_frame.add_score(pins)
            self.double_next = False

        self.actual_frame.roll(pins)

    def roll_many(self, rolls, pins):
        for roll in range(rolls):
            self.roll(pins)

    def roll_list(self, rolls: [int]):
        for pins in rolls:
            self.roll(pins)

    def score(self):
        self.log_to_console()
        game_score = 0
        for frame in self.frames:
            game_score += frame.frame_score()

        return game_score


def transform_symbols(rolls_as_str: str) -> [int]:
    """
    Idea to use this common representation and original python code by Juan L. Kehoe
        (https://juan0001.github.io/Calculate-the-bowling-score-using-a-machine-learning-model)

    Transform the rolls to scores based on the annotation of the symbols.
    Annotation of the symbols:
        "X" indicates a strike, "/" indicates a spare, "-" indicates a miss,
        and a number indicates the number of pins knocked down in the roll.
    For symbols:
        'X' -> 10
        '-' -> 0
        '/' -> N with N = 10 - 'previous roll pins'
    For numbers:
        Will transform the number in str to int.
    Parameters:
    -------
    rolls: list of str or int
        The rolls in a list that is retrieved from elsewhere.
    Returns:
    -------
    rolls: list of int
        A list of transformed rolls.
    """
    rolls = [0 for i in range(len(rolls_as_str))]
    for i in range(len(rolls_as_str)):
        # If it's 'X', it's strike. Set the score to 10.
        if rolls_as_str[i] == 'X':
            rolls[i] = 10
        # If it's '-', it's missed. Set the score to 0.
        elif rolls_as_str[i] == '-':
            rolls[i] = 0
        # If it's '/', it's spare, keep it for the record.
        elif rolls_as_str[i] == '/':
            if i > 0:
                rolls[i] = 10 - rolls[i - 1]
            else:
                rolls[i] = 10
        else:
            rolls[i] = int(rolls_as_str[i])
    return rolls
