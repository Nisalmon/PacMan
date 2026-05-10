import pygame as pg


class Button:
    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.width = 160
        self.height = 100
        self.rect = pg.rect.Rect(x- self.width/4, y - self.height/4, self.width, self.height)

    def mouse_in_rect(self):
        mos_x, mos_y = pg.mouse.get_pos()
        return (
            self.x - self.width/4 <= mos_x and
            self.x + 3*self.width/4 >= mos_x and
            self.y - self.height/4 <= mos_y and
            self.y + 3*self.height/4 >= mos_y
        )

    def clicked(self):
        is_clicked = pg.mouse.get_just_pressed()
        return is_clicked[0] is True and self.mouse_in_rect()


def init_buttons(size):
    buttons = {
        "main": Button(((size[0] - 48) // 2), ((size[1] - 24) // 2), "Play"),
    }
    return buttons


def draw_button(buttons, screen_conf, size):
    color = (127, 127, 127) if not buttons.mouse_in_rect() else (97, 97, 97)
    pg.draw.rect(screen_conf['screen'], color, buttons.rect)
    screen_conf['font'].render_to(screen_conf['screen'], (buttons.x - buttons.height/16, buttons.y + buttons.height/8), buttons.name, (255, 255, 255))
