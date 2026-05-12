class Cells:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def init_cells(visu):
    cells = []
    for i in range(len(visu)):
        for j in range(len(visu[0])):
            if visu[i][j] == "█":
                cells.append(Cells(j*32, i*32))
    return cells
