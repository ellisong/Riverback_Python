import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import xml.etree.ElementTree as ET

from ui import UI
from dictionary import Dictionary
from imageeditor import ImageEditor
from datacompressor import DataCompressor
from color import Color
from palette import Palette
from graphicbank import GraphicBank
from level import LevelHeader, Level

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
    LEVEL_TILE_AMOUNT = 4096
    # shift and & constants
    AND_TILE_VFLIP = 0b10000000
    AND_TILE_VFLIP_SHIFT = 7
    AND_TILE_HFLIP = 0b01000000
    AND_TILE_HFLIP_SHIFT = 6
    AND_TILE_PRIORITY = 0b00100000
    AND_TILE_PRIORITY_SHIFT = 5
    AND_TILE_PALETTE = 0b00011100
    AND_TILE_PALETTE_SHIFT = 2
    AND_TILE_BANK = 0b00000011
    AND_TILE_BANK_SHIFT = 0
    
    uiRoot = tk.Tk()
    ui = UI(master=uiRoot)
    ui.master.title('Riverback')
    
    f = open('test.smc', 'rb')
    romdata = f.read()
    f.close()
    
    level = 11
    level00header = LevelHeader(0xF298+(level*37), 0)
    level00header.update(romdata)
    leveldata = DataCompressor.decompress(romdata, level00header.levelPointer)
    level00 = Level(level00header)
    level00.update(leveldata)
    
    tempGraphicsAddresses = [0x70000, 0x68000, 0x58000, 0x60000, 0x88000, 0x98000, 0x70000, 0x68000, 0x50000, 0x90000, 0xA0000, 0xA4092, 0x80000, 0xAB680]
    
    paletteIndex = 1
    bank0data = DataCompressor.decompress(romdata, tempGraphicsAddresses[level00header.graphicsBankIndex*2])
    bank0 = GraphicBank(bank0data, True)
    bank0.updateImage(paletteIndex)
    bank1data = DataCompressor.decompress(romdata, tempGraphicsAddresses[level00header.graphicsBankIndex*2+1])
    bank1 = GraphicBank(bank1data, False)
    bank1.setPalettes(bank0.getPalettes())
    bank1.updateImage(paletteIndex)
    
    levelBankData, offset = bank0.getPlanarTilesFromBankData(level00.tileIndex, 0)
    levelBankData.extend((bank1.getPlanarTilesFromBankData(level00.tileIndex, offset))[0])
    tileOffset = bank0.calculateTileOffset(level00.tileIndex, 0)
    levelBank = GraphicBank(levelBankData, False)
    levelBank.tileAmount = len(levelBankData) // 0x20
    levelBank.setPalettes(bank0.getPalettes())
    levelBank.updateImage(paletteIndex)
    
    img = Image.new('RGB', (EDITORCANVAS_WIDTH, EDITORCANVAS_HEIGHT))
    imageDict.set('levelImg', img)
    imageDict.set('levelImgTk', ImageEditor.convertImageToTkPhotoImage(img))
        
    img = levelBank.getImage()
    imageDict.set('imgBank0', img)
    imageDict.set('imgBankTk0', ImageEditor.convertImageToTkPhotoImage(img))

    ui.createLevelEditorWidgets(imageDict.get('imgBankTk0'), imageDict.get('levelImgTk'))
    
    x = 0
    y = 0
    levelpointer = 0
    while (levelpointer < level00.LEVEL_TILE_AMOUNT):
        for y in range(0,512,8):
            for x in range(0,512,8):
                tile = level00.tilemap[levelpointer]
                prop = level00.tilemap[levelpointer+1]
                levelpointer += 2
                
                vflip = ((prop & AND_TILE_VFLIP) >> AND_TILE_VFLIP_SHIFT)
                hflip = ((prop & AND_TILE_HFLIP) >> AND_TILE_HFLIP_SHIFT)
                priority = ((prop & AND_TILE_PRIORITY) >> AND_TILE_PRIORITY_SHIFT)
                palette = ((prop & AND_TILE_PALETTE) >> AND_TILE_PALETTE_SHIFT)
                bank = ((prop & AND_TILE_BANK) >> AND_TILE_BANK_SHIFT)
                img = levelBank.getTileImage(tile + (bank*256), level00.paletteIndex[palette]-1)
                if ((hflip != 0) or (vflip != 0)):
                    img = ImageEditor.createTransposedImage(img, hflip, vflip, 0)
                ui.pasteOnLevelCanvas(ImageEditor.convertImageToTkPhotoImage(img), x, y)

    ui.mainloop()
    

