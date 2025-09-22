import pytest
import pandas as pd
from rps.stats import load_results, append_result, basic_stats


def test_load_results_empty(tmp_path):
    file_path = tmp_path / "nonexistent.csv"
    df = load_results(file_path)
    assert list(df.columns) == ["player", "computer", "result", "timestamp"]
    assert len(df) == 0


def test_append_result(tmp_path):
    file_path = tmp_path / "results.csv"
    result = {"player": "rock", "computer": "scissors", "result": "win"}

    append_result(result, file_path)
    df = pd.read_csv(file_path)

    assert df.iloc[0]["player"] == "rock"
    assert df.iloc[0]["computer"] == "scissors"
    assert df.iloc[0]["result"] == "win"
    assert "timestamp" in df.columns


def test_basic_stats():
    data = {
        "player": ["rock", "paper", "rock"],
        "computer": ["scissors", "rock", "rock"],
        "result": ["win", "win", "draw"],
        "timestamp": ["2025-09-22 10:00:00"] * 3
    }
    df = pd.DataFrame(data)
    stats = basic_stats(df)

    assert stats["total_games"] == 3
    assert stats["wins"] == 2
    assert stats["losses"] == 0
    assert stats["draws"] == 1
    assert stats["win_rate"] == pytest.approx(66.666, 0.1)
    assert stats["most_common_player_choice"] == "rock"
