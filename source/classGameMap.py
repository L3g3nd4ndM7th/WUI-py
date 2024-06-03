class GameMap:
    def __init__(self, name="Default Map", height=10, width=10, start=[0, 0], cells=[]):
        self.name = name
        self.height = height
        self.width = width
        self.start = start
        self.cells = cells