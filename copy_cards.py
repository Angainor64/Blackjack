"""
I downloaded the card assets from https://www.kenney.nl/assets/playing-cards-pack. This code just copies those to the
assets folder in this directory, and names them something a bit more programmatic.
"""

suits = {'clubs': 'C', 'diamonds': 'D', 'hearts': 'H', 'spades': 'S'}
values = ['A', '02', '03', '04', '05', '06', '07', '08', '09', '10', 'J', 'Q', 'K']
user_name = 'user'  # Replace with the name of the current user. Doing this because this is uploaded to the internet

if __name__ == '__main__':
    old_path = f'C:\\Users\\{user_name}\\Downloads\\playing-cards-pack\\PNG\\Cards (large)\\card'
    new_path = 'assets\\cards\\'
    for suit in suits.keys():
        for value in values:
            with open(f'{old_path}_{suit}_{value}.png', 'rb') as f:
                card = f.read()
            try:
                value = str(int(value))
            except ValueError:
                pass
            with open(f'{new_path}{value}{suits[suit]}.png', 'wb') as f:
                f.write(card)
