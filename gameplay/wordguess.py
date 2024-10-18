from collections import Counter
from gameplay.cache import GameNode
import random
from words.words import words
from words.correct import correct_words


WORDS_COUNT = 2315

def choose_word():
    x = random.randint(1, WORDS_COUNT)
    return words[x - 1]
    

def _feedback(correct_word, guess):
    correct_letter_counts = dict(Counter(correct_word))
    feedback_list = [1, 2, 3, 4, 5]
    yellow_letters = []
    for index, letter in enumerate(guess):
        if correct_word[index] == letter:
            feedback_list[index] = "G"
            correct_letter_counts[letter] -= 1
        elif letter not in correct_word:
            feedback_list[index] = "B"
        else:
            yellow_letters.append((index, letter))
    for tup in yellow_letters:
        i, l = tup[0], tup[1]
        if correct_letter_counts[l] > 0:
            feedback_list[i] = "Y"
            correct_letter_counts[l] -= 1
        else:
            feedback_list[i] = "B" 
    return ''.join(feedback_list)


def create_game(games_cache) -> dict:
    new_word = choose_word()
    new_game = GameNode(new_word)
    games_cache.put(new_game)
    payload = new_game.create_payload()
    return payload


def _validate_guess(guess: str) -> bool:
    if guess in correct_words:
        return True
    return False


def play_game_loop(guess: str, game: GameNode):
    guess = guess.lower()
    if _validate_guess(guess) == False:
        return game.create_payload(message="Invalid Word")
    game.guesses.append(guess)
    game.guess_count += 1
    feedback = _feedback(game.correct_word, guess)
    game.feedback.append(feedback)
    if feedback == "GGGGG":
        game.results = True
        game.status = False
    elif game.guess_count == 6:
        game.results = False
        game.status = False
    payload = game.create_payload()
    return payload