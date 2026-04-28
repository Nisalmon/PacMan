import pygame as pg
from collections import deque
from player import Player


class Ghost:
    def __init__(self, name, visu, x, y, target):
        self.__name = name
        self.x = x
        self.y = y
        self._sprite_size = (32, 32)
        self._scaled = (24, 24)
        self._sheet = self.load_sprite_sheet()
        self.sprite = self.get_sprite((0, 0))
        self.path = []
        self.previous = ""
        self.__visu = visu
        self.target: Player = target
        self.speed = 48

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
                if self.__visu[y][x] == "█":
                    continue
                if self.__visu[ny][nx] == "█":
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

    def move_ghost(self, dt):
        target = (
                    int((self.target.x + self._scaled[0] / 2) // 32),
                    int((self.target.y + self._scaled[1] / 2) // 32)
                )
        if self.path:
            if self.path[0] == "UP":
                self.y -= self.speed * dt
            elif self.path[0] == "DOWN":
                self.y += self.speed * dt
            elif self.path[0] == "LEFT":
                self.x -= self.speed * dt
            elif self.path[0] == "RIGHT":
                self.x += self.speed * dt
            
            if len(self.path) >= 2 and self.can_move(self.path[1], dt, self.__visu):
                self.previous = self.path.pop(0)
            elif len(self.path) == 1:
                self.previous = self.path.pop(0)
            if (self.path and self.previous != self.path[0] and self.previous != ""):
                self.set_algo(target)
        else:
            self.set_algo(target)

    def can_move(self, dir, dt, visu) -> bool:
        check_x = self.x
        check_y = self.y

        if dir == "LEFT":
            check_x -= self.speed * dt
        elif dir == "RIGHT":
            check_x += self.speed * dt
        elif dir == "UP":
            check_y -= self.speed * dt
        elif dir == "DOWN":
            check_y += self.speed * dt

        center_x = int(check_x + self._scaled[0]/2)
        center_y = int(check_y + self._scaled[1]/2)

        grid_x1, grid_y1 = int((center_x) / 32), int(center_y / 32)
        grid_x2, grid_y2 = int((center_x + 30) / 32), int(center_y / 32)
        grid_x3, grid_y3 = int((center_x)/ 32), int((center_y + 30) / 32)
        grid_x4, grid_y4 = int((center_x + 30) / 32), int((center_y + 30) / 32)
        return (visu[grid_y1][grid_x1] == " " and
                visu[grid_y2][grid_x2] == " " and
                visu[grid_y3][grid_x3] == " " and
                visu[grid_y4][grid_x4] == " ")

    def snap_to_grid(self, tile_size=32, threshold=2):
        center_x = self.x + self._scaled[0] / 2
        center_y = self.y + self._scaled[1] / 2

        # centre de la case la plus proche
        target_x = round(center_x / tile_size) * tile_size
        target_y = round(center_y / tile_size) * tile_size

        # snap uniquement si proche du centre
        if abs(center_x - target_x) < threshold:
            center_x = target_x
        if abs(center_y - target_y) < threshold:
            center_y = target_y

        # remettre en coords sprite (top-left)
        self.x = center_x - self._scaled[0] / 2
        self.y = center_y - self._scaled[1] / 2
        


def draw_ghosts(screen, ghosts):
    for _, value in ghosts.items():
        screen.blit(value.sprite, (value.x, value.y))


def move_all_ghosts(ghosts, dt):
    for _, value in ghosts.items():
        value.move_ghost(dt)
