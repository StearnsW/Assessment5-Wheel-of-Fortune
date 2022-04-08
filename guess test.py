guessed_letters=set()
word='apple'
word=word.upper()
word_knowledge= list("_"*len(word))
def Guess_Consonant(str1):
    letter_guess=Consonant_Guess()
    guessed_letters.add(letter_guess)
    if str1.find(letter_guess)==-1: # check if letter not in word and not repeat guess
        print("That letter is not in the word")
    else: 
        for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
            if str1[i]==letter_guess: # replace values where appropriate
                word_knowledge[i]=letter_guess

def Consonant_Guess():
    is_consonant = False
    while not is_consonant:
        guess=input("What consonant would you like to guess?\n")
        if len(guess) != 1:
            print("That wasn't one letter, try again")
        elif not guess.isalpha():
            print("That wasn't recognized as a letter, try again")
        elif guess.upper() in {'A','E','I','O','U'}:
            print("That was not recognized as a consonant, try again")
        elif guess in guessed_letters:
            print("That letter has already been guessed, try again")
        else:
            is_consonant = True
    return guess.upper()
Guess_Consonant(word)
print(word_knowledge)