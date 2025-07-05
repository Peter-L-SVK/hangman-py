import random
import os
import json
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds=2):
    """Pause the game for a specified number of seconds."""
    time.sleep(seconds)

def load_words(filename='words.json'):
    """Load words from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        pause()
        return {"words": ["default", "words", "if", "file", "missing"]}
    except json.JSONDecodeError:
        print(f"Error: The file {filename} contains invalid JSON.")
        pause()
        return {"words": ["default", "words", "if", "json", "invalid"]}

def get_random_word(word_data, category=None):
    """Return a random word from the loaded data."""
    if category and category in word_data.get('categories', {}):
        return random.choice(word_data['categories'][category])
    return random.choice(word_data['words'])

def display_hangman(tries):
    """Display the hangman ASCII art based on remaining tries."""
    stages = [  # Final state: head, torso, both arms, both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # Head, torso, both arms, one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # Head, torso, both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # Head, torso, one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # Head, torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # Head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # Initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]

def choose_category(word_data):
    """Let the player choose a category if available."""
    if 'categories' not in word_data or not word_data['categories']:
        return None
    
    print("Available categories:")
    categories = list(word_data['categories'].keys())
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    while True:
        choice = input("\nChoose a category (number) or press Enter for random: ")
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice)-1]
        print("Invalid choice. Please try again.")
        pause(1.5)
        clear_screen()
        print("Available categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

def play_hangman():
    """Main game loop for Hangman with enhanced feedback and pauses."""
    clear_screen()
    print("Welcome to Hangman!")
    print("Try to guess the word before the man is hanged.\n")
    pause(1.5)
    
    word_data = load_words()
    category = choose_category(word_data)
    word = get_random_word(word_data, category).lower()
    
    word_completion = ['_'] * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    
    clear_screen()
    print(display_hangman(tries))
    print(' '.join(word_completion))
    if category:
        print(f"\nCategory: {category}")
    print("\n")
    pause(1)
    
    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").lower()
        
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print(f"\nYou already guessed the letter {guess}!")
                pause()
            else:
                guessed_letters.append(guess)
                count = word.count(guess)
                
                if count == 0:
                    print(f"\nSorry, '{guess}' is not in the word.")
                    tries -= 1
                elif count == 1:
                    print(f"\nGood! '{guess}' appears once in the word.")
                else:
                    print(f"\nGreat! '{guess}' appears {count} times in the word.")
                pause(1.5)
                
                # Update word completion
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = word_as_list
                
                if '_' not in word_completion:
                    guessed = True
                    
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print(f"\nYou already guessed the word {guess}!")
                pause()
            elif guess != word:
                print(f"\n'{guess}' is not the word.")
                tries -= 1
                guessed_words.append(guess)
                pause(1.5)
            else:
                guessed = True
                word_completion = word
        else:
            print("\nNot a valid guess.")
            pause(1.5)
            
        clear_screen()
        print(display_hangman(tries))
        print(' '.join(word_completion))
        print("\nGuessed letters: " + ', '.join(guessed_letters))
        print(f"Guesses remaining: {tries}\n")
    
    clear_screen()
    if guessed:
        print(display_hangman(tries))
        print(' '.join(word_completion))
        print("\nCongratulations, you guessed the word! You win!")
    else:
        print(display_hangman(tries))
        print(f"\nSorry, you ran out of tries. The word was '{word}'. Game over!")
    pause(3)
