from __future__ import print_function
import random
import math


# to execute sims, call this function
# play(numRounds, numDecks=6, hitSoft17=False, printSim=False):


# card counting values (current: Hi-Lo)
countValues = {'A': -1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, 'T': -1, 'J': -1, 'Q': -1,
               'K': -1, }

# bet spread {trueCount : betMultiplier}
betSpread = {1:1, 2:2, 3:4, 4:8}


# redefine print (for toggling printing)
def print(*args, **kwargs):
    if enable_print:
        return __builtins__["print"](*args, **kwargs)


# define Shoe class
class Shoe:
    def __init__(self, numDecks):
        self.shuffle(numDecks)

    def shuffle(self, numDecks):
        self.stack = []
        for deck in range(numDecks):
            for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
                for suit in ['s', 'c', 'd', 'h']:
                    self.stack.append(value + suit + str(deck + 1))
        random.shuffle(self.stack)

    def print(self):
        print('Shoe:')
        for i in range(len(self.stack) // 52):
            print(self.stack[i * 52: (i + 1) * 52])

    def deal(self):
        return self.stack.pop(0)

    def remaining(self):
        return len(self.stack)


# values of cards in blackjack
values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

# define Hand class
class Hand:
    def __init__(self, name, cardA, cardB):
        self.name = name
        self.cards = [cardA[0], cardB[0]]
        self.total = values[cardA[0]] + values[cardB[0]]
        self.soft = cardA[0] == 'A' or cardB[0] == 'A'
        self.split = cardA[0] == cardB[0]
        self.bust = False
        self.upcard = cardA[0]
        self.blackjack = self.total == 21
        if cardA[0] == 'A' and cardB[0] == 'A':
            self.total = 12
        self.double = False

    def hit(self, card):
        self.cards.append(card[0])
        self.total += values[card[0]]
        if self.total > 21:
            if self.soft or card[0] == 'A':
                self.total -= 10
                self.soft = False
            else:
                self.bust = True

    def double(self):
        self.double = True

    def doubled(self):
        return self.double

    def print(self):
        if self.soft:
            print(self.name, self.cards, self.total - 10, 'or', self.total)
        else:
            print(self.name, self.cards, self.total)

    def split(self):
        return self.split

    def cards(self):
        return self.cards

    def numCards(self):
        return len(self.cards)

    def total(self):
        return self.total

    def soft(self):
        return self.soft

    def blackjack(self):
        return self.blackjack

    def bust(self):
        return self.bust

    def upcard(self):
        return self.upcard


basicStrategy = [
    # 2    3    4    5    6    7    8    9    T    A
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 2, 3, 4, 5, 6, 7, 8   [0]
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # 9                     [1]
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # 10                    [2]
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],  # 11                    [3]
    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 12                    [4]
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 13                    [5]
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 14                    [6]
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 15                    [7]
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 16                    [8]
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 17, 18, 19, 20, 21    [9]
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A2                    [10]
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A3                    [11]
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A4                    [12]
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A5                    [13]
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A6                    [14]
    ['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],  # A7                    [15]
    ['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S'],  # A8                    [16]
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A9                    [17]
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 22                    [18]
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 33                    [19]
    ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],  # 44                    [20]
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # 55                    [21]
    ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],  # 66                    [22]
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # 77                    [23]
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # 88                    [24]
    ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],  # 99                    [25]
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # TT                    [26]
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']]  # AA                    [27]

upcardIndexDict = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 8, 'Q': 8, 'K': 8,
                   'A': 9}
basicStrategySplit = {'A': 27, '2': 18, '3': 19, '4': 20, '5': 21, '6': 22, '7': 23, '8': 24, '9': 25, 'T': 26, 'J': 26,
                      'Q': 26, 'K': 26}
basicStrategyHard = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 9,
                     19: 9, 20: 9, 21: 9}
basicStrategySoft = {13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 17, 21: 9}


