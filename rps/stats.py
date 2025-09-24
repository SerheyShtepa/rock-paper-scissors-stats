from pathlib import Path
import pandas as pd
from datetime import datetime

DEFAULT_COLUMNS = ["player", "computer", "result", "timestamp"]
DEFAULT_PATH = Path(__file__).parent.parent / "data" / "result.csv"


def load_results(path: Path | str = DEFAULT_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    try:
        df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[DEFAULT_COLUMNS]


def append_result(result: dict, path: Path | str = DEFAULT_PATH) -> None:
    path = Path(path)
    df = load_results(path)

    new_row = pd.DataFrame([{
        "player": result.get("player"),
        "computer": result.get("computer"),
        "result": result.get("result"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def basic_stats(df: pd.DataFrame) -> dict:
    total_games = len(df)
    wins = (df["result"] == "win").sum()
    losses = (df["result"] == "lose").sum()
    draws = (df["result"] == "draw").sum()

    most_common_player = df["player"].mode().iloc[0] if not df.empty else None
    win_rate = (wins / total_games * 100) if total_games > 0 else 0

    return {
        "total_games": total_games,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": win_rate,
        "most_common_player_choice": most_common_player
    }


def reset_game():
    df = pd.DataFrame(columns=DEFAULT_COLUMNS)
    DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DEFAULT_PATH, index=False)
