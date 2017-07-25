import logging
import ttk
import Tkinter as tk
from src.gui.ModelPage import ModelPage


class StartPage(tk.Frame):
    w_ = 300
    h_ = 120

    def __init__(self, parent, root, model):
        tk.Frame.__init__(self, parent)

        self.logger = logging.getLogger(__name__)

        self.parent_ = parent
        self.root_ = root
        self.model_ = model

        #
        self.init_controls()

    #
    # Place a parent at the center of the screen with size
    def centering(self):
        pos_x = (self.winfo_screenwidth() - self.w_) / 2
        pos_y = (self.winfo_screenheight() - self.h_) / 2

        self.root_.geometry('{}x{}+{}+{}'.format(self.w_, self.h_, pos_x, pos_y))

    def init_controls(self):
        l1 = tk.Label(self,
                      text=r'size X',
                      background=None,
                      width=10,
                      height=2,
                      anchor=tk.CENTER).grid(row=0)

        self.entry1 = tk.Entry(self,
                               validate='key',
                               validatecommand=(self.register(self.on_validate),
                                                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),
                               width=36, justify=tk.CENTER)
        self.entry1.grid(row=0, column=1)
        self.entry1.insert(0, str(self.model_.get_grid_x()))

        #
        l1 = tk.Label(self,
                      text=r'size Y',
                      width=10,
                      height=2,
                      background=None,
                      anchor=tk.CENTER).grid(row=1)

        self.entry2 = tk.Entry(self,
                               validate='key',
                               validatecommand=(self.register(self.on_validate),
                                                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),
                               width=36,
                               justify=tk.CENTER)
        self.entry2.grid(row=1, column=1)
        self.entry2.insert(0, str(self.model_.get_grid_y()))

        #
        l3 = tk.Label(self,
                      text=r'Beta',
                      width=10,
                      height=2,
                      background=None,
                      anchor=tk.CENTER).grid(row=2)

        self.entry3 = tk.Entry(self,
                               validate='key',
                               validatecommand=(self.register(self.on_validate),
                                                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'),
                               width=36,
                               justify=tk.CENTER)
        self.entry3.grid(row=2, column=1)
        self.entry3.insert(0, str(self.model_.get_inverse_temperature()))

        s = ttk.Style()
        s.configure('Kim.TButton', foreground='maroon', background='green')

        but1 = tk.Button(self,
                         text='Start!',
                         command=self.button_action,
                         borderwidth=1,
                         relief=tk.SOLID
                         ).grid(row=3, column=1)

    def button_action(self):
        self.model_.set_inverse_temperature(float(self.entry3.get()))
        self.model_.set_grid_x(int(self.entry1.get()))
        self.model_.set_grid_y(int(self.entry2.get()))
        self.model_.update_model()

        # self.root_.init_model_page(self.parent_, self.model_)
        self.root_.show(ModelPage)
        self.destroy()

        self.logger.info('Button was pressed')

    def on_validate(self, d, i, P, s, S, v, V, W):
        """
        :param d: type of action: 1 - insert, 0 - delete, -1 - other
        :param i: index of char string to be inserted/deleted, or -1
        :param P: value of the entry if the edit is allowed
        :param s: value of entry prior to editing
        :param S: the text string being inserted or deleted, if any
        :param v: the type of validation that is currently set
        :param V: the type of validation that triggered the callback
                    (key, focusin, focusout, forced)
        :param W: the tk name of the widget
        :return: True/False -> Valid / Invalid
        Found it here:
            https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        Very good answer!
        """

        if d == '1':
            if W == str(self.entry1) or W == str(self.entry2):

                if S.isdigit():
                    return True
                return False

            if W == str(self.entry3):
                try:
                    float(s+S)
                    return True
                except ValueError:
                    return False
        return True