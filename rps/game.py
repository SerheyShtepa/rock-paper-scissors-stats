import random
from stats import append_result, load_results, basic_stats
from scripts.analyze import analyze_game

CHOICE = {
    "r": "rock",
    "p": "paper",
    "s": "scissors"
}
WINS_AGAINST = {
    "r": "s",
    "p": "r",
    "s": "p"
}
LOSE_AGAINST = {
    "r": "p",
    "p": "s",
    "s": "r"
}

PATTERN_LENGTH = 2

def input_choice() -> str:
    players_choice = input("Enter your choice (r - rock, p - paper, s - scissors, esc - for break): ").lower()
    if players_choice not in CHOICE and players_choice != "esc":
        return "Invalid choice!"
    elif players_choice == "esc":
        return "Good bye"
    else:
        return players_choice

def computer_choice() -> str:
    predicted = analyze_game(PATTERN_LENGTH)
    if predicted:
        return LOSE_AGAINST[predicted]
    else:
        return random.choice(list(CHOICE.keys()))


def determine_winner(player_move: str, computer_move: str) -> dict:
    result = {"player": CHOICE[player_move], "computer": CHOICE[computer_move], "result": ""}
    if player_move == computer_move:
        result["result"] = "draw"
    elif WINS_AGAINST[player_move] == computer_move:
        result["result"] = "win"
    else:
        result["result"] = "lose"
    return result

if __name__ == "__main__":
    while True:
        player_move = input_choice()

        if player_move == "Good bye":
            print("Good bye")
            break
        elif player_move == "Invalid choice!":
            print("Invalid choice!")
            continue

        comp_move = computer_choice()
        result = determine_winner(player_move, comp_move)
        append_result(result)
        df = load_results()
        stats = basic_stats(df)
        #TODO
        # add statistic with another function
        # print(
        #     f"Total games: {stats['total_games']},"
        #     f"Wins: {stats['wins']},"
        #     f"Losses: {stats['losses']},"
        #     f"Draws: {stats['draws']},"
        #     f"Win rate: {stats['win_rate']:.1f}%,"
        #     f"Most common choice: {stats['most_common_player_choice']}"
        # )
        print(f"You chose {CHOICE[player_move]}, computer chose {CHOICE[comp_move]}")
        print(result)
