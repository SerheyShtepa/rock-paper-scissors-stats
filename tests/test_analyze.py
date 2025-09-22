import pytest
import pandas as pd
from unittest.mock import patch
from scripts.analyze import update_pattern_stats, predict_next_move, learn_patterns, analyze_game

def test_update_pattern_stats_creates_and_updates():
    stats = {}
    update_pattern_stats(stats, ("r", "win"), "p")
    assert ("r", "win") in stats
    assert stats[("r", "win")]["p"] == 1
    update_pattern_stats(stats, ("r", "win"), "p")
    assert stats[("r", "win")]["p"] == 2

def test_predict_next_move_known_pattern():
    pattern_stats = {("a", "b"): {"r": 2, "p": 5, "s": 1}}
    last_moves = ["a", "b"]
    result = predict_next_move(pattern_stats, last_moves, pattern_length=2)
    assert result == "p"

def test_predict_next_move_unknown_pattern(monkeypatch):
    monkeypatch.setattr("scripts.analyze.random.choice", lambda seq: "s")
    pattern_stats = {}
    last_moves = ["x", "y"]
    result = predict_next_move(pattern_stats, last_moves, pattern_length=2)
    assert result == "s"

def test_learn_patterns_counts():
    df = pd.DataFrame([
        {"player": "rock", "result": "win"},
        {"player": "paper", "result": "lose"},
        {"player": "scissors", "result": "win"},
    ])
    stats = learn_patterns(df, pattern_length=2)
    assert len(stats) == 1
    key = next(iter(stats))
    counts = stats[key]
    assert counts["s"] == 1
    assert counts["r"] == 0
    assert counts["p"] == 0

def test_analyze_game_with_prediction(tmp_path):
    df = pd.DataFrame([
        {"player": "rock", "result": "win"},
        {"player": "paper", "result": "lose"},
        {"player": "scissors", "result": "win"},
    ])

    with patch("scripts.analyze.load_results", return_value=df):
        with patch("scripts.analyze.save_pattern_stats") as mock_save:
            result = analyze_game(pattern_length=2)
            assert result in {"r", "p", "s"}
            mock_save.assert_called_once()
