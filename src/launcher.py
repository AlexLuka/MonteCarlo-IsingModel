import os
import time
import logging
import Tkinter as tk
from model import Model

from src.gui.ModelPage import ModelPage
from src.gui.StartPage import StartPage


class Main(tk.Tk):

    """
        Learned from Sentdex's GUI tutorial
    """

    def __init__(self):
        #
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, '2D Ising Model')

        # init the model
        model = Model()

        #
        # logger. It was initialized in the main() method.
        self.logger = logging.getLogger(__name__)

        # init GUI
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()

        for F in (StartPage, ModelPage):
            frame = F(container, self, model)
            frame.grid(row=0, column=0)
            self.frames[F] = frame

            if F != StartPage:
                frame.grid_remove()

        self.show(StartPage)

    def show(self, container):
        frame = self.frames[container]
        frame.tkraise()
        frame.centering()
        frame.grid()

        if isinstance(frame, ModelPage):
            frame.draw()
            frame.update_view()

        self.logger.info('Show {}'.format(container))


#
#
#
#
#
def main():
    # Init logger
    logging.basicConfig(filename=os.path.join('..', 'logs', 'logfile.log'),
                        level=logging.INFO,
                        format='%(asctime)s: [%(name)s] [%(levelname)s] --- %(message)s'
                        )
    logging.info('\n'*5 + '------>' + 'Starting project 2')
    #

    app = Main()
    app.mainloop()


if __name__ == '__main__':
    main()
