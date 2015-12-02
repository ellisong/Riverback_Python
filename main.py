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
    tree = ET.parse('data.xml')
    treeRoot = tree.getroot()
    imageDict = Dictionary()
    
    LEVEL_ADDRESS = 0xC210E
    TILE_WIDTH = int(treeRoot.find('tile/width').text)
    TILE_HEIGHT = int(treeRoot.find('tile/height').text)
    EDITORTILESET_WIDTH = int(treeRoot.find('editortileset/tileamount_width').text)
    EDITORTILESET_WIDTH *= TILE_WIDTH
    EDITORTILESET_HEIGHT = int(treeRoot.find('editortileset/tileamount_height').text)
    EDITORTILESET_HEIGHT *= TILE_HEIGHT
    EDITORCANVAS_WIDTH = int(treeRoot.find('editorcanvas/tileamount_width').text)
    EDITORCANVAS_WIDTH *= TILE_WIDTH
    EDITORCANVAS_HEIGHT = int(treeRoot.find('editorcanvas/tileamount_height').text)
    EDITORCANVAS_HEIGHT *= TILE_HEIGHT
    LEVEL_TILE_AMOUNT = int(treeRoot.find('level/tileamount').text)
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
    
    paletteIndex = 1
    bank00data = DataCompressor.decompress(romdata, 0x70000)
    bank00 = GraphicBank(treeRoot, bank00data, True)
    bank00.updateImage(paletteIndex)
    bank01data = DataCompressor.decompress(romdata, 0x68000)
    bank01 = GraphicBank(treeRoot, bank01data, False)
    bank01.setPalettes(bank00.getPalettes())
    bank01.updateImage(paletteIndex)
    
    level = 3
    level00header = LevelHeader(0xF298+(level*37), 0)
    level00header.update(romdata)
    leveldata = DataCompressor.decompress(romdata, level00header.levelPointer)
    level00 = Level(level00header, treeRoot)
    level00.update(leveldata)
    
    levelBank00Data, offset = bank00.getPlanarTilesFromBankData(level00.tileIndex, 0)
    levelBank00Data.extend((bank01.getPlanarTilesFromBankData(level00.tileIndex, offset))[0])
    tileOffset = bank00.calculateTileOffset(level00.tileIndex, 0)
    levelBank00 = GraphicBank(treeRoot, levelBank00Data, False)
    levelBank00.tileAmount = len(levelBank00Data) // 0x20
    levelBank00.setPalettes(bank00.getPalettes())
    levelBank00.updateImage(paletteIndex)
    
    img = Image.new('RGB', (EDITORCANVAS_WIDTH, EDITORCANVAS_HEIGHT))
    imageDict.set('levelImg', img)
    imageDict.set('levelImgTk', ImageEditor.convertImageToTkPhotoImage(img))
        
    img = levelBank00.getImage()
    imageDict.set('imgBank0', img)
    imageDict.set('imgBankTk0', ImageEditor.convertImageToTkPhotoImage(img))

    ui.createLevelEditorWidgets(imageDict.get('imgBankTk0'), imageDict.get('levelImgTk'))
    
    x = 0
    y = 0
    levelpointer = 0
    while (levelpointer < level00.levelTileAmount):
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
                img = levelBank00.getTileImage(tile + (bank*256), level00.paletteIndex[palette]-1)
                if ((hflip != 0) or (vflip != 0)):
                    img = ImageEditor.createTransposedImage(img, hflip, vflip, 0)
                ui.pasteOnLevelCanvas(ImageEditor.convertImageToTkPhotoImage(img), x, y)

    ui.mainloop()
    

