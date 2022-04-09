from http.client import CONFLICT
import random
rounds=3
number_of_players=3
player_dictionary={}
player_bank={}
round_bank={}
words_played={}
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
    current_player=0
    for i in range(number_of_players):
        player_input_name=Get_Name(i)
        player_dictionary[i]=player_input_name
        player_bank[player_input_name]=0
    for i in range(rounds):
        current_player=Play_Round(i+1,current_player)
    

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
def Play_Round(int1,int2):
    if int1<rounds:
        current_player=Wheel_Round(int1,int2)
    else:
        Final_Round(int1)
        current_player=0
    return current_player
    
############################


def Wheel_Round(int1,int2):
    for player in player_bank.keys():
        round_bank[player]=0
    word_checked=False # has the word chosen been checked, begins False as no word chosen for the game yet so can't have been checked
    while not word_checked: # loop to check if is new word or not
        test_word=Get_Word() # get a word
        if test_word not in words_played.values(): # test if word is new
            word_checked=True # word is new so no need to recheck, change checked to True
            round_word=test_word # set round_word (the word to play) to the picked test_word
            words_played[int1]=round_word # add the new word to play to the played words set
    word_knowledge=list("_"*len(round_word)) # what the player knows about the word
    print(words_played)
    round_over = False
    current_player=int2
    print(player_bank)
    guessed_letters=set()
    while not round_over:
        print(f"It is {player_dictionary[current_player]}'s turn")
        turn_over = False
        while not turn_over:
            print(f"You ({player_dictionary[current_player]}) have ${round_bank[player_dictionary[current_player]]} available")
            print(word_knowledge)
            print(guessed_letters)
            choice=Turn_Menu()
            if choice == 1:
                consonants_remaining=False
                for i in range(len(round_word)):
                    if round_word[i] in {'B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z'}-guessed_letters:
                        consonants_remaining=True
                if consonants_remaining:
                    wheel_return=random.choice(wheel_values)
                    print(f"You landed on {wheel_return}.")
                    if wheel_return == 'Lose a Turn':
                        turn_over=True
                    elif wheel_return == 'Bankrupt':
                        round_bank[player_dictionary[current_player]]=0
                        turn_over=True
                    else:
                        not_repeat=False
                        while not not_repeat:
                            guess=Consonant_Guess()
                            if guess not in guessed_letters:
                                not_repeat=True
                            else:
                                print("That letter has already been guessed, try again")
                        guessed_letters.add(guess)
                        good_guess=Guess_Letter(round_word,guess)
                        if good_guess:
                            for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
                                if round_word[i]==guess: # replace values where appropriate
                                    word_knowledge[i]=round_word[i]
                                    round_bank[player_dictionary[current_player]]+=wheel_return
                        else:
                            turn_over=True
                else:
                    print("There are no unguessed consonants remaining.")
            elif choice == 2:
                round_over=Guess_Word(round_word)
                turn_over=True
            else:
                vowels_remaining=False
                for i in range(len(round_word)):
                    if round_word[i] in {'A','E','I','O','U'}-guessed_letters:
                        vowels_remaining=True
                if vowels_remaining:    
                    player_can_buy=Can_Buy_Vowel(current_player)
                    if player_can_buy:
                        round_bank[player_dictionary[current_player]]-=250
                        not_repeat=False
                        while not not_repeat:
                            guess=Vowel_Guess()
                            if guess not in guessed_letters:
                                not_repeat=True
                            else:
                                print("That letter has already been guessed, try again")
                        guessed_letters.add(guess)
                        good_guess=Guess_Letter(round_word,guess)
                        if good_guess:
                            for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
                                if round_word[i]==guess: # replace values where appropriate
                                    word_knowledge[i]=round_word[i]
                        else:
                            turn_over=True
                    else:
                        print("You do not have the funds to purchase a vowel.")
                else:
                    print("There are no more vowels to be guessed in the word.")
        current_player=(current_player+1)%number_of_players
    for player in player_bank.keys():
        player_bank[player]+=round_bank[player]
    return current_player


def Guess_Letter(str1,str2):
    if str1.find(str2)==-1: # check if letter not in word and not repeat guess
        print("That letter is not in the word")
        correct_guess=False
    else: 
        correct_guess=True
    return correct_guess


def Consonant_Guess():
    is_consonant=False
    while not is_consonant:
        guess=input("What consonant would you like to guess?\n")
        if len(guess)!=1:
            print("That wasn't one letter, try again")
        elif not guess.isalpha():
            print("That wasn't recognized as a letter, try again")
        elif guess.upper() in {'A','E','I','O','U'}:
            print("That was not recognized as a consonant, try again")
        else:
            is_consonant = True
    return guess.upper()


def Guess_Word(str1):
    user_guess=input("What word would you like to guess?\n")
    if user_guess.upper()!=str1: # check if word is incorrect and not a repeat
        print("That is incorrect.")
        correct_guess=False
    else: # check if word not repeat
        print("You correctly guessed the word!  Congratulations!")
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
        else:
            is_vowel = True
    return guess.upper()


def Can_Buy_Vowel(int1):
    if round_bank[player_dictionary[int1]]>=250:
        sufficient_funds=True
    else:
        sufficient_funds=False
    return sufficient_funds


def Final_Round(int1):
    guessed_letters=set()
    current_player=Money_Leader()
    print(f"{player_dictionary[current_player]} has the most money entering the final round.")
    print(f"It is {player_dictionary[current_player]}'s turn.")
    input("You will be given one guess at the word after learning some information, hit enter to continue:")
    word_checked=False # has the word chosen been checked, begins False as no word chosen for the game yet so can't have been checked
    while not word_checked: # loop to check if is new word or not
        test_word=Get_Word() # get a word
        if test_word not in words_played: # test if word is new
            word_checked=True # word is new so no need to recheck, change checked to True
            round_word=test_word # set round_word (the word to play) to the picked test_word
            words_played[int1]=round_word # add the new word to play to the played words set
    word_knowledge=list("_"*len(round_word)) # what the player knows about the word
    for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
        if round_word[i] in {'R','S','T','L','N','E'}: # replace values where appropriate
            word_knowledge[i]=round_word[i]
    print(word_knowledge)
    print("The letters R,S,T,L,N,E have already been filled in.")
    print("Please guess 3 more consonants and one additional vowel.")
    for i in range(3):
        new_information=False
        while not new_information:
            guess=Consonant_Guess()
            if guess not in {'R','S','T','L','N'}.union(guessed_letters):
                new_information=True
                guessed_letters.add(guess)
            else:
                print("You already have information about that letter, please try again")
        for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
            if round_word[i]==guess: # replace values where appropriate
                word_knowledge[i]=guess
    new_information=False
    while not new_information:
        guess=Vowel_Guess()
        if guess not in {'E'}:
            new_information=True
        else:
            print("You already have information about that letter, please try again")
    for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
        if round_word[i]==guess: # replace values where appropriate
            word_knowledge[i]=guess
    print(word_knowledge)
    win_money=Guess_Word(round_word)
    if win_money:
        Big_Reward(current_player)
    print(f"The word was {round_word}")
    print("Thanks for playing, goodbye!")
    print(f"Final Bank totals: {player_bank}")


def Big_Reward(int1):
    grand_prize=2500
    print(f"For correctly guessing the final word, you've won ${grand_prize}")
    player_bank[player_dictionary[int1]]+=grand_prize



def Money_Leader():
    max_money=0
    for player_id in player_dictionary.keys():
        if player_bank[player_dictionary[player_id]]>max_money:
            most_money=player_id
            max_money=player_bank[player_dictionary[player_id]]
    return most_money  
       

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
