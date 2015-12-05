import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import xml.etree.ElementTree as ET

from color import Color
from datacompressor import DataCompressor
from dictionary import Dictionary
from graphicbank import GraphicBank
from imageeditor import ImageEditor
from level import LevelHeader, Level
from leveleditor import LevelEditor
from palette import Palette
from ui import UI

import sys
import traceback


if __name__ == "__main__":
    #tree = ET.parse('data.xml')
    #treeRoot = tree.getroot()
    imageDict = Dictionary()
    
    TILE_WIDTH = 8
    TILE_HEIGHT = 8
    EDITORTILESET_WIDTH = 16 * TILE_WIDTH
    EDITORTILESET_HEIGHT = 64 * TILE_HEIGHT
    EDITORCANVAS_WIDTH = 64 * TILE_WIDTH
    EDITORCANVAS_HEIGHT = 64 * TILE_HEIGHT
    
    uiRoot = tk.Tk()
    ui = UI(master=uiRoot)
    ui.master.title('Riverback')
    
    f = open('test.smc', 'rb')
    romdata = f.read()
    f.close()
    
    levelNumber = 8
    levelEditor = LevelEditor()
    levelEditor.openLevel(romdata, levelNumber)
    levelEditor.updateGraphicsBanks(romdata)
    levelEditor.updateLevelBank()
    
    img = Image.new('RGB', (EDITORCANVAS_WIDTH, EDITORCANVAS_HEIGHT))
    imageDict.set('levelImg', img)
    imageDict.set('levelImgTk', ImageEditor.convertImageToTkPhotoImage(img))
        
    img = levelEditor.levelBank.getImage()
    imageDict.set('imgBank0', img)
    imageDict.set('imgBankTk0', ImageEditor.convertImageToTkPhotoImage(img))

    ui.createLevelEditorWidgets(imageDict.get('imgBankTk0'), imageDict.get('levelImgTk'))
    
    levelEditor.updateEditorCanvasImage(ui)
    
    ui.mainloop()
    

