import logging
import ttk
import time
import Tkinter as tk
import Queue
import threading

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


style.use('ggplot')


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
        self.ax = None

        # queue for online update of the model's state
        self.queue = Queue.Queue()
        self.simulation_thread = None

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
        # self.canvas = tk.Canvas(fr1, width=self.cw_, height=self.cw_)
        # self.canvas.pack(fill=None, expand=True)
        # self.draw()

        # matplotlib canvas
        f = Figure(figsize=(5, 5), dpi=100)
        self.ax = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, master=fr1)
        # self.canvas.show()
        self.canvas.get_tk_widget().pack(fill=None, expand=True)
        self.draw()

        # subframe 2
        fr2 = tk.Frame(self, background='green')
        fr2.grid(row=0, column=1, sticky='news')

        # init controls for the subframe 2
        self.b1 = tk.Button(fr2,
                       text='Run simulation',
                       command=self.simulation_run,
                       borderwidth=1,
                       relief=tk.SOLID
                       )
        self.b1.grid(row=3, column=1)

        self.b2 = tk.Button(fr2,
                       text='Stop simulation',
                       command=self.simulation_stop,
                       borderwidth=1,
                       relief=tk.SOLID
                       )
        self.b2.grid(row=3, column=3)
        self.b2.config(state='disabled')

    # ---> GHOST
    # def draw(self):
    #     """
    #         Draw the current state of the system.
    #     """
    #     # get initial grid
    #     m = self.model_.get_mapping()
    #
    #     grid_h = self.cw_ / self.model_.get_grid_y()
    #     grid_w = self.cw_ / self.model_.get_grid_x()
    #
    #     for i in range(self.model_.get_grid_x()):
    #         for j in range(self.model_.get_grid_x()):
    #             self.canvas.create_rectangle(i * grid_w,
    #                                          j * grid_h,
    #                                          (i + 1) * grid_w,
    #                                          (j + 1) * grid_h,
    #                                          fill=self.model_.get_settings().get_cell_colors()[m[i, j]],
    #                                          outline=self.model_.get_settings().get_cell_colors()[m[i, j]]
    #                                          )
    #
    #     print m[0, 0]

    def draw(self):
        self.ax.clear()

        # Display 2D Ising Model
        self.ax.imshow(self.model_.get_mapping(),
                       interpolation='none',
                       cmap=self.model_.get_settings().get_model_colormap())
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def simulation_run(self):
        self.simulation_thread = threading.Thread(target=self.model_.run, args=(self.queue,))
        self.simulation_thread.start()

        # threading.Thread(target=self.model_.run).start()
        self.after(1, self.check_queue)
        self.b1.config(state='disabled')
        self.b2.config(state='active')

    def simulation_stop(self):
        self.logger.info('Set RUNNING_FLAG=FALSE to computational thread')
        self.model_.set_running_flag(False)

        try:
            self.simulation_thread.join()
        except RuntimeError as re:
            self.logger.exception('Error occurred while joining simulation thread')

        self.b2.config(state='disabled')
        self.b1.config(state='active')

    def check_queue(self):
        try:
            val = self.queue.get(0)
            self.logger.info('Message received from the computational thread: [{}].'.format(val))
        except Queue.Empty:
            self.draw()
            self.after(1, self.check_queue)
            self.logger.info('Queue is empty. Continue monitoring the simulation.')
