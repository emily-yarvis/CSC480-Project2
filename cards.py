import random

class Node:
    def __init__(self,visited,total,parent,children,game):
        self.visited = visited
        self.total = total
        self.game = game
        self.parent = parent
        self.children = children


class Card:
    def __init__(self, suit, value):
        self.suit = suit  
        self.value = value  

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
    
    def remove_cards(self, cards_to_remove):
        self.cards = [card for card in self.cards if card not in cards_to_remove]



class Game:
    def __init__(self, myHand,river,opponentsHand):
        self.myHand = myHand
        self.river = river
        self.opponentsHand = opponentsHand
        

def isFlush(hand):
    suite = hand[0].suit
    for card in hand:
        if card.suit != suite:
            return False
        
    return True

def containsPair(hand):
    pairs = []
    counter = dict()
    for card in hand:
        if card.value not in counter:
            counter[card.value] = 1
        else:
            newNum = counter[card.value]+1
            counter[card.value] = newNum
    hand = list(set(hand))##remove duplicates
    for card in hand:
        if counter[card.value] == 2:
            pairs.append(card.value)
    return pairs

def containsTwoPair(hand):
    if len(containsPair(hand)) == 2:
        return True
    else:
        return False

def containsTriple(hand):
    triples = []
    counter = dict()
    for card in hand:
        if card.value not in counter:
            counter[card.value] = 1
        else:
            newNum = counter[card.value]+1
            counter[card.value] = newNum
    hand = list(set(hand))##remove duplicates
    for card in hand:
        if counter[card.value] == 3:
            triples.append(card.value)
    return triples

def containsQuad(hand):
    quad = []
    counter = dict()
    for card in hand:
        if card.value not in counter:
            counter[card.value] = 1
        else:
            newNum = counter[card.value]+1
            counter[card.value] = newNum
    hand = list(set(hand))##remove duplicates
    for card in hand:
        if counter[card.value] == 4:
            quad.append(card.value)
    return quad

def isStraight(hand):
    first = True
    prev = 0
    for card in hand:
        if first:
            first = False
            prev = card.value
        elif prev+1 != card.value:
            return False
        else:
            prev = prev+1
    return True

def isFullHouse(hand):
    pair = False
    triple = False
    counter = dict()
    for card in hand:
        if card.value not in counter:
            counter[card.value] = 1
        else:
            newNum = counter[card.value]+1
            counter[card.value] = newNum
    hand = list(set(hand))##remove duplicates
    for card in hand:
        if counter[card.value] == 2:
            pair = True
        elif counter[card.value] == 3:
            triple = True
    return pair and triple

def isStraightFlush(hand):
    return isStraight(hand) and isFlush(hand)

def isRoyalFlush(hand):

    vals = set()
    for card in hand:
        vals.add(card.value)
    s = set()
    s.add(10)
    s.add(11)
    s.add(12)
    s.add(13)
    s.add(14)
    if vals != s:
        return False
    
    return isFlush(hand)

    