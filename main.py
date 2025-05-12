from cards import *
import time, math

ROYAL_FLUSH = 100
STRAIGHT_FLUSH = 90
FOUR_OF_KIND = 80
FULL_HOUSE = 70
FLUSH = 60
STRAIGHT = 50
THREE_OF_KIND = 40
TWO_PAIR = 30
PAIR = 20
HIGH_CARD = 10

PRE_FLOP = math.perm(50,5)
PRE_TURN = math.perm(47,3)
PRE_RIVER = math.perm(46,3)


def whoWins(currentGame:Game):
    myCards = currentGame.myHand + currentGame.river
    opponentCards = currentGame.opponentsHand + currentGame.river
   
def getBestHand(currentGame):
    hand = currentGame.myHand
    river = currentGame.river

    combos = [
        hand + [river[0], river[1], river[2]],
        hand + [river[0], river[1], river[3]],
        hand + [river[0], river[1], river[4]],
        hand + [river[0], river[2], river[3]],
        hand + [river[0], river[2], river[4]],
        hand + [river[0], river[3], river[4]],
        hand + [river[1], river[2], river[3]],
        hand + [river[1], river[2], river[4]],
        hand + [river[1], river[3], river[4]],
        hand + [river[2], river[3], river[4]],
    ]

    bestRank = -1
    for combo in combos:
        rank = rankHand(combo)
        if rank > bestRank:
            bestRank = rank

    return bestRank


    

def rankHand(hand):
    hand = sortHand(hand)

    if( isRoyalFlush(hand)):
         return ROYAL_FLUSH
    elif(isStraightFlush(hand)):
         return STRAIGHT_FLUSH
    elif(len(containsQuad(hand))!=0):
         return FOUR_OF_KIND
    elif( isFullHouse(hand)):
         return FULL_HOUSE
    elif(isFlush(hand)):
         return FLUSH
    elif(isStraight(hand)):
         return STRAIGHT
    elif(len(containsTriple(hand))!=0):
         return THREE_OF_KIND
    elif(containsTwoPair(hand)):
         return TWO_PAIR
    elif(len(containsPair(hand))!=0):
         return PAIR
    else:
         return getHighCard(hand).value

    

def sortHand(hand):
    for i in range(1, len(hand)):
        key = hand[i].value
        j = i - 1
        while j >= 0 and hand[j].value > key:
            hand[j + 1].value = hand[j].value
            j -= 1
        hand[j + 1].value = key
    return hand
    


def getHighCard(hand):
    return hand[len(hand)-1]



def rollout(currentGame,deck):
    river = currentGame.river
    if len(river) ==0:
        for i in range(5):
            river.append(deck.deal())
        
    elif len(river) ==3:
            river.append(deck.deal())
            river.append(deck.deal())
    elif len(river) ==4:
            river.append(deck.deal())
    elif len(river) ==5:
        pass

    newGame = Game(currentGame.myHand,river,currentGame.opponentsHand)
    newGameOpp = Game(currentGame.opponentsHand,river,currentGame.myHand)
    myBest = getBestHand(newGame)
    hisBest = getBestHand(newGameOpp)
    if myBest> hisBest:
         return 1
    else:
         return 0

def findAllPossibilties(currentGame,deck,parent):
    c = deck.cards + currentGame.opponentsHand
    cards = len(c)
    grab = 0
    permutations = 0
    river = currentGame.river
    if len(river) ==0:
        grab = 5
        permutations = PRE_FLOP
        
    elif len(river) ==3:
           grab = 3
           permutations = PRE_TURN
    elif len(river) ==4:
            permutations = PRE_RIVER
            grab = 3
    elif len(river) ==5:
         pass
    
    startTime = time.time()
    timeLimit = 10
    combos = []
    print("grab",grab)
    print(len(c))
    i=0
    while time.time() - startTime < timeLimit and permutations>i:
         i+=1
         l = []
         for i in range(grab):
             num = random.randint(0,cards-1)
             while l.__contains__(num):
                  num = random.randint(0,cards-1)
             l.append(num)
             
         if grab == 5:
            newGame = Game(currentGame.myHand,[c[l[2]],c[l[3]],c[l[4]]],[c[l[0]],c[l[1]]])
         elif grab == 3:
            newGame = Game(currentGame.myHand,currentGame.river +[c[l[2]]],[c[l[0]],c[l[1]]])
         newDeck = Deck()
         currentList = newGame.opponentsHand+newGame.myHand + newGame.river
         newDeck.remove_cards(currentList)
         #print(l)
         val = rollout(newGame,newDeck)
         #print(val)
         parent.children.append(Node(1,val,parent,[],newGame))
         parent.total +=val
         parent.visited+=1
         combos.append(l)
    while time.time() - startTime < timeLimit:
        n = UCB1(parent)
        d2 = Deck()
        d2.remove_cards(n.game.myHand + n.game.river)
        findSinglePossibilty(n.game,d2,n)
        
    
    return combos

