import random
import sys

answer = random.randint(1, 100)

print("Guess an integer between 1 and 100:")

guess = input("Guess:")

while True:
    while True:
        try:
            guess_number = int(guess)
            break
        except ValueError:
            print("This is not an integer! Please guess again.")

    if guess_number == answer:
        print("Congratulations! You have guessed the number :D")
        break
    else:
        print("That is not the number!!!! Try again.")
        guess = input("Guess:")