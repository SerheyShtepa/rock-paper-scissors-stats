import tkinter as tk
from rps.stats import load_results, basic_stats, reset_game
from rps.game import play_round, CHOICE

player_coins = 50
computer_coins = 50
bank_coins = 0


def coins(outcome):
    global player_coins, computer_coins, bank_coins
    if player_coins > 0 and computer_coins > 0:
        player_coins -= 1
        computer_coins -= 1
        bank_coins += 2

    result = outcome["result"]["result"]
    if result == "win":
        player_coins += bank_coins
        bank_coins = 0
    elif result == "lose":
        computer_coins += bank_coins
        bank_coins = 0


def check_end_game():
    if player_coins <= 0:
        output_result.set(output_result.get() + "\n💀 You ran out of coins! Game Over!")
    elif computer_coins <= 0:
        output_result.set(output_result.get() + "\n🏆 Computer ran out of coins! You Win!")


def play(move):
    outcome = play_round(move)
    output_result.set(
        f"You chose {CHOICE[move]}, computer chose {CHOICE[outcome['computer move']]}.\n"
        f"Result: {outcome['result']['result'].upper()}"
    )
    coins(outcome)
    show_stats()
    check_end_game()


def show_stats():
    df = load_results()
    stats = basic_stats(df)
    output_stats.set(
        f"💰 Coins — You: {player_coins} | Computer: {computer_coins} | Bank: {bank_coins}\n"
        f"📊 Games: {stats['total_games']}\n"
        f"Wins: {stats['wins']}, Losses: {stats['losses']}, Draws: {stats['draws']}\n"
        f"Win rate: {stats['win_rate']:.1f}%\n"
        f"Most common: {stats['most_common_player_choice']}"
    )


def new_game():
    global player_coins, computer_coins, bank_coins
    reset_game()
    output_result.set("New game started!")
    show_stats()
    player_coins = 50
    computer_coins = 50
    bank_coins = 0


def create_gui():
    global output_stats, output_result
    root = tk.Tk()
    root.title("Rock Paper Scissors")
    root.geometry("350x400")

    tk.Label(root, text="Choose your move:", font=("Arial", 14)).pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    for key, name in CHOICE.items():
        tk.Button(btn_frame, text=name.title(), width=10,
                  command=lambda k=key: play(k)).pack(side=tk.LEFT, padx=5)

    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)
    tk.Button(root, text="New Game", command=new_game).pack(pady=5)

    output_result = tk.StringVar()
    tk.Label(root, textvariable=output_result, wraplength=300, justify="center",
             font=("Arial", 12, "bold")).pack(pady=10)

    output_stats = tk.StringVar()
    tk.Label(root, textvariable=output_stats, wraplength=300, justify="center").pack(pady=10)

    show_stats()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
