import pygame as pg
import random


class Pacgums:
    def __init__(self, x, y, _type="normal"):
        self.x = x
        self.y = y
        self._type = _type
        if _type == "super":
            self.sprite = pg.image.load("./sprite/super_pacgum.png")
        else:
            self.sprite = pg.image.load("./sprite/pacgum.png")


def load_pacgums(pacgums, nb_pacgums, maze_hexa, visu):
    visited = [[False for _ in range(len(maze_hexa[0]))]
               for _ in range(len(maze_hexa))]
    if nb_pacgums > len(visited) * len(visited[0]):
        print("Cannot add all of the pacgums..")
        return 0
    cnt = 0
    print(len(visu), len(visu[0]))
    print(len(visited), len(visited[0]))
    while cnt < nb_pacgums:
        x = random.randint(0, len(visu[0]) - 1)
        y = random.randint(0, len(visu) - 1)
        # print(x,y, "aaa", int((x-1)/2), int((y-1)/2))
        if (visu[y][x] != " " or
           visited[int((y - 1) / 2)][int((x - 1) / 2)] is True or
           maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
            continue
        pacgums.append(Pacgums(x * 32 - 16, y * 32 - 16))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    return 1


def draw_pacgums(pacgums, screen):
    for elem in pacgums:
        screen.blit(elem.sprite, (elem.x, elem.y))
