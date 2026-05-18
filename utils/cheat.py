import pygame as pg
from typing import Dict


def enter_input(inputs, running) -> bool:
    for event in pg.event.get():
        if event.type == pg.QUIT and running:
            running = False
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if event.unicode.isalnum() or event.unicode.isspace():
                inputs.append(event.unicode.upper())
            if keys[pg.K_UP]:
                inputs.append("UP")
            elif keys[pg.K_DOWN]:
                inputs.append("DOWN")
            elif keys[pg.K_LEFT]:
                inputs.append("LEFT")
            elif keys[pg.K_RIGHT]:
                inputs.append("RIGHT")
    return running


def enable_cheats(cheat_code) -> bool:
    correct_cheat = [
        "UP", "UP", "DOWN", "DOWN",
        "LEFT", "RIGHT", "LEFT", "RIGHT",
        "B", "A"
    ]
    for i in range(len(cheat_code) - len(correct_cheat) + 1):
        if cheat_code[i:i+len(correct_cheat)] == correct_cheat:
            return True
    return False


def init_cheats() -> Dict[str, bool]:
    cheats = {
        "Invincibility": False,
        "Ghost Freeze": False,
        "Skip level (press S)": False
    }
    return cheats


def activate_cheats(cheats):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_1]:
                cheats['Invincibility'] = not cheats['Invincibility']
            elif keys[pg.K_2]:
                cheats['Ghost Freeze'] = not cheats['Ghost Freeze']
            elif keys[pg.K_3]:
                cheats['Skip level (press S)'] = (
                    not cheats['Skip level (press S)'])
