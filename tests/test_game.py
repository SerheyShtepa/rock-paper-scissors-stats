import pytest
from rps.game import determine_winner, input_choice, computer_choice
from unittest.mock import patch

@pytest.mark.parametrize(
    "player_move, computer_move, expected",
    [
        ("r", "r", "draw"),
        ("r", "p", "lose"),
        ("r", "s", "win"),
        ("p", "r", "win"),
        ("p", "p", "draw"),
        ("p", "s", "lose"),
        ("s", "r", "lose"),
        ("s", "p", "win"),
        ("s", "s", "draw"),
    ]
)

def test_determine_winner(player_move, computer_move, expected):
    result = determine_winner(player_move, computer_move)
    assert result["result"] == expected

@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("r", "r"),
        ("s", "s"),
        ("p", "p"),
        ("esc", "Good bye"),
        ("st", "stats"),
        ("x", "Invalid choice!"),
    ]
)

def test_input_choice(user_input, expected):
    with patch("builtins.input", return_value=user_input):
        assert input_choice() == expected

@pytest.mark.parametrize(
    "predicted_value, expected",
    [
        ("r", "p"),
        ("p", "s"),
        ("s", "r"),
    ]
)
def test_computer_choice_predicted(predicted_value, expected):
    with patch("rps.game.analyze_game", return_value=predicted_value):
        result = computer_choice()
        assert result == expected


@pytest.mark.parametrize(
    "random_value, expected",
    [
        ("r", "r"),
        ("s", "s"),
        ("p", "p"),
    ]
)

def test_computer_choice_random(random_value, expected):
    with patch("rps.game.analyze_game", return_value=None):
        with patch("rps.game.random.choice", return_value=random_value):
            result = computer_choice()
            assert result == expected