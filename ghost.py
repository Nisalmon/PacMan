import pygame as pg
from collections import deque


class Ghost:
    def __init__(self, name, visu, x, y):
        self.__name = name
        self.x = x
        self.y = y
        self._sprite_size = (32, 32)
        self._scaled = (24, 24)
        self._sheet = self.load_sprite_sheet()
        self.sprite = self.get_sprite((0, 0))
        self.path = []
        self.__visu = visu

    def load_sprite_sheet(self):
        if self.__name == "blinky":
            return pg.image.load("./sprite/blinky.png").convert_alpha()

    def get_sprite(self, loc, colorkey=(255, 255, 255)):
        x = loc[1] * self._sprite_size[0]
        y = loc[0] * self._sprite_size[1]

        rect = pg.Rect(x, y, *self._sprite_size)
        img = pg.Surface(self._sprite_size, pg.SRCALPHA).convert_alpha()
        img.blit(self._sheet, (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey, pg.RLEACCEL)
        return pg.transform.scale(img, (self._scaled[0],
                                        self._scaled[1]))

    def set_algo(self, target):
        if self.__name == "blinky":
            self.path = self.algo_blinky(target)

    def algo_blinky(self, target):
        queue = deque()
        visited = set()
        parent = {}
        s_x = int((self.x + self._scaled[0]/2) // 32)
        s_y = int((self.y + self._scaled[1]/2) // 32)
        DIRS = {
            "UP": (0, -1),
            "RIGHT": (1, 0),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
        }
        queue.append((s_x, s_y))
        visited.add((s_x, s_y))

        while queue:
            x, y = queue.popleft()
            if (x, y) == target:
                break

            for d in DIRS:
                dx, dy = DIRS[d]
                nx, ny = x + dx, y + dy

                height = len(self.__visu)
                width = len(self.__visu[0])
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                if d == "UP" and self.__visu[y][x] == "█":
                    continue
                if d == "DOWN" and self.__visu[y][x] == "█":
                    continue
                if d == "LEFT" and self.__visu[y][x] == "█":
                    continue
                if d == "RIGHT" and self.__visu[y][x] == "█":
                    continue

                if d == "UP" and self.__visu[ny][nx] == "█":
                    continue
                if d == "DOWN" and self.__visu[ny][nx] == "█":
                    continue
                if d == "LEFT" and self.__visu[ny][nx] == "█":
                    continue
                if d == "RIGHT" and self.__visu[ny][nx] == "█":
                    continue
                if (nx, ny) in visited:
                    continue
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = ((x, y), d)
        path = []
        cell = target
        if cell not in parent:
            return []
        while cell != (s_x, s_y):
            prev_cell, direction = parent[cell]
            path.append(direction)
            cell = prev_cell

        path.reverse()
        return path

    def move_ghost(self):
        if self.path[0] == "UP":
            self.y -= 32
        elif self.path[0] == "DOWN":
            self.y += 32
        elif self.path[0] == "LEFT":
            self.x -= 32
        elif self.path[0] == "RIGHT":
            self.x += 32
        self.path.pop(0)


def draw_ghosts(screen, ghosts):
    for _, value in ghosts.items():
        screen.blit(value.sprite, (value.x, value.y))


def move_all_ghosts(ghosts):
    for _, value in ghosts.items():
        value.move_ghost()
