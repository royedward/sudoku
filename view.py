from tkinter.messagebox import showinfo
from random import shuffle
from winsound import Beep
from tkinter import ttk
import tkinter as tk
import json

class View:
    num_of_games = 51

    def __init__(self):
        self.win = None
        self.nums = []
        self.json_info = None
        self.game_started = False
        self.correct_count = 0
        self.master_numbers = None

        self.visible_nums = ['' for _ in range(0, 81)]

        self.game_index = list(range(1, View.num_of_games))

        for _ in range(0, 6):
            shuffle(self.game_index)

    # layout graphical user interface
    def setup_view(self):
        self.win = tk.Tk()
        self.win.title('The Sudoku Game')
        self.win.resizable(0, 0)

        monty = ttk.LabelFrame(self.win, text=' Written By Roy ')
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
                    var = tk.StringVar()
                    self.nums.append(var)
                    ttk.Entry(gameFrame, font='Arial 14 bold', width=4, textvariable=var, justify='center').grid(
                        column=str(column), row=str(row), padx=2, pady=2, ipady=8, ipadx=2)

                    var.trace_add('write', self.trace)

        ttk.Button(monty, text='Play New Game', command=self.new_game,
                   width=40).grid(column=1, row=2, pady=10, padx=10, ipady=4)

    # popup window when game is over
    def popup_you_won(self):
        showinfo("Congratulations!", "You Won The Game - Play Another Game")

    # read json file containing answers for all num_of_games games
    def read_json_file(self, path):
        with open(path) as file:
            data = file.read()
            return json.loads(data)

    # if number is greater than 9, it is a starting visible number
    def write_entry_values(self):
        for i in range(0, 81):
            d = self.master_numbers[i]

            if len(d) == 2:
                d = d[:1]
                self.nums[i].set(d)
                self.visible_nums[i] = d
                self.correct_count += 1

    # get game number and json file
    def setup_game(self):
        self.master_numbers = None
        self.correct_count = 0

        if len(self.game_index) == 0:
            self.game_index = list(range(1, self.num_of_games))

            for _ in range(0, 6):
                shuffle(self.game_index)

        game_num = str(self.game_index.pop())
        d = self.json_info['game' + game_num]

        string = ''

        for i in range(0, 9):
            string += d[i] + ','

        self.master_numbers = string.split(',')
        self.write_entry_values()
        self.game_started = True

    # clear all numbers for new game
    def clear_entries(self):
        for i in range(0, 81):
            self.nums[i].set('')
            self.visible_nums[i] = ''

    def new_game(self):
        self.game_started = False
        self.clear_entries()
        self.setup_game()
        self.game_started = True

    # handler that is called when a number is entered
    def trace(self, position, dummy_1, dummy_2):
        if not self.game_started:
            return

        pos = int(position[6:])
        number_entered = self.nums[pos].get()
        correct_number = self.master_numbers[pos]

        if number_entered != correct_number:
            if self.visible_nums[pos] == '':
                self.nums[pos].set('')
                Beep(1000, 100)
            else:
                self.nums[pos].set(self.visible_nums[pos])

        else:

            self.correct_count += 1
            self.visible_nums[pos] = number_entered

            if self.correct_count == 81:
                self.popup_you_won()
                self.new_game()

    def start_game(self):
        self.win.mainloop()

    def start_view(self):
        self.setup_view()
        self.json_info = self.read_json_file('./sudoku.json')
        self.setup_game()
