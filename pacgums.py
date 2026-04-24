import pygame as pg
import random


class Pacgums:
    def __init__(self, x, y, _type="normal"):
        self.x = x
        self.y = y
        self._type = _type
        if _type == "super":
            self.sprite = pg.image.load("super_pacgum.png")
        else:
            self.sprite = pg.image.load("pacgum.png")


def load_pacgums(pacgums, nb_pacgums, maze_hexa, visu):
    visited = [[False for _ in range(len(maze_hexa))] for _ in range(len(maze_hexa[0]))]
    print(len(visited), len(visited[0]))
    if nb_pacgums > len(visited) * len(visited[0]):
        print("Cannot add all of the pacgums..")
        return 0
    cnt = 0
    while cnt < nb_pacgums:
        x, y = random.randint(0, len(visu[0]) - 1), random.randint(0, len(visu) - 1)
        print(x, y)
        print(int((x - 1) / 2), int((y - 1) / 2))
        if visu[y][x] != " " or visited[int((y - 1) / 2)][int((x - 1) / 2)] is True:
            continue
        pacgums.append(Pacgums(x * 32, y * 32))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    return 1


def draw_pacgums(pacgums, screen):
    for elem in pacgums:
        screen.blit(elem.sprite, (elem.x, elem.y))
