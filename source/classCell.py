class Cell:
    def __init__(self, x=0, y=0, id="", type="", name="", description="", cellText="", cellColor="darkgray", textColor="#000000",
                 nodeShape="", nodeColor="", pathColor="#000000", n="", e="", s="", w="", ne="", nw="", se="", sw=""):
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.cellText = cellText
        self.cellColor = cellColor
        self.textColor = textColor
        self.nodeShape = nodeShape
        self.nodeColor = nodeColor
        self.pathColor = pathColor
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.ne = ne
        self.nw = nw
        self.se = se
        self.sw = sw