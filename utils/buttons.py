import pygame as pg
from typing import Tuple, Dict, Any


class Button:
    def __init__(self, x: int, y: int, name: str) -> None:
        self.name = name
        self.width = 160
        self.height = 100
        self.x = x - self.width // 2
        self.y = y
        self.rect = pg.rect.Rect(self.x - self.width/4, self.y - self.height/4,
                                 self.width, self.height)
        self.color = (127, 127, 127)

    def mouse_in_rect(self) -> bool:
        mos_x, mos_y = pg.mouse.get_pos()
        return (
            self.x - self.width/4 <= mos_x and
            self.x + 3*self.width/4 >= mos_x and
            self.y - self.height/4 <= mos_y and
            self.y + 3*self.height/4 >= mos_y
        )

    def clicked(self) -> bool:
        is_clicked = pg.mouse.get_pressed()
        return is_clicked[0] is True and self.mouse_in_rect()


def init_buttons(size: Tuple[int, int]) -> Dict[str, Button]:
    buttons = {
        "main": Button(((size[0] - 48) // 2), ((size[1] - 24) // 2), "Play"),
        "score": Button(((size[0] - 48) // 2),
                        ((size[1] + 200) // 2), "Score"),
        "guide": Button(((size[0] + 296) // 2),
                        ((size[1] - 24) // 2), "Guide"),
        "exit": Button(((size[0] + 296) // 2),
                       ((size[1] + 200) // 2), "Exit")
    }
    return buttons


def draw_button(buttons: Dict[str, Button],
                screen_conf: Dict[str, Any]) -> None:
    for _, button in buttons.items():
        button.color = (127, 127, 127) if not button.mouse_in_rect() else (90,
                                                                           90,
                                                                           90)
        pg.draw.rect(screen_conf['screen'], button.color, button.rect)
        screen_conf['font'].render_to(screen_conf['screen'],
                                      (button.x - button.height/16,
                                      button.y + button.height/8),
                                      button.name, (255, 255, 255))


def cheat_button(buttons: Dict[str, Button], size: Tuple[int, int]) -> None:
    buttons.update(
        {
            "cheat": Button(((size[0] + 124) // 2),
                            ((size[1] + 424) // 2),
                            "Cheat")
        }
    )