def play(numRounds, numDecks=6, hitSoft17=False, printSim=False):
    global enable_print
    enable_print = printSim
    shoe = Shoe(numDecks)
    roundsPlayed = 0
    netWinnings = 0
    shoe.print()
    count = 0
    baseBet = 5


    while roundsPlayed < numRounds:

        # update trueCount
        trueCount = count / (Shoe.remaining(shoe) / 52)

        # print rounds played, netWinnings, and count
        print('\nRounds played:', roundsPlayed)
        if netWinnings < 0:
            print('Net winnings: -$' + str(round(abs(netWinnings), 2)))
        else:
            print('Net winnings: $' + str(round(netWinnings, 2)))
        print('count:', count)
        print('cards in shoe:', Shoe.remaining(shoe), ', decks in shoe:', Shoe.remaining(shoe) / 52, ', true count:',
              count / (Shoe.remaining(shoe) / 52))
        print('True count:', trueCount)
        print('\n')

        # shuffle the shoe when fewer than 2 decks remain
        if shoe.remaining() < 104:
            shoe.shuffle(numDecks)
            print('Re-shuffling.')
            shoe.print()
            # reset count
            count = 0

        # determine betAmount
        try:
            betAmount = baseBet * betSpread[math.floor(trueCount)]
        except KeyError:
            if trueCount > 1:
                betAmount = baseBet * betSpread[max(betSpread)]
            else:
                betAmount = baseBet


        print('Bet amount: $' + str(betAmount))
        blackjackBonus = 6 / 5
        roundsPlayed += 1
        # deal player's hand and append it to handsQueue
        handsQueue = [Hand("Player's hand:", shoe.deal(), shoe.deal())]
        # update count with player's hand
        count += countValues[Hand.cards(handsQueue[0])[0]]
        count += countValues[Hand.cards(handsQueue[0])[1]]
        # reset completeHands, unresolvedHands, and splitCount
        completeHands = []
        unresolvedHands = False
        splitCount = 0
        # deal dealer's hand
        dealer = Hand("Dealer's hand", shoe.deal(), shoe.deal())
        # update count with dealer's upcard
        count += countValues[Hand.upcard(dealer)]
        print("Dealer's upcard: ['" + str(Hand.upcard(dealer)) + "']")

        # check for dealer blackjack
        if Hand.blackjack(dealer) and not Hand.blackjack(handsQueue[0]):
            # subtract loss from netWinnings
            netWinnings -= betAmount
            Hand.print(handsQueue[0])
            Hand.print(dealer)
            # update count with dealer's downcard
            count += countValues[Hand.cards(dealer)[1]]
            print('Dealer has blackjack. Lost $' + str(betAmount) + '.')
            continue

        while handsQueue:
            currentHand = handsQueue.pop(0)
            # check for splitting
            if Hand.split(currentHand):
                if basicStrategy[basicStrategySplit[Hand.cards(currentHand)[0]]][
                    upcardIndexDict[Hand.upcard(dealer)]] == 'P':
                    # add first split hand to handsQueue, update count
                    handsQueue.append(Hand("Player's hand " + str(splitCount + 1), currentHand.cards[0], shoe.deal()))
                    count += countValues[Hand.cards(handsQueue[0])[1]]
                    # add second split hand to handsQueue, update count
                    handsQueue.append(Hand("Player's hand " + str(splitCount + 2), currentHand.cards[1], shoe.deal()))
                    count += countValues[Hand.cards(handsQueue[1])[1]]
                    # track number of splits (for hand-naming purposes)
                    splitCount += 1
                    Hand.print(currentHand)
                    print('Splitting ' + str(Hand.cards(currentHand)[0]) + "'s.")
                    continue
            # check for blackjack
            if Hand.blackjack(currentHand):
                netWinnings += betAmount * blackjackBonus
                completeHands.append(currentHand)
                Hand.print(currentHand)
                print('Blackjack!')
                continue
            # play the hand
            while True:
                Hand.print(currentHand)
                # check if busted
                if Hand.bust(currentHand):
                    netWinnings -= (betAmount + currentHand.doubled() * betAmount)
                    completeHands.append(currentHand)
                    print('Bust. Hand loses $' + str(betAmount + currentHand.doubled() * betAmount) + '.')
                    break
                # determine ideal play
                if Hand.soft(currentHand):
                    play = basicStrategy[basicStrategySoft[Hand.total(currentHand)]][
                        upcardIndexDict[Hand.upcard(dealer)]]
                else:
                    play = basicStrategy[basicStrategyHard[Hand.total(currentHand)]][
                        upcardIndexDict[Hand.upcard(dealer)]]
                # execute ideal play
                if play == 'S':
                    completeHands.append(currentHand)
                    unresolvedHands = True
                    print('Stand.')
                    break
                if play == 'D':
                    # if hand contains only 2 cards, double down
                    if currentHand.numCards() == 2:
                        # hit the hand
                        currentHand.hit(shoe.deal())
                        # update count
                        count += countValues[Hand.cards(currentHand)[-1]]
                        # mark hand as doubled (for calculating win/loss amount later)
                        Hand.double(currentHand)
                        # append hand to completeHands
                        completeHands.append(currentHand)
                        print('Double down.')
                        if not currentHand.bust:
                            Hand.print(currentHand)
                            # flag unresolvedHands True so the dealer's hand is played out later
                            unresolvedHands = True
                        # after doubling down, this hand is finished
                        break
                    # if doubling down is not an option (because the hand has already been hit)
                    else:
                        # hit the hand
                        currentHand.hit(shoe.deal())
                        # update count
                        count += countValues[Hand.cards(currentHand)[-1]]
                        print('Hit.')
                        continue
                if play == 'H':
                    # hit the hand
                    currentHand.hit(shoe.deal())
                    # update count
                    count += countValues[Hand.cards(currentHand)[-1]]
                    print('Hit.')
                    continue

        Hand.print(dealer)
        # update count with dealer's downcard
        count += countValues[Hand.cards(dealer)[1]]
        if unresolvedHands:
            # play dealer's hand
            while dealer.total < 17 or (hitSoft17 and dealer.soft() and dealer.total == 17):
                # dealer hits
                dealer.hit(shoe.deal())
                # update count
                count += countValues[Hand.cards(dealer)[-1]]
                print('Dealer hits.')
                Hand.print(dealer)
            if dealer.total > 21:
                print('Dealer busts.')
                dealer.total = 0
            else:
                print('Dealer stands on', Hand.total(dealer))

        for hand in completeHands:
            if Hand.blackjack(hand):
                print(hand.name, hand.cards, 'wins $' + str(betAmount + betAmount * Hand.doubled(hand)) + '.')
            elif not Hand.bust(hand):
                if Hand.total(hand) > Hand.total(dealer):
                    netWinnings += betAmount + betAmount * Hand.doubled(hand)
                    print(hand.name, hand.cards, 'wins $' + str(betAmount + betAmount * Hand.doubled(hand)) + '.')
                elif Hand.total(hand) < Hand.total(dealer):
                    netWinnings -= betAmount + betAmount * Hand.doubled(hand)
                    print(hand.name, hand.cards, 'loses $' + str(betAmount + betAmount * Hand.doubled(hand)) + '.')
                elif Hand.total(hand) < Hand.total(dealer):
                    print(hand.name, hand.cards, 'loses $' + str(betAmount + betAmount * Hand.doubled(hand)) + '.')
                else:
                    print(hand.name, hand.cards, 'pushes.')

    print('\nRounds played:', roundsPlayed)
    if netWinnings < 0:
        print('Net winnings: -$' + str(round(abs(netWinnings), 2)) + '\n')
    else:
        print('Net winnings: $' + str(round(netWinnings, 2)) + '\n')


    enable_print = True
    print('Net winnings per hand:', netWinnings/numRounds)
    return round(netWinnings, 2)