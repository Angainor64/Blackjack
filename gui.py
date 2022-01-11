import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title('Blackjack Basic Strategy Trainer')
root.configure(background='#1D5D2E', borderwidth=0, width=1366, height=768)
root.geometry('1366x768+139+105')
root.iconbitmap('assets/WindowIcon.ico')


class CardImage:
    def __init__(self, card: str):
        self.card = card
        self.image = ImageTk.PhotoImage(Image.open(f'assets/cards/{card}.png'))


def print_geometry():
    print(root.geometry())


# frame = tk.Frame(root, borderwidth=0)
# frame.pack()
canvas = tk.Canvas(root, bg='#1D5D2E', width=160, height=240, borderwidth=0, highlightthickness=0)
canvas.pack()
img = ImageTk.PhotoImage(file='assets/cards/AC.png')
canvas.create_image(80, 120, image=img)
my_button = tk.Button(root, text='Print geometry', command=print_geometry)
my_button.pack()
# label = tk.Label(image=img, borderwidth=0)
# label.pack()

print(root.geometry())
root.mainloop()
