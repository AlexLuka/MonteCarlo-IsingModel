import logging
import ttk
import time
import Tkinter as tk


class ModelPage(tk.Frame):
    w_ = 1000
    h_ = 500
    cw_ = 480

    def __init__(self, parent, root, model):
        tk.Frame.__init__(self, parent)

        self.logger = logging.getLogger(__name__)

        self.parent_ = parent
        self.root_ = root
        self.model_ = model

        #
        self.canvas = None

        self.init_controls()

    #
    # Place a parent at the center of the screen with size
    def centering(self):
        pos_x = (self.winfo_screenwidth() - self.w_) / 2
        pos_y = (self.winfo_screenheight() - self.h_) / 2

        self.root_.geometry('{}x{}+{}+{}'.format(self.w_, self.h_, pos_x, pos_y))

    def init_controls(self):
        # Configure top frame
        self.grid(row=0, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1, uniform='group1')
        self.grid_columnconfigure(1, weight=1, uniform='group1')
        self.grid_rowconfigure(0, weight=1)

        # configure two subframes:
        #
        # subframe 1
        fr1 = tk.Frame(self, background='dimgray')
        fr1.grid(row=0, column=0, sticky='news')

        # plotting canvas
        self.canvas = tk.Canvas(fr1, width=self.cw_, height=self.cw_)
        self.canvas.pack(fill=None, expand=True)

        self.draw()

        # subframe 2
        fr2 = tk.Frame(self, background='green')
        fr2.grid(row=0, column=1, sticky='news')

        # init controls for the subframe 2

        b1 = tk.Button(fr2,
                       text='Run simulation',
                       command=self.simulation_run,
                       borderwidth=1,
                       relief=tk.SOLID
                       ).grid(row=3, column=1)

    def draw(self):
        """
            Draw the current state of the system.
        """
        # get initial grid
        m = self.model_.get_mapping()

        grid_h = self.cw_ / self.model_.get_grid_y()
        grid_w = self.cw_ / self.model_.get_grid_x()

        for i in range(self.model_.get_grid_x()):
            for j in range(self.model_.get_grid_x()):
                self.canvas.create_rectangle(i * grid_w,
                                             j * grid_h,
                                             (i + 1) * grid_w,
                                             (j + 1) * grid_h,
                                             fill=self.model_.get_settings().get_cell_colors()[m[i, j]],
                                             outline=self.model_.get_settings().get_cell_colors()[m[i, j]]
                                             )

    def simulation_run(self):
        print self.model_.calculate_energy()
        # for _ in range(5):
        #     self.model_.update_model()
        #     self.draw()
        #     time.sleep(1)
