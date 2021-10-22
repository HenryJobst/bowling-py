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
            last_frame_number = self.get_last_frame().frame_number
            if last_frame_number == 9:
                self.frames.append(LastFrame())
            else:
                self.frames.append(Frame(last_frame_number + 1))
        else:
            self.frames.append(FirstFrame())

        return self.frames[-1]

    def to_string(self):
        print("\n--- Bowling-Game ---", flush=True)
        for frame in self.frames:
            print("* Frame   : ", frame.frame_number, flush=True)
            print("  Score   : ", frame.frame_score(), flush=True)
            print("  Addition: ", frame.addition, flush=True)

    def get_last_frame(self):
        if not self.frames or len(self.frames) < 1:
            return None

        return self.frames[-1]

    def get_last_finished_frame(self) -> Frame:
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
                    if last_frame.frame_number < 10:
                        last_frame.add_score(pins)
                        if last_frame.frame_number < 9:
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

    def score(self):
        self.to_string()
        game_score = 0
        for frame in self.frames:
            game_score += frame.frame_score()

        return game_score
