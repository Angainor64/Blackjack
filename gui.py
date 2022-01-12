import tkinter as tk
from PIL import ImageTk, Image
from text_game import InfiniteDeck, get_strategy

root = tk.Tk()
root.title('Blackjack Basic Strategy Trainer')
root.configure(background='#1D5D2E', borderwidth=0, width=1366, height=768)
root.geometry('1366x768+139+105')
root.iconbitmap('assets/WindowIcon.ico')
root.resizable(False, False)
resize = 1


class BasicStrategyGame:
    def __init__(self):
        self.deck = InfiniteDeck()
        self.hands = 0
        self.correct = 0
        self.correct_play = None

    def hand(self):
        while True:
            dealer = self.deck.pop()
            player = [self.deck.pop(), self.deck.pop()]
            correct = get_strategy(dealer, player)
            if correct == 'blackjack':
                continue
            break


def card_image(card: str) -> ImageTk.PhotoImage:
    im = Image.open(f'assets/cards/{card}.png')
    return ImageTk.PhotoImage(im.resize(tuple([int(resize * a) for a in im.size])))


def print_geometry():
    print(root.geometry())


cards = {'back': card_image('back_red'), 'JB': card_image('joker_black'), 'JR': card_image('joker_red')}
for suit in ['C', 'S', 'D', 'H']:
    for number in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
        cards[f'{number}{suit}'] = card_image(f'{number}{suit}')
dealer_cardspace = tk.Canvas(root, bg='#1D5D2E', width=194 * resize, height=240 * resize, borderwidth=0,
                             highlightthickness=0)
dealer_cardspace.grid(row=3, column=0)
dealer_downcard = dealer_cardspace.create_image(80 * resize, 120 * resize, image=cards['AS'])
dealer_upcard = dealer_cardspace.create_image(114 * resize, 120 * resize, image=cards['JH'])
player_card1 = tk.Canvas(root, bg='#1D5D2E', width=160 * resize, height=240 * resize, borderwidth=0,
                         highlightthickness=0)
player_card1.grid(row=0, column=0, columnspan=2)
player_card2 = tk.Canvas(root, bg='#1D5D2E', width=160 * resize, height=240 * resize, borderwidth=0,
                         highlightthickness=0)
player_card2.grid(row=0, column=1, columnspan=2)
button = tk.Button(root, text='close', command=root.quit)
button.grid(row=1, column=0)

root.mainloop()
