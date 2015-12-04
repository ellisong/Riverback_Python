import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

from imageeditor import ImageEditor

class UI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.imageList = []
        self.pack()
    
    def createLevelEditorWidgets(self, imgBankTk0, levelImgTk):
        self.tilesetFrame = Frame(self)
        self.tilesetFrame.pack(side="left")
        
        self.imgBankTk0 = imgBankTk0
        self.imgBankCanvas0 = tk.Canvas(self.tilesetFrame, width=imgBankTk0.width(), height=imgBankTk0.height())
        self.imgBankCanvas0.create_image(0, 0, anchor=tk.NW, image=self.imgBankTk0)
        self.imgBankCanvas0.pack(side="top", expand=True)
        
        self.levelImgTk = levelImgTk
        self.levelCanvas = tk.Canvas(self, width=512, height=512)
        self.levelCanvas.create_image(0, 0, anchor=tk.NW, image=self.levelImgTk)
        self.levelCanvas.pack(side="left")

    #def createWidgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        #self.hi_there.pack(side="top")

    #def say_hi(self):
    #    print("hi there, everyone!")
    
    def pasteOnLevelCanvas(self, imageTk, x, y):
        img = imageTk
        self.imageList.append(img)
        self.levelCanvas.create_image(x, y, image=img, anchor=tk.NW)