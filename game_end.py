def time_out(timer):
    return timer <= 0


def game_over(screen, size):
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 108, size[1] // 2),
                             "GAME OVER", (255, 255, 255))
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 132, size[1] // 2 + 48),
                             "PRESS SPACE", (255, 255, 255))


def win_screen(screen, size):
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 156, size[1] // 2),
                             "LEVEL COMPLETED", (255, 255, 255))
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 132, size[1] // 2 + 48),
                             "PRESS SPACE", (255, 255, 255))
