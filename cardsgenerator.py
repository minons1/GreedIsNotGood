from enum import Enum
from enum import IntEnum
from random import *

full_deck = []
partial_deck = []
play_deck = []

# Card enum for playing cards
class Card(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 1

# Suit enum for cards
class Suit(Enum):
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'

# Class to hold information about cards
class PlayingCard:
    def __init__(self,card_value,card_suit):
        self.card = card_value
        self.suit = card_suit

# Function to deal full deck of cards
def create_deck():
    for suit in Suit:
        for card in Card:
            full_deck.append(PlayingCard(Card(card),Suit(suit)))
    return full_deck

# Draw a single random card from the deck
def draw_card(deck):
    rand_card = randint(0,len(deck)-1)
    return deck.pop(rand_card)

# Test on 10 Cards
def playgenerator():
    count = 10
    while (count>0 and len(partial_deck) > 0):
        play_deck.append(draw_card(partial_deck))
        count-=1

create_deck()
partial_deck = list(full_deck)
playgenerator()
playdecklength = len(play_deck)
for i in range(playdecklength):
     print(play_deck[i].card,play_deck[i].suit)
