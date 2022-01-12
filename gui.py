import tkinter as tk
from PIL import ImageTk, Image
from text_game import InfiniteDeck, get_strategy, suits, numbers, EndGameException
from Crypto.Random.random import shuffle, choice

root = tk.Tk()
root.title('Blackjack Basic Strategy Trainer')
root.configure(background='#1D5D2E', borderwidth=0, width=1366, height=768)
root.geometry('1366x768+139+105')
root.iconbitmap('assets/WindowIcon.ico')
# root.resizable(False, False)
resize = 1


class BasicStrategyGame:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.deck = InfiniteDeck()
        self.hands = 0
        self.correct = 0
        self.correct_play = None
        self.dealer_cardspace = tk.Canvas(root, bg='#1D5D2E', width=196 * resize, height=240 * resize, borderwidth=0, highlightthickness=0)
        self.player_cardspace = tk.Canvas(root, bg='#1D5D2E', width=196 * resize, height=240 * resize, borderwidth=0, highlightthickness=0)
        self.dealer_cardspace.create_image(80 * resize, 120 * resize, image=cards['back'])
        self.dealer_upcard = self.dealer_cardspace.create_image(116 * resize, 120 * resize, image=cards['JH'])
        self.player_card1 = self.player_cardspace.create_image(80 * resize, 120 * resize, image=cards['AC'])
        self.player_card2 = self.player_cardspace.create_image(116 * resize, 120 * resize, image=cards['2C'])
        self.buttons = []
        for button_name in ['Surrender', 'Split', 'Double', 'Hit', 'Stand']:
            self.buttons.append(tk.Button(self.root, text=button_name, command=lambda: self.guess(button_name)))
        self.button_next = tk.Button(self.root, text='Next', command=self.hand)

    def hand(self):
        while True:
            dealer = self.deck.pop()
            player = [self.deck.pop(), self.deck.pop()]
            correct = get_strategy(dealer, player)
            if correct == 'blackjack':
                continue
            self.correct_play = correct
            break
        self.dealer_cardspace.itemconfigure(self.dealer_upcard, image=str(dealer))
        self.player_cardspace.itemconfigure(self.player_card1, image=str(player[0]))
        self.player_cardspace.itemconfigure(self.player_card2, image=str(player[1]))
        for button in self.buttons:
            button.configure(state='active')
        self.button_next.configure(state='disabled')

    def play(self) -> None:
        self.dealer_cardspace.grid(row=0, column=0, rowspan=2)
        self.player_cardspace.grid(row=3, column=0, rowspan=6)
        self.root.mainloop()


def card_image(card: str) -> ImageTk.PhotoImage:
    im = Image.open(f'assets/cards/{card}.png')
    return ImageTk.PhotoImage(im.resize(tuple([int(resize * a) for a in im.size])))


def print_geometry():
    print(root.geometry())


def update_card(canvas: tk.Canvas, card_id: int, new_img: ImageTk.PhotoImage):
    canvas.itemconfigure(card_id, image=new_img)


cards = {'back': card_image('back_red')}
for suit in suits:
    for number in numbers:
        cards[f'{number}{suit}'] = card_image(f'{number}{suit}')
space = tk.Label(text='\n', borderwidth=0, bg='#1D5D2E')
space.grid(row=2, column=0)
game = BasicStrategyGame(root)
game.play()
