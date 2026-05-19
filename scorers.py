import json
from typing import Dict


def load_scorers(score_loc: str) -> Dict[str, int]:
    scores: Dict[str, int] = {}
    try:
        with open(score_loc, "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return {}
    return scores


def fill_scorers(scorers: Dict[str, int],
                 user: Dict[str, int],
                 score_loc: str) -> Dict[str, int]:
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
        print("Error")
        return {
            "ERROR": 1000000
        }
