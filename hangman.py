import random
print("H A N G M A N\n")
play = input('Type "play" to play the game, "exit" to quit:\n')
words = ['python', 'java', 'kotlin', 'javascript']
already_typed = []
word = random.choice(words)
n = len(word)
board = ['-' for i in range(n)]


def play_game():
    if play == "play":
        lives = 8
        while lives > 0:
            print()
            print(''.join(board))
            guess = input("Input a letter:")
            if guess in word and guess not in already_typed:
                indexes = [index for index, letter in enumerate(word) if letter == guess]
                for num in indexes:
                    board[num] = guess
                    already_typed.append(guess)
                if board == word:
                    print("You guessed the word!\nYou survived!")
                    ask_again = True
                    break
            elif guess not in word and guess not in already_typed and guess.isalpha() and guess.islower() and len(guess) == 1:
                lives -= 1
                if lives == 0:
                    print("No such letter in the word\nYou are hanged!")
                elif lives >= 1:
                    print("No such letter in the word")
                    already_typed.append(guess)
            elif guess in already_typed:
                print("You already typed this letter")
                lives += 0
            elif len(guess) != 1:
                print("You should input a single letter")
                lives += 0
            elif guess.isalpha() is False or guess.islower() is False:
                print("It is not an ASCII lowercase letter")
                lives += 0
    elif play == "exit":
        exit()


play_game()