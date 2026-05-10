import pygame as pg
import random


class Pacgums:
    def __init__(self, x, y, score, _type="normal"):
        self.x = x
        self.y = y
        self._type = _type
        self.score = score
        if _type == "super":
            self.sprite = pg.image.load("./sprite/super_pacgum.png")
        else:
            self.sprite = pg.image.load("./sprite/pacgum.png")


def load_pacgums(pacgums, nb_pacgums, maze_hexa, visu, conf):
    visited = [[False for _ in range(len(maze_hexa[0]))]
               for _ in range(len(maze_hexa))]
    if nb_pacgums > len(visited) * len(visited[0]):
        print("Cannot add all of the pacgums..")
        return 0
    cnt = 0
    while cnt < nb_pacgums - 4:
        x = random.randint(0, len(visu[0]) - 1)
        y = random.randint(0, len(visu) - 1)
        if (visu[y][x] != " " or
           visited[int((y - 1) / 2)][int((x - 1) / 2)] is True or
           maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
            continue
        pacgums.append(Pacgums(x * 32 - 16, y * 32 - 16, conf["points_per_pacgum"]))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    while cnt < nb_pacgums:
        x = random.randint(0, len(visu[0]) - 1)
        y = random.randint(0, len(visu) - 1)
        if (visu[y][x] != " " or
           visited[int((y - 1) / 2)][int((x - 1) / 2)] is True or
           maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
            continue
        pacgums.append(Pacgums(x * 32 - 16, y * 32 - 16, conf["points_per_super_pacgum"],"super"))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    return 1
