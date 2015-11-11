import tkinter as tk
from tkinter import *
from tkinter.ttk import *

from PIL import Image, ImageTk

class UI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        #self.hi_there.pack(side="top")
        self.levelImg = Image.new('RGB', (512,512))
        self.levelImgTk = ImageTk.PhotoImage(self.levelImg)
        self.levelCanvas = tk.Canvas(self, width=512, height=512)
        self.levelCanvas.create_image(0, 0, anchor=tk.NW, image=self.levelImgTk)
        self.levelCanvas.pack(side="left")

    #def say_hi(self):
    #    print("hi there, everyone!")