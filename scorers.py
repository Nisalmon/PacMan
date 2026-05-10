import json


def load_scorers(score_loc):
    scores = {}
    try:
        with open(score_loc) as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return {}
    return scores