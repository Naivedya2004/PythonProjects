import random
import string
from words import words

def hangman():
    word_letters = set(words)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 6

    while len(word_letters) > 0 and lives > 0:
        print('you have ', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in words]
        print('current word: ', ''.join(word_list))

     

    user_letter = input('guess a letter: ').upper()
    if user_letter in alphabet - used_letters:
        used_letters.add(user_letter)
        if user_letter in word_letters:
            word_letters.remove(user_letter)

    elif user_letter in used_letters:
        print('you have already used that character. ')

    else:
        print('invalid character')

    



hangman()


user_input = input('type something: ')
print(user_input)

 

