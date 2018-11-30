# Problem Set 2, hangman.py
# Name: Tymoshenko Daria KM-82
# Collaborators:Glib Yudin, KM-82
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set(secret_word).issubset(letters_guessed)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ""
    for letter in secret_word:
        if letters_guessed.count(letter) > 0:
            word += letter
        else:
            word += "_ "
    return word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = list(set(string.ascii_lowercase) - set(letters_guessed))
    available_letters.sort()
    return "".join(available_letters)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings_count = 3
    guesses_count = 6
    letters_guessed = []
    print('''Welcome to the game Hangman!
I am thinking of a word that is {0} letters long.
You have 3 warnings left.'''.format(len(secret_word)))
    while (guesses_count > 0) and ( not is_word_guessed(secret_word, letters_guessed)):
        print('''--------------------
You have {0} guesses left.'''.format(guesses_count))
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter:").lower()
        if (not letter.isalpha()) or (letter in letters_guessed):
            if warnings_count > 0:
                warnings_count -= 1
                print("You can't use this letter.You have {0} warnings left. {1}".format(warnings_count, get_guessed_word(secret_word, letters_guessed) ))
            elif warnings_count == 0:
                guesses_count -= 1
                print("You lose guess.")
            else:
                continue
            if guesses_count <= 0:
                print("You lose.",secret_word)
            else:
                continue
        letters_guessed.append(letter)
        if letter in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                score = guesses_count * len(set(secret_word))
                print('''Congratulations, you won!
Your total score is {0}!'''.format(score))              
        else:
            if letter in ["a", "e", "i", "o", "u"]:
                guesses_count -= 2
            else:
                guesses_count -= 1
            print("Oops! That letter is not in my word. You lose guess.",get_guessed_word(secret_word, letters_guessed))
            if guesses_count <= 0:
                print("You lose.",secret_word)
            else:
                continue


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace("_ ", "_")
    if len(my_word) != len(other_word):
        return False
    else:
        for i in range(len(my_word)):
            if my_word[i] != "_" and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == "_" and other_word[i] in my_word:
                return False
        return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    my_word = my_word.replace("_ ", "_")
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    if len(possible_matches) == 0:
        return "No matches found"
    else:
        return " ".join(possible_matches)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings_count = 3
    guesses_count = 6
    letters_guessed = []
    print('''Welcome to the game Hangman!
I am thinking of a word that is {0} letters long.
You have 3 warnings left.'''.format(len(secret_word)))
    while (guesses_count > 0) and ( not is_word_guessed(secret_word, letters_guessed)):
        print('''--------------------
You have {0} guesses left.'''.format(guesses_count))
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter:").lower()
        if (not letter.isalpha() and letter != "*") or (letter in letters_guessed and letter != "*"):
            if warnings_count > 0:
                warnings_count -= 1
                print("You can't use this letter.You have {0} warnings left.".format(warnings_count))
            if warnings_count == 0:
                guesses_count -= 1
                print("You lose guess.")
            else:
                continue
            if guesses_count <= 0:
                print("You lose.",secret_word)
            else:
                continue
        letters_guessed.append(letter)
        if letter in secret_word:
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                score = guesses_count * len(set(secret_word))
                print('''--------------------
Congratulations, you won!
Your total score is {0}!'''.format(score))
        elif letter == "*":
            print("Possible word matches are:", show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        else:
            if letter in ["a", "e", "i", "o", "u"]:
                guesses_count -= 2
            else:
                guesses_count -= 1
            print("Oops! That letter is not in my word. You lose guess")
            if guesses_count <= 0:
                print("You lose.",secret_word)
            else:
                continue


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    secret_word = random.choice(wordlist)
    #hangman(secret_word)
    hangman_with_hints(secret_word)
    

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.


