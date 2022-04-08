'''
Blackjack:
Classic Card game (without splitting or insurance)
'''

import random
import sys

# Constants UNICODE

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'


def main():
    print(''' Blackjack

    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points
        Aces are worth 1 or 11 pointe.
        Cards 2-10 are worth face value.
        (H)it to take another card
        (S)tand to stop taking cards
        (D)ouble down to increase bet and get one more card at beginning
        Dealer stands at 17.''')

    money = 5000
    while True:  # Main game loop
        # Check if player is out of money
        if money <= 0:
            print('You are broke!')
            sys.exit()

        # make bet
        print('Money:', money)
        bet = getBet(money)

        # deal
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # player actions
        print('Bet:', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # Check bust
            if getHandValue(playerHand) > 21:
                break

            # Get player move
            move = getMove(playerHand, money - bet)

            # Handle Action
            if move == 'D':
                additionalBet = getBet(min(bet, (money-bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')
                print('Bet:', bet)

            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}.')
                playerHand.append(newCard)

            if getHandValue(playerHand) > 21:
                # busted
                continue

            if move in ('S', 'D'):
                break

        # Dealer
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # Dealer hits
                print('The Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input('Press Enter to continue...')
                print('\n\n')

        # show final hands:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        if dealerValue > 21:
            print(f'Dealer busts, you win ${bet}')
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print(f'you lost ${bet}!')
            money -= bet
        elif playerValue > dealerValue:
            print(f'You won ${bet}!')
            money += bet
        elif playerValue == dealerValue:
            print(f'Push. {bet} returned to you')

        input('Press Enter to continue...')
        print('\n\n')


def getBet(maxBet):
    '''
    Ask player how much to bet for round
    '''
    while True:
        print(f'How much do you want to bet? (1-{maxBet}, or QUIT)')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue  # if the player didnt enter a number, ask again

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet  # valid bet


def getDeck():  # sourcery skip: for-append-to-extend
    '''
    Return list (rank and suit) tuples for all cards
    '''
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    '''
    Show the player and dealers cards. Hide dealers first card if showDealerHand is False.
    '''
    print()
    if showDealerHand:
        print('DEALER: ', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # Hide first card:
        displayCards([BACKSIDE] + dealerHand[1:])

    # Show player cards
    print('PLAYER: ', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    '''
    Returns values of cards
    '''
    value = 0
    numberOfAces = 0

    # adds non-aces
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # Add Aces
    value += numberOfAces  # add 1 per ace
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value


def displayCards(cards):
    # sourcery skip: remove-unused-enumerate, use-fstring-for-formatting
    '''
    Display cards in cards list
    '''
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___ '
        if card == BACKSIDE:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for row in rows:
        print(row)


def getMove(playerHand, money):
    '''
    Asks player for mofe - H, S, D
    '''
    while True:
        moves = ['(H)it', '(S)tand']
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble Down')

        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble Down' in moves:
            return move


if __name__ == '__main__':
    main()
