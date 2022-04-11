import random

rounds=3 # number of rounds to be played
number_of_players=3 # number of players in game
player_dictionary={} # blank dictionary to keep track of the player names
player_bank={} # blank dictionary to keep track of overall player money
round_bank={} # blank dictionary to keep track of player money each round before banking
words_played={} # blank dictionary to keep track of which words have been played which round
wheel_values=['Lose a Turn','Bankrupt',100,
200,300,400,500,600,700,800,
900,150,250,350,450,550,650,
750,850,400,450,500,550,600] # list of values to simulate wheel

########################### function to get a word from the list for the round
def Get_Word():
    words_file=open("words_alpha(word list from gitHub).txt") # open list file to read in data
    file_contents=words_file.read() # read in file data
    file_contents=file_contents.upper() # cast letters to UPPERCASE for convenience
    list_of_words=file_contents.splitlines() # turn list file data into a list
    words_file.close() # close list file
    word=random.choice(list_of_words) # chose a random word from the list
    return word
###########################

########################### function to play the game, prints a welcome, get player names, and runs the games
def Welcome():
    print("Welcome to the Wh__l _f F_rtun_") # welcome message
    print(f"This game is set for {number_of_players} players to play {rounds} rounds, no exceptions.") # game explaination
    current_player=0 # player_id for first player
    for i in range(number_of_players): # loop to get names and populate the player_dictionary and player_bank
        player_input_name=Get_Name(i)
        player_dictionary[i]=player_input_name # player keys 0,1,2, values the player names
        player_bank[player_input_name]=0 # all bank values start at 0, keys the inputted name
    for i in range(rounds): # loop to play the rounds
        current_player=Play_Round(i+1,current_player) # run function to play the round by round number and current player
###########################    

########################### function to get names of players, takes player number as input
def Get_Name(int1):
    unique_name=False
    while not unique_name: # loop to make sure names are unique so they can be used as keys
        player_name=input(f"Please enter a name for player {int1+1} (all names converted to UPPERCASE)\n").upper() # get user input
        if player_name in player_dictionary.values():
            print("That name is already in use, please enter a different one")
        else:
            unique_name=True
    return player_name # return inputted player_name
###########################

########################### function to play round, takes round number and current player, returns current player for next instance
def Play_Round(int1,int2):
    if int1<rounds: # check to make sure not last round
        current_player=Wheel_Round(int1,int2) # play a wheel round
    else:
        Final_Round(int1) # play the final round
        current_player=0
    return current_player # return current player
    
###########################

