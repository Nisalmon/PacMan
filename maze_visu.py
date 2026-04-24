import pygame as pg

TILE_SIZE = 32


def build_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            visu[j * 2 + 1][i * 2 + 1] = " "
    return break_walls(visu, maze)


def generate_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]

    for i in range(len(maze[0])):
        for j in range(len(maze)):
            visu[j * 2 + 1][i * 2 + 1] = " "

    for elem in maze:
        for ch in elem:
            print(ch, end="")
        print()
    print()
    visu = break_walls(visu, maze)
    for elem in visu:
        for ch in elem:
            print(ch, end="")
        print()


def break_walls(visu, maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
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
    for r_id, row in enumerate(visu):
        for c_id, col in enumerate(row):
            print(r_id)
            x = c_id * TILE_SIZE * 2
            y = r_id * TILE_SIZE * 2
            if col == 1:
                screen.blit(walls['wall'], (x, y))
            if col == 2:
                screen.blit(rotated_wall_270, (x, y))
            if col == 3:
                screen.blit(walls['wall'], (x, y))
                screen.blit(rotated_wall_270, (x, y))
            if col == 4:
                screen.blit(rotated_wall_180, (x, y))
            if col == 5:
                screen.blit(walls['wall'], (x, y))
                screen.blit(rotated_wall_180, (x, y))
            if col == 6:
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_270, (x, y))
            if col == 7:
                screen.blit(walls['wall'], (x, y))
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_270, (x, y))
            if col == 8:
                screen.blit(rotated_wall_90, (x, y))
            if col == 9:
                screen.blit(rotated_wall_90, (x, y))
                screen.blit(walls['wall'], (x, y))
            if col == 10:
                screen.blit(rotated_wall_270, (x, y))
                screen.blit(rotated_wall_90, (x, y))
            if col == 11:
                screen.blit(rotated_wall_270, (x, y))
                screen.blit(rotated_wall_90, (x, y))
                screen.blit(walls['wall'], (x, y))
            if col == 12:
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_90, (x, y))
            if col == 13:
                screen.blit(walls['wall'], (x, y))
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_90, (x, y))
            if col == 14:
                screen.blit(rotated_wall_90, (x, y))
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_270, (x, y))
            if col == 15:
                screen.blit(walls['wall'], (x, y))
                screen.blit(rotated_wall_90, (x, y))
                screen.blit(rotated_wall_180, (x, y))
                screen.blit(rotated_wall_270, (x, y))
