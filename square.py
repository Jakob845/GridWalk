class square:
    id = ""
    obstacle = False
    deadEnd = False

    def __init__(self, id, obstacle, deadEnd):
        self.id = id
        self.obstacle = obstacle
        self.deadEnd = deadEnd