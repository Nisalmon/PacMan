import pygame as pg
import random
from typing import List, Any, Dict


class Pacgums:
    """
    Class for pacgums
    """
    def __init__(self, x: int, y: int, score: int,
                 _type: str = "normal") -> None:
        """
        To init attributs

        :attributs:
            - x : the x position for the pacgums

            - y : the y position for the pacgums

            - _type : type of the pacgum

            - score : the score

            - sprite : the sprite to load
        """
        self.x = x
        self.y = y
        self._type = _type
        self.score = score
        if _type == "super":
            self.sprite = pg.image.load("./sprite/super_pacgum.png")
        else:
            self.sprite = pg.image.load("./sprite/pacgum.png")


def load_pacgums(pacgums: List[Pacgums],
                 nb_pacgums: int,
                 maze_hexa: List[List[str]],
                 visu: List[List[str]],
                 conf: Dict[str, Any]) -> int:
    """
    To load pacgums

    :params:
        - pacgums : the pacgums

        - nb_pacgums : the number of pacgums

        - maze_hexa : the maze in hexa

        - visu : the maze visu

        - conf : the sprite to load

    :returns:
        Int : to know if the process failed or not
    """
    visited = [[False for _ in range(len(maze_hexa[0]))]
               for _ in range(len(maze_hexa))]
    if nb_pacgums > len(visited) * len(visited[0]):
        print("Cannot add all of the pacgums..")
        print("clamped to 100")
        nb_pacgums = 100
    cnt = 0
    super_pac_loc = [
        (1, 1),
        (len(visu[0]) - 2, 1),
        (1, len(visu) - 2),
        (len(visu[0]) - 2, len(visu) - 2)
    ]
    while cnt < 4 and cnt < nb_pacgums:
        x, y = super_pac_loc[cnt]
        if (visu[y][x] != " " or
           visited[int((y - 1) / 2)][int((x - 1) / 2)] is True or
           maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
            continue
        pacgums.append(Pacgums(x * 32 - 16, y * 32 - 16,
                               conf["points_per_super_pacgum"], "super"))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    while cnt < nb_pacgums:
        x = random.randint(0, len(visu[0]) - 1)
        y = random.randint(0, len(visu) - 1)
        if (visu[y][x] != " " or
           visited[int((y - 1) / 2)][int((x - 1) / 2)] is True or
           maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
            continue
        pacgums.append(Pacgums(x * 32 - 16, y * 32 - 16,
                               conf["points_per_pacgum"]))
        visited[int((y - 1) / 2)][int((x - 1) / 2)] = True
        cnt += 1
    return 1
