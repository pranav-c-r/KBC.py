"""
Handles user interaction, restart logic, and checkpoint rules.
"""
from kbc_module import load_questions_from_csv,KBCGame
import os

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def run_game():
    questions=load_questions_from_csv('questions.csv')
    if not questions:
        print("No questions loaded.Check questions.csv.")
        return
    game=KBCGame(questions)

    while True:
        clear_console()
        print("\nWelcome to Kaun Banega Crorepati-Python Edition!\n")
        name=input("Enter your name: ").strip() or "Anonymous"
        game.reset_game_state()
        game.player_name=name
        
        try:
            selected=game.select_questions_for_game()
        except ValueError as e:
            print(e)
            return
        
        for idx,q in enumerate(selected,start=1):
            game.current_qno=idx
            # Offer quit before checkpoint
            if game.is_checkpoint(idx):
                print(f"\nQuestion {idx} is a decisive one.")
                print(f"You currently have ₹{game.current_winnings}.")
                while True:
                    opt = input("Enter 'c' to continue or 'q' to quit: ").lower().strip()
                    if opt in ('c','q'):
                        break
                    print("Invalid input.")
                if opt=='q':
                    print(f"You walk away with ₹{game.current_winnings}.")
                    KBCGame.save_score_to_csv(name,game.current_winnings)
                    break

            correct, _=game.ask_question(idx,q)
            if correct:
                game.current_winnings=game.get_prize_for_qno(idx)
                print(f"Correct! You’ve won ₹{game.current_winnings}")
                if idx==10:
                    print(f"\nCongrats {name}! You won the Jackpot of ₹{game.current_winnings}!")
                    KBCGame.save_score_to_csv(name,game.current_winnings)
                    break
            else:
                print("\nWrong answer.")
                if game.is_checkpoint(idx):
                    print("Decisive question—you lose all winnings.")
                    game.current_winnings=0
                else:
                    last_cp=game.last_passed_checkpoint_amount(idx-1)
                    game.current_winnings=last_cp
                    if last_cp:
                        print(f"You keep ₹{last_cp} (last checkpoint).")
                    else:
                        print("No checkpoints cleared. You get ₹0.")
                KBCGame.save_score_to_csv(name,game.current_winnings)
                break

        # restart?
        while True:
            again=input("\nPlay again? (y/n): ").lower().strip()
            if again=='y':
                break
            elif again=='n':
                print("Thanks for playing!")
                return
            else:
                print("Please enter y/n.")

# start game.                
if __name__=="__main__":
    run_game()
