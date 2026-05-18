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
