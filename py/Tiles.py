class Tiles:
    def __init__(self):
        self.temp = 1


class Ground(Tiles):
    def __init__(self):
        self.sprite = "Sprites\Tiles\Ground.png"

class Path(Tiles):
    def __init__(self):
        self.sprite = "Sprites\Tiles\Path.png"