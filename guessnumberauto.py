import random

def guess(x):
    random_number = random.randint(1, x) #between 1 and x ki range
    guess = 0
    while guess != random_number:
        guess = int(input(f"guess a number between 1 and {x}: "))
        if guess < random_number:
            print("too low")
        elif guess > random_number:
            print("too high")
    
    print(f"that is the correct guess {random_number}. ")

guess(10)






