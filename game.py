import random

def guessing_game():
    print("🎮 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("Can you guess it?\n")

    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    while attempts < max_attempts:
        attempts_left = max_attempts - attempts
        print(f"You have {attempts_left} attempt(s) left.")

        # Get the player's guess
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("⚠️  Please enter a valid number!\n")
            continue

        attempts += 1

        # Check the guess
        if guess < secret_number:
            print("📉 Too low! Try higher.\n")
        elif guess > secret_number:
            print("📈 Too high! Try lower.\n")
        else:
            print(f"🎉 Correct! The number was {secret_number}.")
            print(f"You got it in {attempts} attempt(s). Well done!")
            return

    print(f"\n💀 Game over! The number was {secret_number}. Better luck next time!")

# Run the game
guessing_game()