def findSinglePossibilty(currentGame,deck,parent):
    c = deck.cards + currentGame.opponentsHand
    cards = len(c)
    grab = 0
    permutations = 0
    river = currentGame.river
    if len(river) ==0:
        grab = 5
        permutations = PRE_FLOP
        
    elif len(river) ==3:
           grab = 3
           permutations = PRE_TURN
    elif len(river) ==4:
            permutations = PRE_RIVER
            grab = 3
    elif len(river) ==5:
         pass
    
    
    l = []
    for i in range(grab):
        num = random.randint(0,cards-1)
        while l.__contains__(num):
            num = random.randint(0,cards-1)
        l.append(num)
             
        if grab == 5:
            newGame = Game(currentGame.myHand,[c[l[2]],c[l[3]],c[l[4]]],[c[l[0]],c[l[1]]])
        elif grab == 3:
            newGame = Game(currentGame.myHand,currentGame.river +[c[l[2]]],[c[l[0]],c[l[1]]])
        newDeck = Deck()
        currentList = newGame.opponentsHand+newGame.myHand + newGame.river
        newDeck.remove_cards(currentList)
        print(l)
        val = rollout(newGame,newDeck)
        print(val)
        parent.children.append(Node(1,val,parent,[],newGame))
        parent.total +=val
        parent.visited+=1
        while(parent.parent is not None):
            parent.total +=val
            parent.visited+=1

    return None
     
def UCB1(parent):
    maxNode = None
    max = 0
    for node in parent.children:
         if node.total/node.visited + math.sqrt(2 * math.log(node.total)/node.visited) > max:
              max = node.total/node.visited + math.sqrt(2 * math.log(node.total)/node.visited)
              maxNode = node
    return maxNode
    
        
print(rankHand([ Card('Heart',14), Card('Heart',10), Card('Heart',13), Card('Heart',12), Card('Heart',11)]))
cards = sortHand([Card('Heart',5), Card('Heart',2), Card('Heart',8), Card('Heart',10), Card('Heart',9), Card('Heart',12), Card('Heart',7)])

d = Deck()
d.shuffle()
a = [d.deal(),d.deal()]
b=[d.deal(),d.deal()]
#print(rollout(Game(a,[],b),d))
#findAllPossibilties(Game(a,[],b),d)

for card in cards:
    print(card.value)




deck = Deck()
deck.shuffle()

myCards = []
river = []
#print win percventage at each stage
game = Game([],[],[])
##pre-flop##
game.myHand.append(deck.deal())
game.myHand.append(deck.deal())

game.opponentsHand.append(deck.deal())
game.opponentsHand.append(deck.deal())

head = Node(1,0,None,[],game)
findAllPossibilties(game,deck,head)
print("Pre-Flop win percentage: ",head.total/head.visited)
##flop##

game.river.append(deck.deal())
game.river.append(deck.deal())
game.river.append(deck.deal())

head = Node(1,0,None,[],game)
findAllPossibilties(game,deck,head)
print("Flop win percentage: ",head.total/head.visited)
###turn###
river.append(deck.deal())
head = Node(1,0,None,[],game)
findAllPossibilties(game,deck,head)
print("Turn win percentage: ",head.total/head.visited)

###river###
river.append(deck.deal())
