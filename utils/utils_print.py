def get_leaderboard(screen, scorers, size):
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


def print_score(score, screen, size):
    loc1 = (size[0] + 20, 12)
    loc2 = (size[0] + 20, 36)
    screen['font'].render_to(screen['screen'], loc1,
                             "SCORE:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{score}", (255, 255, 255))


def print_life(sprite, lives, screen, size):
    loc1 = (size[0] + 20, 96)
    loc2 = (size[0] + 20, 120)
    screen['font'].render_to(screen['screen'], loc1,
                             "Lives:", (255, 255, 255))
    for i in range(0, lives):
        screen['screen'].blit(sprite, (loc2[0] + i * 24, loc2[1]))


def print_timer(time, screen, size):
    loc1 = (size[0] + 20, 180)
    loc2 = (size[0] + 20, 204)
    screen['font'].render_to(screen['screen'], loc1,
                             "Time:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{time}", (255, 255, 255))


def print_all(screen, size, score, sprite, lives, time):
    print_score(score, screen, size)
    print_life(sprite, lives, screen, size)
    print_timer(time, screen, size)


def print_countdown(screen, value, size) -> None:
    loc = ((size[0] - 300) // 2 - 10, size[1] // 2 - 72)
    screen['font'].render_to(screen['screen'], loc,
                             f"{value}", (255, 255, 255))


def print_paused(screen, size) -> None:
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


def end_game_print(screen, score, size):
    loc1 = (size[0] // 2 - 116, size[1] // 2 - 48)
    loc2 = (size[0] // 2, size[1] // 2)
    screen['font'].render_to(screen['screen'], loc1,
                             "Final Score:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{score}", (255, 255, 255))


def get_username(screen, username, size):
    loc1 = (size[0] // 2 - 116, size[1] // 2 + 48)
    loc2 = (size[0] // 2, size[1] // 2 + 80)
    screen['font'].render_to(screen['screen'], loc1,
                             "Enter Name:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2,
                             f"{username}", (255, 255, 255))


def get_cheats(screen, cheats):
    cnt = 0
    for name, value in cheats.items():
        color = (255, 0, 0) if not value else (0, 255, 0)
        screen['font'].render_to(screen['screen'], (0, 36 * cnt),
                                 f"{cnt + 1}: {name}", color)
        cnt += 1
