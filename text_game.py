import Crypto.Random.random as random
from typing import Union, List
import logging

suits = ['H', 'C', 'S', 'D']
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
logging.getLogger('main')


class EndGameException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Card:
    def __init__(self, suit: str, number: str):
        self.id = {'suit': suit, 'number': number}
        try:
            if ord(number) > 59:
                self.count = -1
            elif int(number) <= 6:
                self.count = 1
            else:
                self.count = 0
        except TypeError:
            self.count = -1
        if len(str(number)) == 2 or ord(number) > 65:
            self.value = 10
        else:
            try:
                self.value = int(number)
            except ValueError:
                self.value = 'A'

    def __str__(self) -> str:
        return self.id['number'] + self.id['suit']


class Decks:
    def __init__(self, num_decks: int = 1, shuffle: bool = True):
        cards = []
        for suit in suits:
            for number in numbers:
                cards.append(Card(suit, number))
        self.cards = cards * num_decks
        if shuffle:
            self.shuffle()

    def __str__(self) -> str:
        return f'Deck({map(str, self.cards)})'

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def pop(self) -> Card:
        return self.cards.pop()


class InfiniteDeck:
    def __init__(self):
        self.cards = Decks(1, False).cards.copy()

    def pop(self) -> Card:
        return random.choice(self.cards)


class Player:
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        self.cards = kwargs['keys'] if 'pixel_cards' in keys else []
        self.money = kwargs['money'] if 'money' in keys else -1


class BasicStrategyGame:
    def __init__(self):
        self.deck = InfiniteDeck()
        self.hands = 0
        self.correct = 0

    def hand(self) -> bool:
        while True:
            dealer = self.deck.pop()
            player = [self.deck.pop(), self.deck.pop()]
            correct = get_strategy(dealer, player)
            if correct == 'blackjack':
                continue
            break
        print(f'Dealer has {dealer}')
        print(f'You have {player[0]} and {player[1]}')
        guess = input('What is the correct play?\n').lower()
        if guess == 'end' or guess == 'stop':
            raise EndGameException('End the game')
        if correct[:2] == guess[:2]:
            print('Correct!')
            return True
        print(f'Incorrect. The correct answer is {correct}.')
        return False

    def play(self) -> None:
        try:
            while True:
                self.hands += 1
                self.correct += self.hand()
                print(f'Hands: {self.hands}  '
                      f'Correct: {self.correct}  '
                      f'Accuracy: {round(self.correct / self.hands * 100, 0)}%')
        except EndGameException:
            print('Game has ended. Final score:')
            print(f'Hands: {self.hands}  '
                  f'Correct: {self.correct}  '
                  f'Accuracy: {round(self.correct / self.hands * 100, 0)}%')


def get_strategy(dealer: Card, player: List[Card]) -> Union[str, None]:
    player_val = list(map(lambda x: x.value, player))
    dealer_val = dealer.value if dealer.value != 'A' else 11
    # print(dealer_val)
    # for card in player:
    #     print(card, end=' ')
    # print(player_val)
    if 'A' not in player_val:
        if sum(player_val) > 21:
            return 'lose'
        if sum(player_val) == 21:
            # print(f'got blackjack with {player_val}')
            return 'blackjack'
        soft = False
        total = sum(player_val)
    else:
        # print('Player has an Ace')
        player_val_copy = player_val.copy()
        player_val_copy[player_val_copy.index('A')] = 11
        while 'A' in player_val_copy:
            player_val_copy[player_val_copy.index('A')] = 1
        if sum(player_val_copy) >= 21:
            if sum(player_val_copy) == 21:
                # print(f'got blackjack with {player_val}')
                return 'blackjack'
            player_val_copy[player_val_copy.index('A')] = 1
            if sum(player_val_copy) >= 21:
                if sum(player_val_copy) == 21:
                    # print(f'got blackjack with {player_val}')
                    return 'blackjack'
                return 'lose'
            soft = False
        else:
            soft = True
        total = sum(player_val_copy)
    if 'A' not in player_val and len(player_val) == 2:  # Surrender conditions
        total = sum(player_val)
        if total == 16 and dealer_val >= 9:
            return 'surrender'
        if total == 15 and dealer_val == 10:
            return 'surrender'
    if len(player_val) == 2 and player_val[0] == player_val[1]:  # If is a double
        # print('This is a double')
        if 'A' in player_val or 8 in player_val:
            return 'split'
        if 9 in player_val:
            if 2 <= dealer_val <= 9 and dealer_val != 7:
                return 'split'
            return 'stand'
        if 7 in player_val or 6 in player_val:
            if 2 <= dealer_val <= player_val[0]:
                return 'split'
            return 'stand'
        if 5 in player_val:
            if 2 <= dealer_val <= 9:
                return 'double'
            return 'hit'
        if 4 in player_val:
            if 5 <= dealer_val <= 6:
                return 'split'
            return 'hit'
        if 3 in player_val or 2 in player_val:
            if 2 <= dealer_val <= 7:
                return 'split'
            return 'hit'
    if soft:  # Soft totals
        # print('This is a soft total')
        if total == 20:
            return 'stand'
        if total == 19:
            if dealer_val == 6:
                return 'double'
            return 'stand'
        if total == 18:
            if 2 <= dealer_val <= 6:
                return 'double'
            if dealer_val >= 9:
                return 'hit'
            return 'stand'
        if total == 17:
            if 3 <= dealer_val <= 6:
                return 'double'
        elif total == 16 or total == 15:
            if 4 <= dealer_val <= 6:
                return 'double'
        elif total == 14 or total == 13:
            if 5 <= dealer_val <= 6:
                return 'double'
        return 'hit'
    # Hard totals
    # print('This is a hard total')
    if total >= 17:
        # print(f'{total} is greater than or equal to 17')
        return 'stand'
    if total >= 13:
        # print(f'{total} is greater than or equal to 13')
        if 2 <= dealer_val <= 6:
            # print(f'Dealer has {dealer_val}, which is between 2 and 6')
            return 'stand'
        # print(f'Dealer has {dealer_val}')
        return 'hit'
    if total == 12:
        # print('Total is 12')
        if 4 <= dealer_val <= 6:
            # print(f'Dealer has {dealer_val}, which is between 4 and 6')
            return 'stand'
        # print(f'Dealer has {dealer_val}')
        return 'hit'
    if total == 11:
        # print('Total is 11')
        return 'double'
    if total == 10:
        # print('Total is 10')
        if 2 <= dealer_val <= 9:
            # print(f'Dealer has {dealer_val}, which is between 2 and 9')
            return 'double'
        # print(f'Dealer has {dealer_val}')
        return 'hit'
    if total == 9:
        # print('Total is 9')
        if 3 <= dealer_val <= 6:
            # print(f'Dealer has {dealer_val}, which is between 3 and 6')
            return 'double'
        # print(f'Dealer has {dealer_val}')
        return 'hit'
    # print(f'Total is {total}, which is less than 9')
    return 'hit'


if __name__ == '__main__':
    BasicStrategyGame().play()
