import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import choice
from ttkbootstrap import utility

class Ticket(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        self.layoutFilter()
        self.layoutFilter()
        self.layoutFilter()
        self.layoutFilter()


    def layoutFilter(self):
        filter_frame = ttk.Labelframe(master=self, text='default', bootstyle=SUCCESS)
        filter_frame.pack(padx=5, pady=5, fill=None)
        cb = ttk.Checkbutton(master=filter_frame, text='default', bootstyle=SUCCESS)
        cb.pack(padx=5, pady=5, fill=BOTH)
        cb.invoke()

if __name__ == "__main__":
    app = ttk.Window("今年肯定能回家")  #, "superhero", resizable=(False, False)
    Ticket(app)
    app.mainloop()
