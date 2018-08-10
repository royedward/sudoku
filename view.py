import tkinter as tk
from tkinter import ttk


class View:
    def __init__(self, trace_function, new_game):
        self.nums = []
        self.trace = trace_function
        self.new_game = new_game
        self.win = None

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

        return self.nums

    def start_game(self):
        self.win.mainloop()