########################### function play wheel round, takes round number and current player as inputs, returns player to begin next round
def Wheel_Round(int1,int2):
    for player in player_bank.keys(): # loop to reset round bank
        round_bank[player]=0
    word_checked=False # has the word chosen been checked, begins False as no word chosen for the game yet so can't have been checked
    while not word_checked: # loop to check if is new word or not
        test_word=Get_Word() # get a word
        if test_word not in words_played.values(): # test if word is new
            word_checked=True # word is new so no need to recheck, change checked to True
            round_word=test_word # set round_word (the word to play) to the picked test_word
            words_played[int1]=round_word # add the new word to play to the played words set
    word_knowledge=list("_"*len(round_word)) # what the player knows about the word
    round_over=False
    current_player=int2 # set current_player to inputted value
    guessed_letters=set() # set of already guessed letters
    while not round_over: # loop to play the round
        print(f"It is {player_dictionary[current_player]}'s turn") # output who's round it is
        turn_over=False
        while not turn_over: # loop to play player's turn
            print(f"You ({player_dictionary[current_player]}) have ${round_bank[player_dictionary[current_player]]} available") # how much $ does the player have for this round
            print(f"The word:\n{word_knowledge}") # let the player what's already been guessed
            print(f"Guessed Letters:{guessed_letters}") # let the player
            choice=Turn_Menu() # display the choice menu and take the return to play the game
            if choice==1: # if the player chooses to spin the wheel
                consonants_remaining=False
                for i in range(len(round_word)): # loop to see if there are any consonants to play
                    if round_word[i] in {'B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z'}-guessed_letters:
                        consonants_remaining=True
                if consonants_remaining: # spins wheel to guess consonant if there are any consonants left to play
                    wheel_return=random.choice(wheel_values) # get an option from the wheel
                    print(f"You landed on {wheel_return}.") # display the results of the "wheel spin"
                    if wheel_return=='Lose a Turn': # end turn if Lose a Turn is returned by wheel
                        turn_over=True
                    elif wheel_return=='Bankrupt': # end turn if Bankrupt is returned by wheel, and change current_player's round_bank to 0
                        round_bank[player_dictionary[current_player]]=0
                        turn_over=True
                    else: # have player guess a consonant if wheel returns a $ value
                        not_repeat=False
                        while not not_repeat: # loop to make sure guess isn't a repeat
                            guess=Consonant_Guess()
                            if guess not in guessed_letters:
                                not_repeat=True
                            else:
                                print("That letter has already been guessed, try again")
                        guessed_letters.add(guess) # adds guess to guessed_letter
                        good_guess=Guess_Letter(round_word,guess) # run fuction to see if guess is in this round's word
                        if good_guess: # update knowledge
                            for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
                                if round_word[i]==guess: # replace values where appropriate
                                    word_knowledge[i]=round_word[i]
                                    round_bank[player_dictionary[current_player]]+=wheel_return
                        else: # end turn because of incorrect guess
                            turn_over=True
                    consonants_remaining=False
                    for i in range(len(round_word)): # check to see if the last guess was the last consonant
                        if round_word[i] in {'B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z'}-guessed_letters:
                            consonants_remaining=True
                    if not consonants_remaining:
                        print("That was the final consonant")
                else: # output if there are unguessed consonants
                    print("There are no unguessed consonants remaining.")
            elif choice==2: # lets the player guess a word
                round_over=Guess_Word(round_word)
                turn_over=True
            else: # lets the player buy a vowel
                vowels_remaining=False
                for i in range(len(round_word)): # loop to check if there are any remaining vowels
                    if round_word[i] in {'A','E','I','O','U'}-guessed_letters:
                        vowels_remaining=True
                if vowels_remaining: # lets player guess a vowel if there are any remaining
                    player_can_buy=Can_Buy_Vowel(current_player) # check to see if player has the money to buy a vowel
                    if player_can_buy:
                        round_bank[player_dictionary[current_player]]-=250 # charges player to buy vowel
                        not_repeat=False
                        while not not_repeat: # loop to make sure the player isn't repeating a vowel guess
                            guess=Vowel_Guess()
                            if guess not in guessed_letters:
                                not_repeat=True
                            else:
                                print("That letter has already been guessed, try again")
                        guessed_letters.add(guess) # add guess to guessed_letters
                        good_guess=Guess_Letter(round_word,guess) # check if guess is in the word
                        if good_guess:
                            for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
                                if round_word[i]==guess: # replace values where appropriate
                                    word_knowledge[i]=round_word[i]
                        else: # end turn if incorrect guess
                            turn_over=True
                    else:
                        print("You do not have the funds to purchase a vowel.")
                    vowels_remaining=False
                    for i in range(len(round_word)): # loop to see if last guess was the last vowel
                        if round_word[i] in {'A','E','I','O','U'}-guessed_letters:
                            vowels_remaining=True
                    if not vowels_remaining:
                        print("That was the last vowel")
                else:
                    print("There are no more vowels to be guessed in the word.")
        current_player=(current_player+1)%number_of_players # change current_player to next in order at end of turn
    for player in player_bank.keys(): # loop to bank money earned during round to overall bank
        player_bank[player]+=round_bank[player]
    return current_player # return current player for next round
###########################

########################### function to see if letter is in word, takes word and letter as input, returns truth of guess
def Guess_Letter(str1,str2):
    if str1.find(str2)==-1: # check if letter not in word and not repeat guess
        print("That letter is not in the word")
        correct_guess=False
    else: 
        correct_guess=True
    return correct_guess # return if guess is true or false
###########################

########################### function to get user consonant guess
def Consonant_Guess():
    is_consonant=False
    while not is_consonant: # loop to ensure valid input
        guess=input("What consonant would you like to guess?\n")
        if len(guess)!=1: # input too long
            print("That wasn't one letter, try again")
        elif not guess.isalpha(): # input not letter
            print("That wasn't recognized as a letter, try again")
        elif guess.upper() in {'A','E','I','O','U'}: # input a vowel
            print("That was not recognized as a consonant, try again")
        else: # input is a consonant
            is_consonant=True
    return guess.upper() # returns valid guess value
###########################

########################### function to guess word, takes round word as input, returns if guess is correct or not
def Guess_Word(str1):
    user_guess=input("What word would you like to guess?\n")
    if user_guess.upper()!=str1: # check if word is incorrect
        print("That is incorrect.")
        correct_guess=False
    else:
        print("You correctly guessed the word!  Congratulations!")
        correct_guess=True
    return correct_guess # return truth of guess==round_word
###########################

########################### function to guess vowel, returns guessed vowel
def Vowel_Guess():
    is_vowel=False
    while not is_vowel: # loop to make sure guess is a vowel
        guess=input("What vowel would you like to buy?\n")
        if len(guess)!=1: # make sure input is one letter
            print("That wasn't one letter, try again")
        elif not guess.isalpha(): # make sure guess is a letter
            print("That wasn't recognized as a letter, try again")
        elif guess.upper() not in {'A','E','I','O','U'}: # make sure guess is not not a vowel
            print("That was not recognized as a vowel, try again")
        else: # input is a vowel
            is_vowel=True
    return guess.upper() # return guessed vowel
