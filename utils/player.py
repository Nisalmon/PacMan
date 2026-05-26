import pygame as pg
import time
from utils.pacgums import Pacgums
from utils.ghost import Ghost
from typing import Tuple, Dict, List


TILE_SIZE = 32
PLAYER_SIZE = 24
HALF_TILE = TILE_SIZE // 2
HALF_PLAYER = 24 // 2


class Player:
    """
    Class for the player

    :methods:
        - get_scale : to get the scale

        - get_sprite : to get the sprite

        - move_player : To move the player in the maze

        - can_move : check if the player can move to the next direction

        - eat_pacgums : To simulate the eat of the pacgum

        - get_tolerance : To get the tolerance

        - touch_ghost : Check if the player collide a ghost
    """
    def __init__(self, x: int, y: int,
                 sprite_loc: str, lives: int,
                 scale: int) -> None:
        """
        To initialize the player

        :params:
            - x : x position of the player

            - y : y position of the player

            - sprite_loc : location of the sprite sheet

            - lives : number of lives

            - scale : scaling size of the player
        """
        self.x: float = x
        self.y: float = y
        self._sheet = pg.image.load(sprite_loc).convert_alpha()
        self._sprite_size = (32, 32)
        self._scaled = self.get_scale(scale)
        self.scale = scale
        self.tile_size = 32 * scale
        self.sprite = self.get_sprite((0, 0))
        self.sprite_index = 0
        self.sprite_increment = 1
        self.speed = self.tile_size
        self.anim_timer = 0.0
        self.__anim_speed = 0.08
        self.score = 0
        self.direction: List[str] = []
        self.lives = lives
        self.alive: bool | None = True
        self.just_respawned = False

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

    def get_sprite(self, loc: Tuple[int, int],
                   colorkey: pg.Color | int | Tuple[int, int, int] = (255,
                                                                      255,
                                                                      255)
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

        rect = pg.Rect(x, y, *self._sprite_size)
        img = pg.Surface(self._sprite_size, pg.SRCALPHA).convert_alpha()
        img.blit(self._sheet, (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey, pg.RLEACCEL)
        return pg.transform.scale(img, self._scaled)

    def move_player(self, dt: float, visu: List[List[str]]) -> None:
        """
        To move the ghost depending on the user input

        :params:
            - dt : delta for the speed of the current game

            - visu : the maze visu
        """
        keys = pg.key.get_pressed()
        dir = self.direction[0] if self.direction else ""
        dir2 = (self.can_move(self.direction[1], dt, visu)
                if len(self.direction) == 2 else False)
        if keys[pg.K_LEFT]:
            if len(self.direction) < 2 and "LEFT" not in self.direction:
                self.direction.append("LEFT")
            elif len(self.direction) == 2 and "LEFT" not in self.direction:
                self.direction[1] = "LEFT"

        elif keys[pg.K_RIGHT]:
            if len(self.direction) < 2 and "RIGHT" not in self.direction:
                self.direction.append("RIGHT")
            elif len(self.direction) == 2 and "RIGHT" not in self.direction:
                self.direction[1] = "RIGHT"

        elif keys[pg.K_UP]:
            if len(self.direction) < 2 and "UP" not in self.direction:
                self.direction.append("UP")
            elif len(self.direction) == 2 and "UP" not in self.direction:
                self.direction[1] = "UP"

        elif keys[pg.K_DOWN]:
            if len(self.direction) < 2 and "DOWN" not in self.direction:
                self.direction.append("DOWN")
            elif len(self.direction) == 2 and "DOWN" not in self.direction:
                self.direction[1] = "DOWN"

        self.anim_timer += dt

        if self.anim_timer >= self.__anim_speed:
            self.anim_timer -= self.__anim_speed
            self.sprite_index += self.sprite_increment

            if self.sprite_index == 3 or self.sprite_index == 0:
                self.sprite_increment *= -1

        base_sprite = self.get_sprite((0, self.sprite_index))
        if self.can_move(dir, dt, visu) and dir2 is False:
            if len(self.direction) > 0:
                if self.can_move(self.direction[0], dt, visu):
                    if self.direction[0] == "LEFT":
                        self.sprite = pg.transform.rotate(base_sprite, 180)
                        self.x -= self.speed * dt

                    elif self.direction[0] == "RIGHT":
                        self.sprite = pg.transform.rotate(base_sprite, 0)
                        self.x += self.speed * dt

                    elif self.direction[0] == "UP":
                        self.sprite = pg.transform.rotate(base_sprite, 90)
                        self.y -= self.speed * dt

                    elif self.direction[0] == "DOWN":
                        self.sprite = pg.transform.rotate(base_sprite, 270)
                        self.y += self.speed * dt
        else:
            if len(self.direction) == 2:
                self.direction.pop(0)

    def eat_pacgums(self,
                    pacgums: List[Pacgums],
                    ghosts: Dict[str, Ghost],
                    eat: pg.mixer.Sound) -> None:
        """
        To get the state of the pacgums eated

        :params:
            - pacgums : list of all the pacgums

            - ghosts : the list of all the ghosts

            - eat : sound for the eated gum
        """
        for gum in pacgums:
            if (abs(self.x - gum.x) < 7 and
               abs(self.y - gum.y) < 7):
                self.score += gum.score
                eat.play(0)
                pacgums.pop(pacgums.index(gum))
                if gum._type == "super":
                    for _, gh in ghosts.items():
                        gh.state = "afraid"
                        gh.afraid_timer = time.time()
                        gh.edible = True
                        gh._sheet = gh.load_sprite_sheet()

    def can_move(self, dir: str, dt: float,
                 visu: List[List[str]]) -> bool:
        """
        To check the next pixel move

        :params:
            - scale : the scaling required

        :returns:
            Bool : To know if we collide with a wall or not
        """
        check_x: float = round(self.x)
        check_y: float = round(self.y)

        if dir == "":
            return False
        if dir == "LEFT":
            check_x -= self.speed * dt + 1
        elif dir == "RIGHT":
            check_x += self.speed * dt + 1
        elif dir == "UP":
            check_y -= self.speed * dt + 1
        elif dir == "DOWN":
            check_y += self.speed * dt + 1

        center_x = round(check_x + self._scaled[0]//2)
        center_y = round(check_y + self._scaled[1]//2)
        tol = self.get_tolerance()
        grid_x1, grid_y1 = (int((center_x)/(self.tile_size/2)),
                            int((center_y)/(self.tile_size/2)))
        grid_x2, grid_y2 = (int((center_x + tol)/(self.tile_size/2)),
                            int((center_y)/(self.tile_size/2)))
        grid_x3, grid_y3 = (int((center_x)/(self.tile_size/2)),
                            int((center_y + tol)/(self.tile_size/2)))
        grid_x4, grid_y4 = (int((center_x + tol)/(self.tile_size/2)),
                            int((center_y + tol)/(self.tile_size/2)))
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
        tol = self.tile_size/2 - 3 * (self.tile_size/2)/32
        return tol

    def touch_ghost(self, ghosts: Dict[str, Ghost]) -> None:
        """
        To check the if the player collide a ghost

        :params:
            - ghosts : Dict of all the ghosts
        """
        for _, value in ghosts.items():
            if (abs(self.x - value.x) < 15 and
               abs(self.y - value.y) < 15 and
               value.edible is False):
                self.lives -= 1
                self.alive = False
                if self.lives <= 0:
                    self.lives = 0
            elif (abs(self.x - value.x) < 15 and
                  abs(self.y - value.y) < 15 and
                  value.edible is True and
                  value.state == "afraid"):
                self.score += value.score
                value.state = "dead"
                value._sheet = value.load_sprite_sheet()


def init_player(x: int,
                y: int,
                sprite: str,
                lives: int,
                scale: int) -> Player:
    """
        To init player

        :params:
            - x: int

            - y: int

            - sprite: str

            - lives: int

            - scale: iny


        :returns:
            Player : create player
        """
    return Player(x, y, sprite, lives, scale)
