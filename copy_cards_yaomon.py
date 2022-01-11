"""
Credit for the pixel_cards in assets/pcp goes to https://twitter.com/YaomonKS
"""

suits = {'Clover': 'C', 'Diamond': 'D', 'Heart': 'H', 'Spade': 'S'}
values = {'1': 'A', '2': '2', '3': '3', '4': '4', '5': '5',
          '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
          '11': 'J', '12': 'Q', '13': 'K'}


if __name__ == '__main__':
    old_path = f'assets/pcp/'
    new_path = 'assets/cards_NO_BACK/'
    for suit in suits.keys():
        for value in values.keys():
            with open(f'{old_path}{suit}/card_{value}_{suit.lower()}.png', 'rb') as f:
                card = f.read()
            try:
                value = str(int(value))
            except ValueError:
                pass
            with open(f'{new_path}{values[value]}{suits[suit]}.png', 'wb') as f:
                f.write(card)
