class Cell:
    def __init__(self):
        self.hasBomb = False
        self.hasExploded = False
        self.flagged = False
        self.is_opened = False
        self.neighbours = 0
        self.flagged_bomb = False
        self.has_gotten_points = False

    def set_flagged(self, b):
        if self.hasBomb:
            self.flagged_bomb = True
        self.flagged = b

    def is_flagged(self):
        return self.flagged

    def get_fb(self):
        return self.flagged_bomb

    def open(self, b):
        self.is_opened = b

    def has_opened(self):
        return self.is_opened

    def is_a_bomb(self):
        return self.hasBomb

    def set_is_bomb(self, b):
        self.hasBomb = True

    def exploded(self):
        self.hasExploded = True