from __future__ import annotations
import pygame as pg
from collections import deque
import random
from typing import Dict, List, Tuple, Deque, Any
import time


BASE_SPEED = 56
DEFAULT_SCALE = 24


class Ghost:
    """
    Class for the ghost

    :methods:
        - get_scale : to get the scale

        - load_sprite_sheet : load all the sprite

        - get_sprite : to get the sprite

        - set_algo : apply the correct algo to the ghost

        - algo_blinky : the BFS algorithm

        - move_ghost : To move the ghost in the maze

        - can_move : check if the ghost can move to the next direction

        - get_pinky_target : To get the next target of pinky

        - get_inky_target : To get the next target of inky

        - get_rand_target : To get a random target

        - get_tolerance : to get the tolerance
    """
    def __init__(self,
                 name: str, score: int, visu: List[List[str]],
                 maze_hexa: List[List[str]], x: int, y: int,
                 scale: int, tile_size: int, target: Any,
                 red: Ghost | None) -> None:
        """
        To init attributs

        :attributs:
            - __name: str

            - score: int

            - x: float

            - y: float

            - state: str

            - afraid_timer: int

            - edible: bool

            - _sprite_size: tuple

            - _scaled: tuple

            - tile_size: int

            - tile_scale: int

            - _sheet: Surface

            - sprite: Surface

            - spawn: tuple

            - path: List[str]

            - previous: str

            - __visu: List[List[str]]

            - __maze_hexa: List[List[str]]

            - target: Any

            - speed: float

            - red: Ghost | None

            - anim_timer: float

            - anim_speed: float

            - sprite_increment: int

            - sprite_index: int

            - rand_target: tuple
        """
        self.__name = name
        self.score = score
        self.x: float = x
        self.y: float = y
        self.state = "chase"
        self.afraid_timer = 0.0
        self.edible = False
        self._sprite_size = (32, 32)
        self._scaled = self.get_scale(scale)
        self.tile_size = tile_size
        self.tile_scale = scale
        self._sheet = self.load_sprite_sheet()
        self.sprite = self.get_sprite((0, 0))
        self.spawn = ((x // 32 + 1), (y // 32 + 1))
        self.path: List[str] = []
        self.previous = ""
        self.__visu = visu
        self.__maze_hexa = maze_hexa
        self.target: Any = target
        self.speed = target.speed - 8
        if self.__name == "inky" and red:
            self.red = red
        self.anim_timer = 0.0
        self.anim_speed = 0.08
        self.sprite_increment = 1
        self.sprite_index = 0
        self.rand_target = self.get_rand_target(self.__maze_hexa, self.__visu)

    def get_scale(self, scale: int) -> Tuple[float, float]:
        """
        To calculate the sprite scale

        :params:
            - scale : the scaling required
        :returns:
            tuple : the scaling maze
        """
        wall_size_x = 32 * scale
        size = 31.25 * wall_size_x // 100 + 4
        return (size, size)

    def load_sprite_sheet(self) -> pg.Surface:
        """
        To calculate the sprite scale

        :returns:
            Surface : The loaded sprite sheet
        """
        if self.state == "afraid":
            return pg.image.load("./sprite/afraid.png").convert_alpha()
        elif self.state == "dead":
            return pg.image.load("./sprite/dead.png").convert_alpha()
        elif self.__name == "blinky":
            return pg.image.load("./sprite/blinky.png").convert_alpha()
        elif self.__name == "inky":
            return pg.image.load("./sprite/inky.png").convert_alpha()
        elif self.__name == "pinky":
            return pg.image.load("./sprite/pinky.png").convert_alpha()
        else:
            return pg.image.load("./sprite/clyde.png").convert_alpha()

    def get_sprite(self, loc: Tuple[int, int],
                   colorkey: (pg.Color |
                              Tuple[int, int, int] |
                              int) = (255, 255, 255)
                   ) -> pg.Surface:
        """
        To get the sprite

        :params:
            - loc : the coordinate of the sprite

            - colorkey : the color

        :returns:
            Surface : the sprite
        """
        x = loc[1] * self._sprite_size[0]
        y = loc[0] * self._sprite_size[1]
        if self.state == "afraid":
            y = 0

        rect = pg.Rect(x, y, *self._sprite_size)
        img = pg.Surface(self._sprite_size, pg.SRCALPHA).convert_alpha()
        img.blit(self._sheet, (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey, pg.RLEACCEL)
        return pg.transform.scale(img, self._scaled)

    def set_algo(self, target: Tuple[int, int]) -> None:
        """
        To calculate the sprite scale

        :params:
            - scale : the scaling required
        """
        if self.state == "chase":
            if self.__name == "blinky":
                self.path = self.algo_blinky(target)
                self.rand_target = self.get_rand_target(self.__maze_hexa,
                                                        self.__visu)
            elif self.__name == "pinky":
                self.path = self.algo_blinky(
                    self.get_pinky_target(target,
                                          (self.target.direction[0]
                                           if self.target.direction else ""),
                                          self.__visu))
                self.rand_target = self.get_rand_target(self.__maze_hexa,
                                                        self.__visu)
            elif self.__name == "inky":
                self.path = self.algo_blinky(
                    self.get_inky_target(
                        (int((self.red.x + self._scaled[0]/2) // 32),
                         int((self.red.y + self._scaled[1]/2) // 32)),
                        target,
                        (self.target.direction[0]
                         if self.target.direction else ""),
                        self.__visu))
                self.rand_target = self.get_rand_target(self.__maze_hexa,
                                                        self.__visu)
            else:
                if len(self.algo_blinky(target)) <= 8 or self.path:
                    self.path = self.algo_blinky(self.rand_target)
                else:
                    self.path = self.algo_blinky(target)
                    self.rand_target = self.get_rand_target(self.__maze_hexa,
                                                            self.__visu)
        elif self.state == "afraid":
            if self.afraid_timer and time.time() - self.afraid_timer >= 10:
                self.state = "chase"
                self.edible = False
                self._sheet = self.load_sprite_sheet()
            if len(self.path) == 0:
                self.rand_target = self.get_rand_target(self.__maze_hexa,
                                                        self.__visu)
            self.path = self.algo_blinky(self.rand_target)
        elif self.state == "dead":
            self.path = self.algo_blinky(self.spawn)
            if len(self.path) == 0:
                self.state = "chase"
                self.edible = False
                self._sheet = self.load_sprite_sheet()

    def algo_blinky(self, target: Tuple[int, int]) -> List[str]:
        """
        To calculate the shortest path for Blinky

        :params:
            - target : target position in the maze

        :returns:
            List : list of directions to reach the target
        """
        queue: Deque[Tuple[int, ...]] = deque()
        visited = set()
        parent = {}
        s_x = int((self.x + self._scaled[0]/2) // (self.tile_size/2))
        s_y = int((self.y + self._scaled[1]/2) // (self.tile_size/2))

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

    def move_ghost(self, dt: float) -> None:
        """
        To move the ghost depending on the user input

        :params:
            - dt : delta for the speed of the current game
        """
        ht = self.tile_size/2
        target = (
                    int((self.target.x + self._scaled[0] / 2) // ht),
                    int((self.target.y + self._scaled[1] / 2) // ht)
                )
        direction = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer -= self.anim_speed
            self.sprite_index += self.sprite_increment
            if self.sprite_index == 1 or self.sprite_index == 0:
                self.sprite_increment *= -1

        if (self.previous in direction and
            self.can_move(self.previous, dt, self.__visu) and not
            (self.path and
             self.can_move(self.path[0], dt, self.__visu))):
            if not set(self.path) == {self.previous}:
                self.set_algo(target)
            if self.previous == "UP":
                self.sprite = self.get_sprite((self.sprite_index, 2))
                self.y -= self.speed * dt
            elif self.previous == "DOWN":
                self.sprite = self.get_sprite((self.sprite_index, 1))
                self.y += self.speed * dt
            elif self.previous == "LEFT":
                self.sprite = self.get_sprite((self.sprite_index, 3))
                self.x -= self.speed * dt
            elif self.previous == "RIGHT":
                self.sprite = self.get_sprite((self.sprite_index, 0))
                self.x += self.speed * dt
        elif self.path and self.can_move(self.path[0], dt, self.__visu):
            if self.path[0] == "UP":
                self.sprite = self.get_sprite((self.sprite_index, 2))
                self.y -= self.speed * dt
            elif self.path[0] == "DOWN":
                self.sprite = self.get_sprite((self.sprite_index, 1))
                self.y += self.speed * dt
            elif self.path[0] == "LEFT":
                self.sprite = self.get_sprite((self.sprite_index, 3))
                self.x -= self.speed * dt
            elif self.path[0] == "RIGHT":
                self.sprite = self.get_sprite((self.sprite_index, 0))
                self.x += self.speed * dt

            if len(self.path) >= 2 and self.can_move(self.path[0], dt,
                                                     self.__visu):
                self.previous = self.path.pop(0)
            elif len(self.path) == 1:
                self.previous = self.path.pop(0)
        else:
            self.set_algo(target)

    def can_move(self, dir: str,
                 dt: float, visu: List[List[str]]) -> bool:
        """
        To check the next pixel move

        :params:
            - scale : the scaling required

        :returns:
            Bool : To know if we collide with a wall or not
        """
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

        center_x = int(check_x + self._scaled[0]//2)
        center_y = int(check_y + self._scaled[1]//2)
        tol = self.get_tolerance()
        grid_x1, grid_y1 = (int((center_x) / (self.tile_size/2)),
                            int((center_y) / (self.tile_size/2)))
        grid_x2, grid_y2 = (int((center_x + tol) / (self.tile_size/2)),
                            int((center_y) / (self.tile_size/2)))
        grid_x3, grid_y3 = (int((center_x) / (self.tile_size/2)),
                            int((center_y + tol) / (self.tile_size/2)))
        grid_x4, grid_y4 = (int((center_x + tol) / (self.tile_size/2)),
                            int((center_y + tol) / (self.tile_size/2)))
        return (visu[grid_y1][grid_x1] == " " and
                visu[grid_y2][grid_x2] == " " and
                visu[grid_y3][grid_x3] == " " and
                visu[grid_y4][grid_x4] == " ")

    def get_tolerance(self) -> float:
        """
        To get the tolerance

        :returns:
            float : the tolerance
        """
        tol = self.tile_size/2 - 2 * (self.tile_size/2)/32
        return tol

    def get_inky_target(self, red_pos: Tuple[int, int],
                        pac_pos: Tuple[int, int],
                        pac_dir: str,
                        visu: List[List[str]]) -> Tuple[int, int]:
        """
        To calculate the target for inky

        :params:
            - red_pos : The red ghost actual position

            - pac_pos : the actual pacman position

            - pac_dir : the actual direction of pacman

            - visu : the maze visu

        :returns:
            Tuple : The target for inky
        """
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

    def get_pinky_target(self, pac_pos: Tuple[int, int],
                         pac_dir: str,
                         visu: List[List[str]]) -> Tuple[int, int]:
        """
        To calculate the target for pinky

        :params:
            - pac_pos : the actual pacman position

            - pac_dir : the actual direction of pacman

            - visu : the maze visu

        :returns:
            Tuple : The target for pinky
        """
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

    def get_rand_target(self, maze_hexa: List[List[str]],
                        visu: List[List[str]]) -> Tuple[int, int]:
        """
        To calculate a random target

        :params:
            - maze_hexa : the maze in hexa

            - visu : the maze visu

        :returns:
            Tuple : A random target
        """
        while True:
            x = random.randint(0, len(visu[0]) - 1)
            y = random.randint(0, len(visu) - 1)
            if (visu[y][x] != " " or
               maze_hexa[int((y - 1) / 2)][int((x - 1) / 2)] == "F"):
                continue
            if visu[y][x] == " ":
                return (x, y)


def init_ghosts(conf: Dict[str, str | int],
                visu: List[List[str]],
                pacman: Any,
                maze_hexa: List[List[str]],
                scale: int) -> Dict[str, Ghost]:
    """
    To calculate a random target

    :params:
        - maze_hexa : the maze in hexa

        - visu : the maze visu

    :returns:
        Tuple : A random target
    """
    w = int(conf['width'])
    h = int(conf['height'])
    tile = 32 * scale
    x1, y1 = int(tile/2 - 12*(scale/2)), int(tile/2 - 12*(scale/2))
    pts = int(conf['points_per_ghost'])
    ghosts = {
        "blinky": Ghost("blinky", pts, visu, maze_hexa,
                        x1, y1, scale, tile, pacman, None),
        "clyde": Ghost("clyde", pts, visu, maze_hexa, x1,
                       (h - 1) * tile + y1, scale, tile, pacman, None),
        "pinky": Ghost("pinky", pts, visu, maze_hexa,
                       (w - 1) * tile + x1, (h - 1) * tile + y1, scale,
                       tile, pacman, None)
    }
    ghosts.update({"inky": Ghost("inky", pts, visu,
                                 maze_hexa, (w - 1) * tile + x1, y1, scale,
                                 tile, pacman, ghosts['blinky'])})
    return ghosts


def move_all_ghosts(ghosts: Dict[str, Ghost], dt: float) -> None:
    """
    To calculate the target for pinky

    :params:
        - ghosts : dict that contains all ghosts

        - dt : speed of the current game
    """
    for _, value in ghosts.items():
        value.move_ghost(dt)


def scared_ghost(ghosts: Dict[str, Ghost]) -> bool:
    """
    To know if one of the ghost is afraid

    :params:
        - pac_pos : the actual pacman position

        - pac_dir : the actual direction of pacman

        - visu : the maze visu

    :returns:
        Tuple : The target for pinky
    """
    for _, gh in ghosts.items():
        if gh.state == "afraid":
            return True
    return False
