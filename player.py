import pygame as pg
# from typing import Union, Tuple


TILE_SIZE = 32

class Player:
    def __init__(self, x, y, sprite_loc):
        self.x = x
        self.y = y
        self._sheet = pg.image.load(sprite_loc).convert_alpha()
        self._sprite_size = (32, 32)
        self.sprite = self.get_sprite((0, 0))
        self.sprite_index = 0
        self.sprite_increment = 1
        self.speed = 32
        self.anim_timer = 0
        self.__anim_speed = 0.08
        self.score = 0

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
        return pg.transform.scale(img, (24, 24))

    def move_player(self, dt, cells, visu):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN]:
            self.x = round(self.x / 4) * 4

        elif keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
            self.y = round(self.y / 4) * 4
        moving = False
        if self.can_move(cells, keys, dt, visu):
            if keys[pg.K_LEFT]:
                self.x -= self.speed * dt
                moving = True

            elif keys[pg.K_RIGHT]:
                self.x += self.speed * dt
                moving = True

            elif keys[pg.K_UP]:
                self.y -= self.speed * dt
                moving = True

            elif keys[pg.K_DOWN]:
                self.y += self.speed * dt
                moving = True

        if moving:
            self.anim_timer += dt

            if self.anim_timer >= self.__anim_speed:
                self.anim_timer -= self.__anim_speed
                self.sprite_index += self.sprite_increment

                if self.sprite_index == 3 or self.sprite_index == 0:
                    self.sprite_increment *= -1

            base_sprite = self.get_sprite((0, self.sprite_index))

            if keys[pg.K_LEFT]:
                self.sprite = pg.transform.rotate(base_sprite, 180)

            elif keys[pg.K_RIGHT]:
                self.sprite = pg.transform.rotate(base_sprite, 0)

            elif keys[pg.K_UP]:
                self.sprite = pg.transform.rotate(base_sprite, 90)

            elif keys[pg.K_DOWN]:
                self.sprite = pg.transform.rotate(base_sprite, 270)
            
            

    def eat_pacgums(self, pacgums):
        for gum in pacgums:
            if (abs(self.x - gum.x) < 10 and
                abs(self.y - gum.y) < 10):
                self.score += 10
                pacgums.pop(pacgums.index(gum))

    def can_move(self, cells, dir, dt, visu) -> bool:
        check_x = self.x
        check_y = self.y

        if dir[pg.K_LEFT]:
            check_x -= self.speed * dt
        elif dir[pg.K_RIGHT]:
            check_x += self.speed * dt
        elif dir[pg.K_UP]:
            check_y -= self.speed * dt
        elif dir[pg.K_DOWN]:
            check_y += self.speed * dt

        center_x, center_y = check_x + 12, check_y + 12
        grid_x, grid_y = int(center_x/32), int(center_y/32)
        grid_x2, grid_y2 = int((center_x + 12)/32), int((center_y + 12)/32)

        return visu[grid_y][grid_x] == " "