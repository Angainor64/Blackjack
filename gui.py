import tkinter as tk
from PIL import ImageTk, Image
from text_game import InfiniteDeck, get_strategy, suits, numbers, EndGameException
from Crypto.Random.random import shuffle, choice

root = tk.Tk()
root.title('Blackjack Basic Strategy Trainer')
root.configure(background='#1D5D2E', borderwidth=0, width=1366, height=768)
root.geometry('274x582+305+206')
root.iconbitmap('assets/WindowIcon.ico')
# root.resizable(False, False)
resize = 1


class BasicStrategyGame:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.deck = InfiniteDeck()
        self.hands = 0
        self.correct = 0
        self.correct_play = ''
        self.dealer_cardspace = tk.Canvas(root, bg='#1D5D2E', width=196 * resize, height=240 * resize, borderwidth=0,
                                          highlightthickness=0)
        self.player_cardspace = tk.Canvas(root, bg='#1D5D2E', width=196 * resize, height=240 * resize, borderwidth=0,
                                          highlightthickness=0)
        self.dealer_cardspace.create_image(80 * resize, 120 * resize, image=cards['back'])
        self.dealer_upcard = self.dealer_cardspace.create_image(116 * resize, 120 * resize, image=cards['JH'])
        self.player_card1 = self.player_cardspace.create_image(80 * resize, 120 * resize, image=cards['AC'])
        self.player_card2 = self.player_cardspace.create_image(116 * resize, 120 * resize, image=cards['2C'])
        self.buttons = []
        for button_name in ['Surrender', 'Split', 'Double', 'Hit', 'Stand']:
            self.buttons.append(
                tk.Button(self.root, text=button_name, command=lambda: self.guess(button_name), state='disabled'))
        self.button_next = tk.Button(self.root, text='Next', command=self.hand)
        self.feedback = tk.Label(text='Click the "next" button\nto start playing')
        self.accuracy = tk.Label(text='Accuracy:\n0%')
        self.buffer = tk.Label(text='\n', borderwidth=0, bg='#1D5D2E')

    def guess(self, play):
        for button in self.buttons:
            button.configure(state='disabled')
        self.button_next.configure(state='active')
        self.hands += 1
        if play.lower() == self.correct_play.lower():
            self.correct += 1
            self.feedback.configure(text='Correct!')
            self.buffer.configure(text='\n\n')
            self.accuracy.configure(text=f'Accuracy:\n{round(self.correct / self.hands * 100)}%')
        else:
            self.feedback.configure(text=f'Incorrect.\nThe correct answer was {self.correct_play.capitalize()}.')
            self.buffer.configure(text='\n')
            self.accuracy.configure(text=f'Accuracy:\n{round(self.correct / self.hands * 100)}%')

    def hand(self):
        while True:
            dealer = self.deck.pop()
            player = [self.deck.pop(), self.deck.pop()]
            correct = get_strategy(dealer, player)
            if correct == 'blackjack':
                continue
            self.correct_play = correct
            break
        print(dealer, list(map(str, player)))
        self.dealer_cardspace.itemconfigure(self.dealer_upcard, image=card_image(str(dealer)))
        self.player_cardspace.itemconfigure(self.player_card1, image=card_image(str(player[0])))
        self.player_cardspace.itemconfigure(self.player_card2, image=card_image(str(player[1])))
        for button in self.buttons:
            button.configure(state='active')
        self.button_next.configure(state='disabled')
        self.buffer.configure(text='\n\n')
        self.feedback.configure(text='What is the correct play?')

    def play(self) -> None:
        self.dealer_cardspace.grid(row=0, column=1)
        self.player_cardspace.grid(row=4, column=1, rowspan=6)
        tk.Label(text='\n', borderwidth=0, bg='#1D5D2E').grid(row=1, column=1)
        tk.Label(text=' ', borderwidth=0, bg='#1D5D2E').grid(row=6, column=2)
        tk.Label(text=' ', borderwidth=0, bg='#1D5D2E').grid(row=0, column=0)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=4+i, column=3)
        self.button_next.grid(row=9, column=3)
        self.feedback.grid(row=2, column=1, columnspan=3)
        self.accuracy.grid(row=0, column=3)
        self.buffer.grid(row=3, column=1)
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
game = BasicStrategyGame(root)
game.play()
