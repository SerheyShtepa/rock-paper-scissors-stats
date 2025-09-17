import random
from pathlib import Path
import json
from rps.stats import load_results, basic_stats


def show_basic_stats():
    df = load_results()
    stats = basic_stats(df)

    print(f"Total games: {stats['total_games']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Draws: {stats['draws']}")
    print(f"Win rate: {stats['win_rate']:.1f}%")
    print(f"Most common choice: {stats['most_common_player_choice']}")


def update_pattern_stats(pattern_stats, pattern, next_move):
    if pattern not in pattern_stats:
        pattern_stats[pattern] = {"r": 0, "p": 0, "s": 0}
    pattern_stats[pattern][next_move] += 1


def predict_next_move(pattern_stats, last_moves, pattern_length=2) -> str:
    last_pattern = tuple(last_moves[-pattern_length:])

    if last_pattern not in pattern_stats:
        return random.choice(["r", "p", "s"])

    next_moves = pattern_stats[last_pattern]
    predicted_move = max(next_moves, key=next_moves.get)
    return predicted_move


def learn_patterns(df, pattern_length=2) -> dict:
    local_pattern_stats = {}
    CHOICE_SHORT = {"rock": "r", "paper": "p", "scissors": "s"}

    for i in range(len(df) - pattern_length):
        pattern = tuple(
            (df.iloc[j]["player"], df.iloc[j]["result"])
            for j in range(i, i + pattern_length)
        )
        next_move = df.iloc[i + pattern_length]["player"]
        next_move_short = CHOICE_SHORT[next_move]

        if pattern not in local_pattern_stats:
            local_pattern_stats[pattern] = {"r": 0, "p": 0, "s": 0}
        local_pattern_stats[pattern][next_move_short] += 1

    return local_pattern_stats


def save_pattern_stats(pattern_stats: dict, path: Path | str = Path("../data/pattern_stats.json")) -> None:

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {}
    for key, counts in pattern_stats.items():
        if isinstance(key, tuple):
            sk = "|".join(map(str, key))
        else:
            sk = str(key)
        serializable[sk] = counts
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(serializable, ensure_ascii=False, indent=2))
    tmp.replace(path)



def analyze_game(pattern_length) -> str:
    df = load_results()
    if len(df) < 1:
        return None
    pattern_stats = learn_patterns(df, pattern_length=pattern_length)

    last_moves = [(df.iloc[i]["player"], df.iloc[i]["result"]) for i in range(len(df))]
    predicted_move = predict_next_move(pattern_stats, last_moves, pattern_length=pattern_length)

    save_pattern_stats(pattern_stats)
    return predicted_move
if __name__ == "__main__":
    print(analyze_game(2))