###########################

########################### function to see if player has funds to buy a vowel, takes playerID as input, returns if funds sufficient
def Can_Buy_Vowel(int1):
    if round_bank[player_dictionary[int1]]>=250: # if round bank is above vowel cost ($250)
        sufficient_funds=True
    else:
        sufficient_funds=False
    return sufficient_funds
###########################

########################### function to play final round, takes round number as input
def Final_Round(int1):
    guessed_letters=set() # set of already guessed letters
    current_player=Money_Leader() # find out which player has the most money
    if current_player==-1: # deals with case where nobody has any money entering final round
        print('Since nobody has any money, the first player shall get to play the final round')
        current_player=0 # lets first player play final round
    else: # lets players know who will play the final round
        print(f"{player_dictionary[current_player]} has the most money entering the final round.")
    print(f"It is {player_dictionary[current_player]}'s turn.")
    input("You will be given one guess at the word after learning some information, hit enter to continue:") # breif overview of instructions
    word_checked=False # has the word chosen been checked, begins False as no word chosen for the game yet so can't have been checked
    while not word_checked: # loop to check if is new word or not
        test_word=Get_Word() # get a word
        if test_word not in words_played: # test if word is new
            word_checked=True # word is new so no need to recheck, change checked to True
            round_word=test_word # set round_word (the word to play) to the picked test_word
            words_played[int1]=round_word # add the new word to play to the played words dictionary
    word_knowledge=list("_"*len(round_word)) # what the player knows about the word
    for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
        if round_word[i] in {'R','S','T','L','N','E'}: # replace values where appropriate
            word_knowledge[i]=round_word[i]
    print(word_knowledge) # prints what is already known
    print("The letters R,S,T,L,N,E have already been filled in.") # lets the player understand why some letters are filled in
    print("Please guess 3 more consonants and one additional vowel.") # Explain what the player will be prompted for
    for i in range(3): # loop to get consonants 
        new_information=False
        while not new_information: # loop to ensure the player is guessing new things
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
    while not new_information: # loop to ensure the vowel guess is new information
        guess=Vowel_Guess()
        if guess!='E':
            new_information=True
        else:
            print("You already have information about that letter, please try again")
    for i in range(len(word_knowledge)): # loop through the blank locations to see which need replacing
        if round_word[i]==guess: # replace values where appropriate
            word_knowledge[i]=guess
    print(word_knowledge) # let the player know the new information
    win_money=Guess_Word(round_word) # have the player guess the final word
    print(f"The word was {round_word}") # let the player know what the word was
    if win_money: # if player guessed correctly, runs Big_Reward function
        Big_Reward(current_player)
    print(f"Final Bank totals: {player_bank}") # outputs final bank amounts
    print("Thanks for playing, goodbye!") # ends the game
###########################

########################### function to add big reward to player's bank, takes playerID who played Final_Round
def Big_Reward(int1):
    grand_prize=2500 # walue of grand prize
    print(f"For correctly guessing the final word, you've won ${grand_prize}") # tells player what they've won
    player_bank[player_dictionary[int1]]+=grand_prize # adds grand prize to player's bank
###########################

########################### function to find out who which player has most money, returns first player with most money
def Money_Leader():
    max_money=1 # starting value to compare player's bank values against
    most_money=-1 # default playerID in case nobody has any money
    for player_id in player_dictionary.keys(): # loop to check players bank value against current leader
        if player_bank[player_dictionary[player_id]]>max_money: # player's bank value is above current max_money
            most_money=player_id # reset player_id to current player's as they are now leader
            max_money=player_bank[player_dictionary[player_id]] # reset max_money value
        elif player_bank[player_dictionary[player_id]]==max_money: # if player has the same value as previous money leader
            print(f"{player_dictionary[player_id]} is tied for the money lead, sadly they don't get to go on.") # apology message
    return most_money  # return playerID of player with most money
###########################       

########################### function to display the options a player has on their turn, returns the option chosen
def Turn_Menu():
    print("Turn Menu")
    print("====================")
    print("1: Spin the Wheel")
    print("2: Guess the word")
    print("3: Buy a vowel")
    choice_made=False
    while not choice_made: # loop to make sure the player entered a valid menu option
        turn_choice=input("What would you like to do?\n")
        if turn_choice in {'1','2','3'}:
            turn_choice=int(turn_choice)
            choice_made=True
        else:
            print("That is not a recognized option, please try again")
    return turn_choice # returns menu choice
###########################



Welcome()
