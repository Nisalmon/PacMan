import pygame as pg

TILE_SIZE = 32


def build_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            visu[j * 2 + 1][i * 2 + 1] = " "
    return break_walls(visu, maze)


def break_walls(visu, maze):
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            if maze[j][i] == '1':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "

            if maze[j][i] == '2':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == '3':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == '4':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == '5':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "

            if maze[j][i] == '6':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == '7':
                visu[j * 2 + 1][i * 2] = " "

            if maze[j][i] == '8':
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2][i * 2 + 1] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == '9':
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == 'A':
                visu[j * 2][i * 2 + 1] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == 'B':
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == 'C':
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == 'D':
                visu[j * 2 + 1][i * 2 + 2] = " "

            if maze[j][i] == 'E':
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == '0':
                visu[j * 2][i * 2 + 1] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2][i * 2 + 1] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

    return visu


def draw_maze(screen, visu, walls):
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
        for c_id, col in enumerate(row):
            x = c_id * TILE_SIZE * 2
            y = r_id * TILE_SIZE * 2
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
