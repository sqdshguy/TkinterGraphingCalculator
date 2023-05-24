from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import *

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Grapher")
        self.window.resizable(False, False)
        
        self.font = ("Verdana", 10)
        self.plot_button_font = ("Verdana", 16, "bold")
        
        self.colors = ['red', 'blue', 'green', 'black', 'yellow', 'grey']
        self.color = StringVar()
        self.x_min = DoubleVar(value=-50)
        self.y_min = DoubleVar(value=-50)
        self.x_max = DoubleVar(value=50)
        self.y_max = DoubleVar(value=50)
        self.function = StringVar()
        
        self.plot_frame = self.create_frame()
        self.canvas = self.create_canvas()
        self.create_buttons()
        
        self.window.mainloop()
        
    def create_frame(self):
        frame = Frame(self.window, width=700, height=700, bg="#20221f")
        frame.pack_propagate(False)
        frame.pack(fill="y", expand=True, side="left")
        return frame
    
    def create_canvas(self):
        figure = Figure(figsize=(5, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot([], [])
        
        canvas = FigureCanvasTkAgg(figure, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        canvas._tkcanvas.pack(side="top", fill="both", expand=True)
        
        return canvas
    
    def create_buttons(self):
        functions_frame = Frame(self.plot_frame, width=700, height=163, bg="#20221f")
        functions_frame.pack_propagate(False)
        functions_frame.pack(fill="x", expand=True, side="top")
        
        first_row = Frame(functions_frame, width=670, height=40, bg="#20221f")
        first_row.pack_propagate(False)
        first_row.pack(expand=True, side="top")
        
        second_row = Frame(functions_frame, width=670, height=40, bg="#20221f")
        second_row.pack_propagate(False)
        second_row.pack(expand=True)
        
        third_row = Frame(functions_frame, width=120, height=80, bg="#20221f")
        third_row.pack_propagate(False)
        third_row.pack(expand=True, side="bottom")
        
        button_plot = Button(third_row, font=self.plot_button_font, text="PLOT", width=10, height=2, bg="#20221f",
                                fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                command=self.plot)
        button_plot.grid(row=0, column=0, padx=0, pady=0, columnspan=1, sticky="EWNS")
        
        labels = [
            (first_row, "X min:", self.x_min),
            (first_row, "Y min:", self.y_min),
            (second_row, "X max:", self.x_max),
            (second_row, "Y max:", self.y_max)
        ]
        
        for frame, text, var in labels:
            label = Label(frame, font=self.font, text=text, width=6, height=2, bg="#20221f", fg="white",
                             activeforeground="white")
            label.pack(side="left", padx=3)
            
            entry = Entry(frame, width=6, textvariable=var)
            entry.pack(side="left", padx=3)
        
        Label(first_row, font=self.font, text="Function: y=", width=10, height=2, bg="#20221f", fg="white",
                 activeforeground="white").pack(side="left", padx=3)
        
        function_entry = Entry(first_row, textvariable=self.function)
        function_entry.pack(side="left", padx=3)
    
        spinbox = Spinbox(first_row, values=self.colors, textvariable=self.color)
        spinbox.config(state="readonly", background="#20221f", foreground="#20221f")
        spinbox.pack(side="left", padx=3)

        move_up_button = Button(second_row, text="↑", width=3, height=1, bg="#20221f",
                                   fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                   command=self.move_up)
        move_up_button.pack(side="left", padx=3)

        move_down_button = Button(second_row, text="↓", width=3, height=1, bg="#20221f",
                                     fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                     command=self.move_down)
        move_down_button.pack(side="left", padx=3)

        move_left_button = Button(second_row, text="←", width=3, height=1, bg="#20221f",
                                     fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                     command=self.move_left)
        move_left_button.pack(side="left", padx=3)

        move_right_button = Button(second_row, text="→", width=3, height=1, bg="#20221f",
                                      fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                      command=self.move_right)
        move_right_button.pack(side="left", padx=3)

        zoom_in_button = Button(second_row, font=self.font, text="+", width=3, height=1, bg="#20221f",
                                   fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                   command=self.zoom_in)
        zoom_in_button.pack(side="left", padx=3)

        zoom_out_button = Button(second_row, font=self.font, text="-", width=3, height=1, bg="#20221f",
                                    fg="white", relief="raised", activebackground="#383737", activeforeground="white",
                                    command=self.zoom_out)
        zoom_out_button.pack(side="left", padx=3)
        
        copyright_label = Label(self.plot_frame, text="© Oleksandr Herasymov", font=("Verdana", 8), bg="#20221f", fg="white")
        copyright_label.pack(side="bottom", pady=5)

    def plot(self):
        color = self.color.get()
        func = self.function.get()
        
        try:
            x = arange(int(self.x_min.get()), int(self.x_max.get()) + 1, 0.1)
            y = eval(func)
        except:
            messagebox.showerror('Error', 'An error occured while plotting\nPlease the check the limits and the function')
        
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.set_xlim([self.x_min.get(), self.x_max.get()])
        ax.set_ylim([self.y_min.get(), self.y_max.get()])
        ax.axhline(color='black', lw=0.5)
        ax.axvline(color='black', lw=0.5)
        ax.plot(x, y, color=color)
        self.canvas.draw()

    def move_up(self):
        self.y_min.set(self.y_min.get() + 10)
        self.y_max.set(self.y_max.get() + 10)
        self.plot()

    def move_down(self):
        self.y_min.set(self.y_min.get() - 10)
        self.y_max.set(self.y_max.get() - 10)
        self.plot()

    def move_left(self):
        self.x_min.set(self.x_min.get() - 10)
        self.x_max.set(self.x_max.get() - 10)
        self.plot()

    def move_right(self):
        self.x_min.set(self.x_min.get() + 10)
        self.x_max.set(self.x_max.get() + 10)
        self.plot()

    def zoom_in(self):
        if self.x_max.get() > 10:
            self.x_min.set(self.x_min.get() + 10)
            self.x_max.set(self.x_max.get() - 10)
            self.y_min.set(self.y_min.get() + 10)
            self.y_max.set(self.y_max.get() - 10)
        self.plot()

    def zoom_out(self):
        self.x_min.set(self.x_min.get() - 10)
        self.x_max.set(self.x_max.get() + 10)
        self.y_min.set(self.y_min.get() - 10)
        self.y_max.set(self.y_max.get() + 10)
        self.plot()

if __name__ == '__main__':
    app = App()
