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
        self.magnetization_ax = None
        self.magnetization_canvas = None
        self.tf1 = None
        self.tf2 = None
        self.tf3 = None

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

        self.config(bg='dimgray')
        #
        # subframe 1
        fr1 = tk.Frame(self, background='dimgray')
        fr1.grid(row=0, column=0, sticky='news')

        # matplotlib canvas
        f = Figure(figsize=(5, 5), dpi=100)
        self.ax = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, master=fr1)
        # self.canvas.show()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # sub-frame 2: This Frame will contain the controls (Buttons and Graphs).
        # padx=(2, 0) specifies the pads one the left and right of the widget.
        # Left pad = 2 serves as separator between fr1 and fr2.
        fr2 = tk.Frame(self, background='dimgray')
        fr2.grid(row=0, column=1, sticky='news', padx=(2, 0))

        # fr2.grid_rowconfigure(5)
        for i in range(3):
            fr2.grid_columnconfigure(i, weight=1)
        fr2.grid_rowconfigure(0, weight=0)
        fr2.grid_rowconfigure(1, weight=0)
        fr2.grid_rowconfigure(2, weight=0)
        fr2.grid_rowconfigure(3, weight=10)

        # init controls for the subframe 2
        self.b1 = tk.Button(fr2,
                            text='Run simulation',
                            command=self.simulation_run,
                            borderwidth=1,
                            relief=tk.SOLID
                            )
        self.b1.grid(row=0, column=2)

        self.b2 = tk.Button(fr2,
                            text='Stop simulation',
                            command=self.simulation_stop,
                            borderwidth=1,
                            relief=tk.SOLID
                            )
        self.b2.grid(row=1, column=2)
        self.b2.config(state='disabled')

        #
        tk.Button(fr2, text='Useless button', borderwidth=1, relief=tk.SOLID).grid(row=2, column=2)

        # Inverse temperature
        l = tk.Label(fr2, text='Beta (Inverse temperature)', bg='gray', anchor=tk.E)
        l.grid(row=0, column=0, sticky='news')

        l2 = tk.Label(fr2, text='Nx ', bg='gray', anchor=tk.E)
        l2.grid(row=1, column=0, sticky='news')

        l3 = tk.Label(fr2, text='Ny ', bg='gray', anchor=tk.E)
        l3.grid(row=2, column=0, sticky='news')

        self.tf1 = tk.Entry(fr2, justify=tk.CENTER)
        self.tf1.grid(row=0, column=1, padx=1, pady=1)

        self.tf2 = tk.Entry(fr2, justify=tk.CENTER)
        self.tf2.grid(row=1, column=1, padx=1, pady=1)

        self.tf3 = tk.Entry(fr2, justify=tk.CENTER)
        self.tf3.grid(row=2, column=1, padx=1, pady=1)
        # grid size

        # Notebook (Tabbed Pane)
        nb = ttk.Notebook(fr2)

        # Tab 1
        tab1 = tk.Frame(nb)

        f2 = Figure(figsize=(5, 4.05), dpi=100)
        self.magnetization_ax = f2.add_subplot(111)
        self.magnetization_canvas = FigureCanvasTkAgg(f2, master=tab1)
        self.magnetization_canvas.get_tk_widget().pack(fill=tk.Y, expand=True)

        # Tab 2
        tab2 = tk.Frame(nb)

        f3 = Figure(figsize=(5, 4.05), dpi=100)
        self.energy_ax = f3.add_subplot(111)
        self.energy_canvas = FigureCanvasTkAgg(f3, master=tab2)
        self.energy_canvas.get_tk_widget().pack(fill=tk.Y, expand=True)

        # Tab 3
        tab3 = tk.Frame(nb)

        # Tab 4
        tab4 = tk.Frame(nb)

        nb.add(tab1, text=r'Magnetization', compound=tk.TOP)
        nb.add(tab2, text=r'Energy')
        nb.add(tab3, text=r'Specific heat')
        nb.add(tab4, text=r'Susceptibility')

        nb.grid(row=3, columnspan=3, sticky='news')

        # Draw
        self.draw()

    def draw(self):
        """
            Draw the Ising model's state on the left panel
        """
        self.ax.clear()

        # Display 2D Ising Model
        self.ax.imshow(self.model_.get_mapping(),
                       interpolation='none',
                       cmap=self.model_.get_settings().get_model_colormap())
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

        # Draw magnetization
        self.magnetization_ax.clear()
        self.magnetization_ax.plot(self.model_.get_magnetization())
        self.magnetization_canvas.draw()

        # Draw magnetization squared
        self.energy_ax.clear()
        self.energy_ax.plot(self.model_.get_energy())
        self.energy_canvas.draw()

    def simulation_run(self):
        # run the simulation in separate thread
        # communication with the mainloop is done via queue
        self.simulation_thread = threading.Thread(target=self.model_.run, args=(self.queue,))
        self.simulation_thread.start()

        self.after(1, self.check_queue)
        self.b1.config(state='disabled')
        self.b2.config(state='active')

    def simulation_stop(self):
        self.logger.info('Set RUNNING_FLAG=FALSE to computational thread')
        self.model_.set_running_flag(False)

        try:
            self.simulation_thread.join()
        except RuntimeError as re:
            self.logger.exception('Error occurred while joining simulation thread \n {}'.format(re))

        self.b2.config(state='disabled')
        self.b1.config(state='active')

    def check_queue(self):
        try:
            # Get the message from the queue
            val = self.queue.get(0)
            # If message received, print the STOP message to a logger
            self.logger.info('Message received from the computational thread: [{}].'.format(val))
            # Else, raise an exception that the queue is empty, redraw the system, and keep monitoring the queue
        except Queue.Empty:
            self.draw()
            self.after(20, self.check_queue)
            self.logger.info('Queue is empty. Continue monitoring the simulation.')

    def update_view(self):
        self.tf1.insert(0, str(self.model_.get_inverse_temperature()))
        self.tf2.insert(0, str(self.model_.get_grid_x()))
        self.tf3.insert(0, str(self.model_.get_grid_y()))

    def update_model(self):
        self.model_.set_inverse_temperature(float(self.tf1.get()))
        self.model_.set_grid_x(int(self.tf2.get()))
        self.model_.set_grid_y(int(self.tf3.get()))
        self.model_.update_model()
