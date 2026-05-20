import json
from typing import Dict


def load_config(file: str) -> Dict[str, str | int]:
    conf: Dict[str, int | str] = {}
    try:
        with open(file) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("There is a problem with the config.json file.")
        return {}
    try:
        for elem in config:
            for key, value in elem.items():
                conf[key] = value
    except Exception:
        print("An error occured during the config parsing.")
        return {}
    return conf


def check_size(conf: Dict[str, str | int]) -> None:
    try:
        w: int = int(conf['width'])
        h: int = int(conf['height'])
        if w > 15 or w < 11 or h > 15 or h < 11:
            print("Width and Height must be ranging from 11 to 15 !")
            print("Setting them to default values : 15.")
            conf['width'] = 15
            conf['height'] = 15
    except KeyError:
        print("Keys for width and/or height are missing !")
        print("Setting them to default values : 15.")
        conf['width'] = 15
        conf['height'] = 15


def check_lives(conf: Dict[str, str | int]) -> None:
    try:
        lvs: int = int(conf['lives'])
        if lvs <= 0 or not isinstance(lvs, int):
            print("Lives must be an integer greater than 0 !")
            print("Setting lives to 3.")
            conf['lives'] = 3
    except KeyError:
        print("Key for lives is missing !")
        print("Setting lives to 3.")
        conf['lives'] = 3


def check_time(conf: Dict[str, str | int]) -> None:
    try:
        t: int = int(conf['level_max_time'])
        if t <= 0 or not isinstance(t, int):
            print("Time must be an integer greater than 0 !")
            print("Setting level_max_time to 3.")
            conf['level_max_time'] = 300
    except KeyError:
        print("Key for level_max_time is missing !")
        print("Setting level_max_time to 300.")
        conf['level_max_time'] = 300


def check_pacgum(conf: Dict[str, str | int]) -> None:
    try:
        pg: int = int(conf['pacgums'])
        if pg <= 0 or not isinstance(pg, int):
            print("Pacgums must be an integer greater than 0 !")
            print("Setting pacgums to 100.")
            conf['pacgums'] = 100
    except KeyError:
        print("Key for pacgums is missing !")
        print("Setting pacgums to 100.")
        conf['pacgums'] = 100


def check_pacgum_score(conf: Dict[str, str | int]) -> None:
    try:
        pg: int = int(conf['points_per_pacgum'])
        if pg <= 0 or not isinstance(pg, int):
            print("Pacgums score must be an integer greater than 0 !")
            print("Setting points_per_pacgum to 10.")
            conf['points_per_pacgum'] = 10
    except KeyError:
        print("Key for points_per_pacgum is missing !")
        print("Setting points_per_pacgum to 10.")
        conf['points_per_pacgum'] = 10


def check_super_pacgum_score(conf: Dict[str, str | int]) -> None:
    try:
        pg: int = int(conf['points_per_super_pacgum'])
        if pg <= 0 or not isinstance(pg, int):
            print("Super pacgums score must be an integer greater than 0 !")
            print("Setting points_per_super_pacgum to 50.")
            conf['points_per_super_pacgum'] = 50
    except KeyError:
        print("Key for points_per_super_pacgum is missing !")
        print("Setting points_per_super_pacgum to 50.")
        conf['points_per_super_pacgum'] = 50


def check_ghost_score(conf: Dict[str, str | int]) -> None:
    try:
        g: int = int(conf['points_per_ghost'])
        if g <= 0 or not isinstance(g, int):
            print("Ghost score must be an integer greater than 0 !")
            print("Setting points_per_ghost to 200.")
            conf['points_per_ghost'] = 200
    except KeyError:
        print("Key for points_per_ghost is missing !")
        print("Setting points_per_ghost to 200.")
        conf['points_per_ghost'] = 200


def check_seed(conf: Dict[str, str | int]) -> None:
    try:
        sd: int = int(conf['seed'])
        if sd < 0 or not isinstance(sd, int):
            print("Seed must be an integer greater than 0 !")
            print("Setting seed to 0.")
            conf['seed'] = 0
    except KeyError:
        print("Key for seed is missing !")
        print("Setting seed to 0.")
        conf['seed'] = 0


def check_highscorers(conf: Dict[str, str | int]) -> None:
    try:
        if not str(conf['highscore_filename']).endswith(".json"):
            raise Exception()
        with open(conf['highscore_filename'], "r") as _:
            pass
    except (json.JSONDecodeError, FileNotFoundError,
            PermissionError, KeyError, Exception):
        print("An error occured when processing highscorers.")
        print("Setting highscore_filename to default value:")
        print("highscores.json")
        conf['highscore_filename'] = "highscores.json"


def check_level(conf: Dict[str, str | int]) -> None:
    try:
        lvl: int = int(conf['level'])
        if lvl <= 0 or not isinstance(lvl, int):
            print("Level must be an integer higher than 0 !")
            print("Setting it to default value: 10")
            conf['level'] = 10
    except KeyError:
        print("The level key is missing.")
        print("Setting level to default value: 10")
        conf['level'] = 10


def check_conf(conf: Dict[str, str | int]) -> None:
    check_size(conf)
    check_time(conf)
    check_lives(conf)
    check_pacgum(conf)
    check_pacgum_score(conf)
    check_super_pacgum_score(conf)
    check_ghost_score(conf)
    check_seed(conf)
    check_highscorers(conf)
    check_level(conf)
