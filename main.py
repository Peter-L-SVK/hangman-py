#!/usr/bin/env python3

import lib

if __name__ == "__main__":
    while True:
        lib.play_hangman()
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing! Goodbye!")
            lib.pause(1.5)
            break
        lib.clear_screen()
        continue
