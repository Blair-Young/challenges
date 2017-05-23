# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html
from __future__ import division
from data import DICTIONARY, LETTER_SCORES, POUCH
import random
import itertools
import Queue

NUM_LETTERS = 7
start_game_phrases = ['no', 'nope', 'fuck off']

class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.word_score = None
        self.overall_score = None
    
    def calc_player_score(self, best_value):
        self.overall_score = (self.word_score/best_value)*100

def letter_gen():
    return [letter.lower() for letter in random.sample(POUCH, 7)]

def best(hand):
    total_perms = []
    for word_length in range(7):
        for perm in list(itertools.permutations(hand, word_length)):
            pot_word = ''.join(perm)
            if pot_word in DICTIONARY:
                total_perms.append(pot_word)
    return set(total_perms)  

def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)

def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)

def multiplayer(players):
    finished = []    
    hand = letter_gen()    
    possible =  best(hand)
    best_word =  max_word_value(possible)
    best_score = calc_word_value(best_word)
    
    q = Queue.Queue()
    for i in range(players):
        player_name = raw_input('Name...')
        q.put(Player(player_name))

    print ('Here is the hand: {}').format(hand)
    while not q.empty():
        player_go = q.get()
        print ("Your go, {}").format(player_go.name)
        player_answer = raw_input("Enter your best word: ")
        if player_answer in possible:
            player_go.word_score = calc_word_value(player_answer)
            player_go.calc_player_score(best_score)
        else:
            print 'Illegal word'
            player_go.overall_score = 0
        finished.append(player_go)

    for player in finished:
        print ('{} scored {}').format(player.name, player.overall_score)
    print ('Best word: {} with a score of {}').format(best_word, best_score)
    return

def singleplayer():
    hand = letter_gen()
    possible =  best(hand)
    best_word =  max_word_value(possible)
    best_score = calc_word_value(best_word)
    player_name = raw_input('What is your name? ')
    player_1 = Player(player_name)
    print ('Here is your hand: {}').format(hand)
    player_word = raw_input('Enter your best word: ')
    if player_word in possible:
        player_1.word_score = calc_word_value(player_word)
        player_1.calc_player_score(best_score)
        print player_1.overall_score
        print best_word
        print best_score
    else:
        print 'Illegal word'
    
def main():
    while 1:
        start_game = raw_input('You wanna play some scrabble, scrub?').lower()
        if start_game in start_game_phrases:
            break
        players = int(raw_input('How many players?'))
        if players > 1:
            multiplayer(players)
        elif players == 1:
            singleplayer()
        else:
            print 'loser'
            
if __name__ == "__main__":
    main()
