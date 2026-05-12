import json


def load_scorers(score_loc):
    scores = {}
    try:
        with open(score_loc, "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return {}
    return scores


def fill_scorers(scorers, user, score_loc):
    scorers.update(user)
    n_scorers = {k: v for k, v in sorted(scorers.items(),
                                         key=lambda item: item[1],
                                         reverse=True)}
    scorers = n_scorers
    while len(scorers) > 10:
        scorers.popitem()
    try:
        with open(score_loc, "w") as f:
            json.dump(scorers, f)
        return scorers
    except Exception:
        raise ("Error")
