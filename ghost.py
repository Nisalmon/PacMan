import pygame as pg
from collections import deque
from player import Player
import random
from typing import Dict, List, Optional, Union, Tuple


class Ghost:
    def __init__(self, name, visu, maze_hexa, x, y, target, red):
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
        self.__maze_hexa = maze_hexa
        self.target: Player = target
        self.speed = 56
        if self.__name == "inky" or self.__name == "pinky":
            self.red = red

        self.target_pos = None
        self.rand_target = self.get_rand_target(self.__maze_hexa, self.__visu)
        self.frame = 0

    def load_sprite_sheet(self):
        if self.__name == "blinky":
            return pg.image.load("./sprite/blinky.png").convert_alpha()
        elif self.__name == "inky":
            return pg.image.load("./sprite/inky.png").convert_alpha()
        elif self.__name == "pinky":
            return pg.image.load("./sprite/pinky.png").convert_alpha()
        else:
            return pg.image.load("./sprite/clyde.png").convert_alpha()

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
        self.target_pos = target
        if self.__name == "blinky":
            self.path = self.algo_blinky(target)
        elif self.__name == "pinky":
            self.path = self.algo_blinky(self.get_pinky_target(target, self.target.direction[0] if self.target.direction else "",
                                                               self.__visu))
        elif self.__name == "inky":
            self.path = self.algo_blinky(self.get_inky_target((int((self.red.x + self._scaled[0]/2) // 32),
                                                               int((self.red.y + self._scaled[1]/2) // 32)),
                                                               target, self.target.direction[0] if self.target.direction else "",
                                                               self.__visu))
        else:
            if len(self.algo_blinky(target)) <= 8:
                self.path = self.algo_blinky(self.rand_target)
            else:
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
                # if self.__visu[y][x] == "█":
                #     continue
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
        self.frame += 1
        direction = ["UP", "DOWN", "LEFT", "RIGHT"]
        if self.previous in direction and self.can_move(self.previous, dt, self.__visu) and not (self.path and self.can_move(self.path[0], dt, self.__visu)):
            if not set(self.path) == {self.previous}:
                self.set_algo(target)
            if self.previous == "UP":
                self.y -= self.speed * dt
            elif self.previous == "DOWN":
                self.y += self.speed * dt
            elif self.previous == "LEFT":
                self.x -= self.speed * dt
            elif self.previous == "RIGHT":
                self.x += self.speed * dt
            if self.frame % 15 == 0 and self.__name == "clyde":
                print("A")
                print(self.path)
        elif self.path and self.can_move(self.path[0], dt, self.__visu):
            if self.frame % 15 == 0 and self.__name == "clyde":
                print(self.path)
                print("B")
            if self.path[0] == "UP":
                self.y -= self.speed * dt
            elif self.path[0] == "DOWN":
                self.y += self.speed * dt
            elif self.path[0] == "LEFT":
                self.x -= self.speed * dt
            elif self.path[0] == "RIGHT":
                self.x += self.speed * dt

            if len(self.path) >= 2 and self.can_move(self.path[0], dt, self.__visu):
                self.previous = self.path.pop(0)
            elif len(self.path) == 1:
                self.previous = self.path.pop(0)
        else:
            self.set_algo(target)
            # if self.frame % 15 == 0 and self.__name == "inky":
            #     print("C")
            #     print(self.red.x, self.red.y)
            #     print(self.path)
        # if not self.path:
        #     self.set_algo(target)
        # elif self.frame % 10 == 0:
        #     self.set_algo(target)

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

        grid_x1, grid_y1 = int((center_x) / 32), int((center_y) / 32)
        grid_x2, grid_y2 = int((center_x + 30) / 32), int((center_y) / 32)
        grid_x3, grid_y3 = int((center_x) / 32), int((center_y + 30) / 32)
        grid_x4, grid_y4 = int((center_x + 30) / 32), int((center_y + 30) / 32)
        return (visu[grid_y1][grid_x1] == " " and
                visu[grid_y2][grid_x2] == " " and
                visu[grid_y3][grid_x3] == " " and
                visu[grid_y4][grid_x4] == " ")

    def get_inky_target(self, red_pos, pac_pos, pac_dir,  visu):
        pac_x, pac_y = pac_pos
        red_x, red_y = red_pos
        pivot_x, pivot_y = (pac_x, pac_y)
        if pac_dir:
            if pac_dir[0] == "UP":
                pivot_x, pivot_y = (pac_x, pac_y - 2)
            elif pac_dir[0] == "RIGHT":
                pivot_x, pivot_y = (pac_x + 2, pac_y)
            elif pac_dir[0] == "DOWN":
                pivot_x, pivot_y = (pac_x, pac_y + 2)
            elif pac_dir[0] == "LEFT":
                pivot_x, pivot_y = (pac_x - 2, pac_y)
            vector = (pivot_x + (pivot_x - red_x), pivot_y + (pivot_y - red_y))
            target_x = max(0, min(vector[0], len(visu[0]) - 1))
            target_y = max(0, min(vector[1], len(visu) - 1))
            count = 0
            while visu[target_y][target_x] == "█":
                count += 1
                if count > 50:
                    print("INFINITE LOOP PREVENTED")
                    break
                if target_x > pac_x:
                    target_x -= 1
                elif target_x < pac_x:
                    target_x += 1
                if visu[target_y][target_x] != "█":
                    break
                if target_y > pac_y:
                    target_y -= 1
                elif target_y < pac_y:
                    target_y += 1

            return (target_x, target_y)
        else:
            return pac_pos

    def get_pinky_target(self, pac_pos, pac_dir,  visu):
        pac_x, pac_y = pac_pos
        pivot_x, pivot_y = (pac_x, pac_y)
        if pac_dir:
            if pac_dir[0] == "UP":
                pivot_x, pivot_y = (pac_x, pac_y - 4)
            elif pac_dir[0] == "RIGHT":
                pivot_x, pivot_y = (pac_x + 4, pac_y)
            elif pac_dir[0] == "DOWN":
                pivot_x, pivot_y = (pac_x, pac_y + 4)
            elif pac_dir[0] == "LEFT":
                pivot_x, pivot_y = (pac_x - 4, pac_y)
            target_x = max(0, min(pivot_x, len(visu[0]) - 1))
            target_y = max(0, min(pivot_y, len(visu) - 1))
            count = 0
            while visu[target_y][target_x] == "█":
                count += 1
                if count > 50:
                    print("INFINITE LOOP PREVENTED")
                    break
                if target_x > pac_x:
                    target_x -= 1
                elif target_x < pac_x:
                    target_x += 1
                if visu[target_y][target_x] != "█":
                    break
                if target_y > pac_y:
                    target_y -= 1
                elif target_y < pac_y:
                    target_y += 1

            return (target_x, target_y)
        else:
            return pac_pos

    def get_rand_target(self, maze_hexa, visu):
        while True:
            x = random.randint(0, len(visu[0]) - 1)
            y = random.randint(0, len(visu) - 1)
            if (visu[y][x] != " " or
               maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
                continue
            if visu[y][x] == " ":
                print(x, y)
                return (x, y)


def init_ghosts(conf, visu, pacman, maze_hexa) -> Dict[str, Ghost]:
    w = conf['width']
    h = conf['height']
    ghosts = {
        "blinky": Ghost("blinky", visu, maze_hexa, 20, 20, pacman, None),
        "clyde": Ghost("clyde", visu, maze_hexa, 20, (h - 1) * 64 + 20, pacman, None),
    }
    ghosts.update({"inky": Ghost("inky", visu, maze_hexa, (w - 1) * 64 + 20, 20, pacman, ghosts['blinky'])})
    ghosts.update({"pinky": Ghost("pinky", visu, maze_hexa, (w - 1) * 64 + 20, (h - 1) * 64 + 20, pacman, ghosts['blinky'])})
    return ghosts


def draw_ghosts(screen, ghosts) -> None:
    for _, value in ghosts.items():
        screen.blit(value.sprite, (value.x, value.y))
        pg.draw.rect(screen, (0, 255, 0), (value.x + value._scaled[0]/2, value.y + value._scaled[1]/2, 30, 30), 1)


def move_all_ghosts(ghosts, dt) -> None:
    for _, value in ghosts.items():
        value.move_ghost(dt)
