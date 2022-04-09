import random
rounds=3
number_of_players=3
current_round=1
current_player=0
player_dictionary={}
player_bank={}
round_bank={}
words_played=set()
guessed_letters=set()
word_knowledge=set()
wheel_values=['Lose a Turn','Bankrupt',100,
200,300,400,500,600,700,800,
900,450,550,500,350,400,450,
550,600,650,250,150,750,850]

def Get_Word():
    words_file=open("words_alpha(word list from gitHub).txt") # open list file to read in data
    file_contents=words_file.read() # read in file data
    file_contents=file_contents.upper() # cast letters to UPPERCASE for convenience
    list_of_words=file_contents.splitlines() # turn list file data into a list
    words_file.close() # close list file
    word=random.choice(list_of_words) # chose a random word from the list
    return word

def Welcome():
    print("Welcome to the Wh__l _f F_rtun_")
    print(f"This game is set for {number_of_players} players to play {rounds} rounds, no exceptions.")
    for i in range(number_of_players):
        player_input_name=Get_Name(i)
        player_dictionary[i]=player_input_name
        player_bank[player_input_name]=0
    

###########################
def Get_Name(int1):
    unique_name = False
    while not unique_name:
        player_name=input(f"Please enter a name for player {int1+1} (all names converted to UPPERCASE)\n").upper()
        if player_name in player_dictionary.values():
            print("That name is already in use, please enter a different one")
        else:
            unique_name = True
    return player_name
###########################

###########################
def Play_Round(int1):
    for i in guessed_letters:
        guessed_letters.remove(i)
    for player in player_bank.keys():
        round_bank[player]=0
    if int1<rounds:
        Wheel_Round()
    else:
        Final_Round()
    for player in player_bank.keys():
        player_bank[player]+=round_bank[player]
############################


def Wheel_Round():
    word_checked=False # has the word chosen been checked, begins False as no word chosen for the game yet so can't have been checked
    while not word_checked: # loop to check if is new word or not
        test_word=Get_Word() # get a word
        if test_word not in words_played: # test if word is new
            word_checked=True # word is new so no need to recheck, change checked to True
            round_word=test_word # set round_word (the word to play) to the picked test_word
            words_played.add(round_word) # add the new word to play to the played words set
    word_knowledge=list("_"*len(round_word)) # what the player knows about the word
    
    round_over = False
    while not round_over:
        print(f"It is {player_dictionary[current_player]}'s turn")
        turn_over = False
        while not turn_over:
            print(f"You ({player_dictionary[current_player]}) have ${round_bank[player_dictionary[current_player]]} available")
            choice=Turn_Menu()
            if choice == 1:
                turn_over=Spin_Wheel(round_word,current_player)
            elif choice == 2:
                round_over=Guess_Word(round_word)
                turn_over=True
            else:
                player_can_buy=Can_Buy_Vowel(current_player)
                if player_can_buy:
                    round_bank[player_dictionary[current_player]]-=250
                    turn_over=Buy_Vowel(round_word)
                else:
                    print("You do not have the funds to purchase a vowel.")


def Spin_Wheel(str1,int1):
    wheel_return=random.choice(wheel_values)
    if wheel_return == 'Lose a Turn':
        turn_continues=False
    elif wheel_return == 'Bankrupt':
        round_bank[player_dictionary[int1]]=0
        turn_continues=False
    else:
        Guess_Consonant(str1,int1,wheel_return)
        turn_continues=True
    return turn_continues


def Guess_Consonant(str1,int1,int2):
    letter_guess=Consonant_Guess()
    guessed_letters.add(letter_guess)
    if str1.find(letter_guess)==-1: # check if letter not in word and not repeat guess
        print("That letter is not in the word")
        correct_guess=False
    else: 
        for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
            if str1[i]==letter_guess: # replace values where appropriate
                word_knowledge[i]=letter_guess
                round_bank[player_dictionary[int1]]+=int2
        correct_guess=True
    return correct_guess


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


def Guess_Word(str1):
    user_guess=input("What word would you like to guess?\n")
    if user_guess!=str1: # check if word is incorrect and not a repeat
        print("That is incorrect.")
        correct_guess=False
    else: # check if word not repeat
        print("You correctly guessed the word!  Congratulations, you won!")
        correct_guess=True
    return correct_guess
        
def Vowel_Guess():
    is_vowel = False
    while not is_vowel:
        guess=input("What vowel would you like to guess?\n")
        if len(guess) != 1:
            print("That wasn't one letter, try again")
        elif not guess.isalpha():
            print("That wasn't recognized as a letter, try again")
        elif guess.upper() not in {'A','E','I','O','U'}:
            print("That was not recognized as a vowel, try again")
        elif guess in guessed_letters:
            print("That letter has already been guessed, try again")
        else:
            is_vowel = True
    return guess.upper()

def Buy_Vowel(str1):
    letter_guess=Vowel_Guess()
    guessed_letters.add(letter_guess)
    if str1.find(letter_guess)==-1: # check if letter not in word and not repeat guess
        print("That letter is not in the word")
        correct_guess=False
    else: 
        for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
            if str1[i]==letter_guess: # replace values where appropriate
                word_knowledge[i]=letter_guess
        correct_guess=True
    return correct_guess


def Can_Buy_Vowel(int1):
    if round_bank[player_dictionary[int1]]>=250:
        sufficient_funds=True
    else:
        sufficient_funds=False
    return sufficient_funds


def Final_Round():
    max_money=0
    for player in player_bank.keys():
        if player_bank[player]>max_money:
            most_money=player
    print(most_money)
        

##################################
def Turn_Menu():
    print("Turn Menu")
    print("====================")
    print("1: Guess a consonant")
    print("2: Guess the word")
    print("3: Buy a vowel")
    choice_made = False
    while not choice_made:
        turn_choice=input("What would you like to do?\n")
        if turn_choice in {'1','2','3'}:
            turn_choice = int(turn_choice)
            choice_made = True
        else:
            print("That is not a recognized option, please try again")
    return turn_choice
##################################



Welcome()
