import pygame as pg
from typing import Tuple, Dict, Any


def get_leaderboard(screen: Dict[str, Any],
                    scorers: Dict[str, int],
                    size: Tuple[int, int]) -> None:
    '''
    To print the leaderboard in score section.

    :params:
        - screen: Dict: The screen configuration dict.

        - scorers: Dict: The dict containing the highest scorers.

        - size: Tuple: The size of the screen.
    '''
    loc = (size[0] // 2, size[1] - 3*size[1]//4)
    txt = "Highscores:"
    screen['font'].render_to(screen['screen'],
                             (loc[0] - len(txt)*10, loc[1] + 72),
                             f"{txt}", (255, 255, 255))
    cnt = 1
    for name, value in scorers.items():
        screen['font'].render_to(screen['screen'],
                                 (loc[0] - len(txt) * 15,
                                  loc[1] + 72 + 30*cnt),
                                 f"{cnt}. {name}: {value}",
                                 (255, 255, 255))
        cnt += 1


def print_score(score: int,
                screen: Dict[str, Any],
                size: Tuple[int, int]) -> None:
    '''
    To print the current score during game.

    :params:
        - score: int: Current score of player

        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.
    '''
    loc1 = (size[0] + 20, 12)
    loc2 = (size[0] + 20, 36)
    screen['font'].render_to(screen['screen'], loc1,
                             "SCORE:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{score}", (255, 255, 255))


def print_life(sprite: pg.Surface,
               lives: int,
               screen: Dict[str, Any],
               size: Tuple[int, int]) -> None:
    '''
    To print the amount of lives the player have.

    :params:
        - sprite: Surface: The sprite of lives

        - lives: int: The amount of lives of the player

        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.
    '''
    loc1 = (size[0] + 20, 96)
    loc2 = (size[0] + 20, 120)
    screen['font'].render_to(screen['screen'], loc1,
                             "Lives:", (255, 255, 255))
    for i in range(0, lives):
        if i >= 3:
            break
        screen['screen'].blit(sprite, (loc2[0] + i * 24, loc2[1]))


def print_timer(time: int,
                screen: Dict[str, Any],
                size: Tuple[int, int]) -> None:
    '''
    To print the remaining time on screen.

    :params:
        - screen: Dict: The screen configuration dict.

        - time: int: time left to finish the level.

        - size: Tuple: The size of the screen
    '''
    loc1 = (size[0] + 20, 180)
    loc2 = (size[0] + 20, 204)
    screen['font'].render_to(screen['screen'], loc1,
                             "Time:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{time}", (255, 255, 255))


def print_level(current: int,
                max_lvl: int,
                screen: Dict[str, Any],
                size: Tuple[int, int]) -> None:
    '''
    To print current level the player is on out of max_lvl

    :params:
        - current: int: The level the player is on

        - max_lvl: int: The number of levels in game

        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.
    '''
    loc1 = (size[0] + 20, 260)
    screen['font'].render_to(screen['screen'], loc1,
                             f"Level {current}/{max_lvl}",
                             (255, 255, 255))


def print_all(screen: Dict[str, Any],
              size: Tuple[int, int],
              score: int,
              sprite: pg.Surface,
              lives: int,
              time: int,
              level: int,
              nb_level: int) -> None:
    '''
    To print score, life, timer and level.

    :params:
        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.

        - score: int: Current score of player

        - sprite: Surface: The sprite of lives

        - lives: int: The amount of lives of the player

        - time: int: time left to finish the level.

        - level: int: The level the player is on

        - nb_level: int: The number of levels in game
    '''
    print_score(score, screen, size)
    print_life(sprite, lives, screen, size)
    print_timer(time, screen, size)
    print_level(level, nb_level, screen, size)


def print_countdown(screen: Dict[str, Any],
                    value: int,
                    size: Tuple[int, int]) -> None:
    '''
    To print countdown upon respawning.

    :params:
        - screen: Dict: The screen configuration dict.

        - value: int: The time left before being able to play

        - size: Tuple: The size of the screen
    '''
    loc = ((size[0] - 300) // 2 - 10, size[1] // 2 - 72)
    screen['font'].render_to(screen['screen'], loc,
                             f"{value}", (255, 255, 255))


def print_paused(screen: Dict[str, Any],
                 size: Tuple[int, int]) -> None:
    '''
    To print paused on screen

    :params:
        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen
    '''
    loc = (size[0]//2, size[1]//2)
    txt = [
        "Paused",
        "Press TAB to return to menu",
        "or SPACE to continue."
    ]
    for i in range(len(txt)):
        screen['font'].render_to(screen['screen'],
                                 (loc[0] - (len(txt[i])//2)*24,
                                  loc[1] + 36 * i),
                                 f"{txt[i]}", (255, 255, 255))


def print_guide(screen: Dict[str, Any]) -> None:
    '''
    To print instructions of how to play on screen

    :params:
        - screen: Dict: The screen configuration dict.
    '''
    instr = [
        "Move using arrow keys.",
        "In game, press ESC to pause the game.",
        "To go back to previous menus, press BACKSPACE."
    ]
    screen['font'].render_to(screen['screen'],
                             (0, 0),
                             "Instructions:",
                             (255, 255, 255))
    for i in range(len(instr)):
        screen['font'].render_to(screen['screen'],
                                 (0, 36*(i + 1)),
                                 instr[i],
                                 (255, 255, 255))


def end_game_print(screen: Dict[str, Any],
                   score: int,
                   size: Tuple[int, int]) -> None:
    '''
    To print the final score on screen

    :params:
        - screen: Dict: The screen configuration dict.

        - score: int: Final score of the game.

        - size: Tuple: The size of the screen.
    '''
    loc1 = (size[0] // 2 - 116, size[1] // 2 - 48)
    loc2 = (size[0] // 2, size[1] // 2)
    screen['font'].render_to(screen['screen'], loc1,
                             "Final Score:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{score}", (255, 255, 255))


def congrats_print(screen: Dict[str, Any],
                   size: Tuple[int, int]) -> None:
    '''
    To print Congratulation on screen

    :params:
        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.
    '''
    loc = (size[0] // 2, size[1] // 2 - 148)
    txt = "Congratulation"
    screen['font'].render_to(screen['screen'], (loc[0] - (len(txt) // 2) * 24,
                                                loc[1]),
                             f"{txt}", (255, 255, 255))


def game_over_print(screen: Dict[str, Any],
                    size: Tuple[int, int]) -> None:
    '''
    To print GameOver on screen

    :params:
        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.
    '''
    loc = (size[0] // 2, size[1] // 2 - 148)
    txt = "Game Over..."
    screen['font'].render_to(screen['screen'], (loc[0] - (len(txt) // 2) * 24,
                                                loc[1]),
                             f"{txt}", (255, 255, 255))


def get_username(screen: Dict[str, Any],
                 username: str,
                 size: Tuple[int, int]) -> None:
    '''
    To print the input of the player for username

    :params:
        - screen: Dict: The screen configuration dict.

        - size: Tuple: The size of the screen.

        - username: str: The username that will be stored in scorers.
    '''
    loc1 = (size[0] // 2 - 116, size[1] // 2 + 48)
    loc2 = (size[0] // 2, size[1] // 2 + 80)
    screen['font'].render_to(screen['screen'], loc1,
                             "Enter Name:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{username}", (255, 255, 255))


def get_cheats(screen: Dict[str, Any],
               cheats: Dict[str, bool]) -> None:
    '''
    To print all available cheats in cheat menu

    :params:
        - screen: Dict: The screen configuration dict.

        - cheats: Dict: All available cheats
    '''
    cnt = 0
    for name, value in cheats.items():
        color = (255, 0, 0) if not value else (0, 255, 0)
        screen['font'].render_to(screen['screen'], (0, 36 * cnt),
                                 f"{cnt + 1}: {name}", color)
        cnt += 1
