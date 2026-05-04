import pygame as pg


TILE_SIZE = 32
HALF_TILE = TILE_SIZE // 2
HALF_PLAYER = 24 // 2


class Player:
    def __init__(self, x, y, sprite_loc):
        self.x = x
        self.y = y
        self._sheet = pg.image.load(sprite_loc).convert_alpha()
        self._sprite_size = (32, 32)
        self._scaled = (24, 24)
        self.sprite = self.get_sprite((0, 0))
        self.sprite_index = 0
        self.sprite_increment = 1
        self.speed = 64
        self.anim_timer = 0
        self.__anim_speed = 0.08
        self.score = 0
        self.direction = []

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

    def move_player(self, dt, visu):
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

    def eat_pacgums(self, pacgums):
        for gum in pacgums:
            if (abs(self.x - gum.x) < 10 and
               abs(self.y - gum.y) < 10):
                self.score += 10
                pacgums.pop(pacgums.index(gum))

    def can_move(self, dir, dt, visu) -> bool:
        check_x = round(self.x)
        check_y = round(self.y)

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
        grid_x1, grid_y1 = int((center_x)/32), int((center_y)/32)
        grid_x2, grid_y2 = int((center_x + 29)/32), int((center_y)/32)
        grid_x3, grid_y3 = int((center_x)/32), int((center_y + 29)/32)
        grid_x4, grid_y4 = int((center_x + 29)/32), int((center_y + 29)/32)
        return (visu[grid_y1][grid_x1] == " " and
                visu[grid_y2][grid_x2] == " " and
                visu[grid_y3][grid_x3] == " " and
                visu[grid_y4][grid_x4] == " ")

    def valid_move(self, dir, visu):
        points = [
            (self.x - 18) / 32 + 1,
            (self.y - 18) / 32 + 1,
            (self.x + 43) / 32,
            (self.y + 43) / 32,
        ]
        check_x = int(points[0])
        check_y = int(points[1])
        check_x2 = int(points[2])
        check_y2 = int(points[3])

        if dir == "LEFT":
            check_x -= 1
            return (visu[check_y][check_x] == " " and
                    visu[check_y2][check_x] == " ")
        elif dir == "RIGHT":
            check_x += 1
            return (visu[check_y][check_x2] == " " and
                    visu[check_y2][check_x2] == " ")
        elif dir == "UP":
            check_y -= 1
            return (visu[check_y][check_x] == " " and
                    visu[check_y][check_x2] == " ")
        elif dir == "DOWN":
            check_y += 1
            return (visu[check_y2][check_x] == " " and
                    visu[check_y2][check_x2] == " ")
        else:
            return False
