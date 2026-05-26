import pygame as pg
from typing import Dict, List, Tuple, Any
from utils.pacgums import Pacgums
from utils.player import Player
from utils.ghost import Ghost


TILE_SIZE = 32


def draw_maze(screen: pg.Surface, visu: List[List[int]],
              walls: Dict[str, Any], scale: Tuple[int, int]) -> None:
    """
    To print the maze in the screen

    :params:
        - screen : the pygame screen

        - visu : the maze visu

        - walls : Dict that contains sprites for the walls

        - scale : The scaling
    """
    rotated_wall_90 = pg.transform.rotate(walls['wall'], 90)
    rotated_wall_180 = pg.transform.rotate(walls['wall'], 180)
    rotated_wall_270 = pg.transform.rotate(walls['wall'], 270)
    rotated_corner_wall_90 = pg.transform.rotate(walls['corner_wall'], 90)
    rotated_corner_wall_180 = pg.transform.rotate(walls['corner_wall'], 180)
    rotated_corner_wall_270 = pg.transform.rotate(walls['corner_wall'], 270)
    rotated_incline_wall_90 = pg.transform.rotate(walls['incline_wall'], 90)
    rotated_incline_wall_180 = pg.transform.rotate(walls['incline_wall'], 180)
    rotated_incline_wall_270 = pg.transform.rotate(walls['incline_wall'], 270)
    rotated_triple_wall_90 = pg.transform.rotate(walls['triple_wall'], 90)
    rotated_triple_wall_180 = pg.transform.rotate(walls['triple_wall'], 180)
    rotated_triple_wall_270 = pg.transform.rotate(walls['triple_wall'], 270)
    for r_id, row in enumerate(visu):
        for c_id, _ in enumerate(row):
            x = c_id * TILE_SIZE * scale[0]
            y = r_id * TILE_SIZE * scale[1]
            cell = visu[r_id][c_id]
            has_N = bool(cell & 1)
            has_E = bool(cell & 2)
            has_S = bool(cell & 4)
            has_W = bool(cell & 8)

            if has_N and not has_E and not has_W:
                screen.blit(walls['wall'], (x, y))
            if has_N and has_E:
                screen.blit(walls['incline_wall'], (x, y))
            if has_N and has_W:
                screen.blit(rotated_incline_wall_90, (x, y))
            if has_S and not has_E and not has_W:
                screen.blit(rotated_wall_180, (x, y))
            if has_S and has_E:
                screen.blit(rotated_incline_wall_270, (x, y))
            if has_S and has_W:
                screen.blit(rotated_incline_wall_180, (x, y))
            if has_E and not has_N and not has_S:
                screen.blit(rotated_wall_270, (x, y))
            if has_W and not has_N and not has_S:
                screen.blit(rotated_wall_90, (x, y))
            if not has_N and not has_E:
                screen.blit(rotated_corner_wall_180, (x, y))
            if not has_E and not has_S:
                screen.blit(rotated_corner_wall_90, (x, y))
            if not has_S and not has_W:
                screen.blit(walls["corner_wall"], (x, y))
            if not has_W and not has_N:
                screen.blit(rotated_corner_wall_270, (x, y))
            if has_N and has_E and has_W:
                screen.blit(walls["triple_wall"], (x, y))
            if has_E and has_N and has_S:
                screen.blit(rotated_triple_wall_270, (x, y))
            if has_S and has_E and has_W:
                screen.blit(rotated_triple_wall_180, (x, y))
            if has_W and has_N and has_S:
                screen.blit(rotated_triple_wall_90, (x, y))
            if has_E and has_N and has_S and has_W:
                screen.blit(walls["four_wall"], (x, y))


def draw_pacgums(pacgums: List[Pacgums], screen: pg.Surface) -> None:
    """
    To draw in the screen the pacgums

    :params:
        - pacgums : the list of all pacgums

        - screen : pygame screen
    """
    for elem in pacgums:
        screen.blit(elem.sprite, (elem.x, elem.y))


def draw_ghosts(screen: pg.Surface, ghosts: Dict[str, Ghost]) -> None:
    """
    To draw the ghost in the pygame screen

    :params:
        - screen : pygame screen

        - ghosts : the list of all the ghost
    """
    for _, value in ghosts.items():
        screen.blit(value.sprite, (value.x, value.y))


def draw_env(screen: pg.Surface, visu: List[List[int]], walls: Dict[str, Any],
             pacgums: List[Pacgums], ghosts: Dict[str, Ghost],
             player: Player, scale: Tuple[int, int]) -> None:
    """
    To print all the sprite in the game

    :params:
        - screen : pygame screen

        - visu : the maze visu

        - walls : list that contains all the sprites for the wall

        - pacgums : the list of all the pacgums

        - ghosts : Dict that contains all the ghosts

        - player : The player class

        - scale : the scaling of the maze
    """
    draw_maze(screen, visu, walls, scale)
    draw_pacgums(pacgums, screen)
    draw_ghosts(screen, ghosts)
    screen.blit(player.sprite, (player.x, player.y))
