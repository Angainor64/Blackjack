class Card:
    def __init__(self, suit: str, value: str):
        self.id = {'suit': suit, 'value': value}
        if ord(value) > 59:
            self.count = -1
        elif int(value) <= 6:
            self.count = 1
        else:
            self.count = 0

    def __str__(self):
        return self.id['suit'] + self.id['value']

    