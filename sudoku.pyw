import json
import tkinter as tk
from tkinter import ttk
from random import shuffle
from tkinter.messagebox import showinfo
from winsound import Beep

# global variables

# number of games plus 1
num_of_games = 51

# correct value for each square
master_numbers = None

# game staus
game_started = False

# text variable index for gui square
nums = []

# radomized game numbers
game_index = list(range(1, num_of_games))
shuffle(game_index)

# count correct entries to determine if game is over
correct_count = 0

# used to protect current entries
visible_nums = ['' for _ in range(0, 81)]

# used during looping thru the squares
index = 0

# contains all the raw json information
json_info = []

# end of global variables


def popup_you_won():
    showinfo("Congratulations!", "You Won The Game - Play Another Game")


def read_json_file(path):
    with open(path) as file:
        data = file.read()
        return json.loads(data)


def write_entry_values():
    global correct_count, visible_nums

    for i in range(0, 81):
        d = master_numbers[i]

        if len(d) == 2:
            d = d[:1]
            nums[i].set(d)
            visible_nums[i] = d
            correct_count += 1


def setup_game():
    global master_numbers, correct_count, game_index
    master_numbers = None
    correct_count = 0

    if len(game_index) == 0:
        game_index = list(range(1, num_of_games))
        shuffle(game_index)

    game_num = str(game_index.pop())
    d = json_info['game' + game_num]

    string = ''

    for i in range(0, 9):
        string += d[i] + ','

    master_numbers = string.split(',')
    write_entry_values()


def clear_entries():
    global visible_nums
    for i in range(0, 81):
        nums[i].set('')
        visible_nums[i] = ''


def new_game():
    global game_started
    game_started = False
    clear_entries()
    setup_game()
    game_started = True


def trace(position, dummy_1, dummy_2):
    global correct_count, visible_nums

    if not game_started:
        return

    pos = int(position[6:])
    number_entered = nums[pos].get()
    correct_number = master_numbers[pos]

    if number_entered != correct_number:
        if visible_nums[pos] == '':
            nums[pos].set('')
            Beep(1000, 100)
        else:
            nums[pos].set(visible_nums[pos])

    else:
        correct_count += 1
        visible_nums[pos] = number_entered

        if correct_count == 81:
            popup_you_won()
            new_game()


win = tk.Tk()
win.title('The Sudoku Game')
win.resizable(0, 0)

monty = ttk.LabelFrame(win, text=' Written By Roy ')
monty.grid(column=0, row=0, pady=20, padx=20)

gameFrame = ttk.LabelFrame(monty)
gameFrame.grid(column=1, row=1, pady=20, padx=30)


for row in range(0, 11):

    for column in range(0, 11):
        flag = False

        if column == 3 or column == 7:
            ttk.Separator(gameFrame, orient='horizontal').grid(
                column=str(column), row=str(row), padx=4)
            flag = True

        if row == 3 or row == 7:
            ttk.Separator(gameFrame, orient='vertical').grid(
                column=str(column), row=str(row), pady=4)
            flag = True

        if not flag:
            nums.append(tk.StringVar())
            ttk.Entry(gameFrame, font='Arial 14 bold', width=4, textvariable=nums[index], justify='center').grid(
                column=str(column), row=str(row), padx=2, pady=2, ipady=8, ipadx=2)

            nums[index].trace_add('write', trace)
            index += 1

ttk.Button(monty, text='Play New Game', command=new_game,
           width=40).grid(column=1, row=2, pady=10, padx=10, ipady=4)

json_info = read_json_file('./sudoku.json')
setup_game()
game_started = True

win.mainloop()
