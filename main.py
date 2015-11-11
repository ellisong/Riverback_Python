import tkinter as tk

from ui import UI

if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(master=root)
    ui.master.title('Riverback')
    ui.mainloop()