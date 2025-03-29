#string concatenation
#suppose we want to create some string that says "subscribe to ____"
youtuber = 'naivedya' #some string variable


print("subscribe to " + youtuber)
print(" subscribe to {}".format(youtuber))
print(f" subscribe to {youtuber}")

adj = input("adjective: ")
verb1 = input("verb: ")
verb2 = input("verb: ")
famous_person = input("Famous person: ")


madlib = f"computer programming is so {adj}! It makes me so excited all the time beacause \
    I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}! " 

print(madlib)
