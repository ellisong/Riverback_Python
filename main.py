import tkinter as tk
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET

from ui import UI
from dictionary import Dictionary
from imageeditor import ImageEditor
from datacompressor import DataCompressor

import sys
import traceback


if __name__ == "__main__":
    TILE_DIMENSION = 8
    BANK_TILE_AMOUNT = 256
    LEVEL_ADDRESS = 0xC210E
    LEVEL_TILE_AMOUNT = 0x1000
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
    
    tree = ET.parse('data.xml')
    treeRoot = tree.getroot()
    imageDict = Dictionary()
    
    # uiRoot = tk.Tk()
    # ui = UI(master=uiRoot)
    # ui.master.title('Riverback')
    # IE = ImageEditor()
    
    # img = Image.open("umihara-kawase-bank0-0.png")
    # imageDict.set('imgBank0', img)
    # imglist = IE.getTilesListFromTileset(img, BANK_TILE_AMOUNT, TILE_DIMENSION, TILE_DIMENSION)
    # #imglist = IE.convertImagesToTkPhotoImage(imglist)
    # imageDict.setMultiple(imglist, 'imgTile', '_', 0)
    # imageDict.set('imgBankTk0', IE.convertImageToTkPhotoImage(img))
    
    # img = Image.open("umihara-kawase-bank0-1.png")
    # imageDict.set('imgBank1', img)
    # imglist = IE.getTilesListFromTileset(img, BANK_TILE_AMOUNT, TILE_DIMENSION, TILE_DIMENSION)
    # #imglist = IE.convertImagesToTkPhotoImage(imglist)
    # imageDict.setMultiple(imglist, 'imgTile', '_', BANK_TILE_AMOUNT)
    # imageDict.set('imgBankTk1', IE.convertImageToTkPhotoImage(img))
    
    # img = Image.new('RGB', (512,512))
    # imageDict.set('levelImg', img)
    # imageDict.set('levelImgTk', IE.convertImageToTkPhotoImage(img))
    
    f = open('test.smc', 'rb')
    romdata = f.read()
    f.close()
    pos = 0
    for x in [0x70000, 0x68000, 0x58000, 0x60000, 0x88000, 0x98000, 0x70000, 0x68000, 0x50000, 0x90000, 0xA0000, 0xA4092, 0x80000, 0xAB680]:
        decomp = DataCompressor.decompress(romdata, x)
        print("data length decomp: " + str(len(decomp)))
        f = open('bank'+str(pos//2)+str(pos%2)+'.smc', 'w+b')
        f.write(decomp)
        f.close()
        pos += 1
    #comp = DataCompressor.compress(decomp)
    #print("data length comp: " + str(len(comp)))
    #f = open('compress.out', 'w+b')
    #f.write(comp)
    #f.close()
    #decomp2 = DataCompressor.decompress(comp, 0)
    #print("data length decomp2: " + str(len(decomp2)))
    #f = open('decompress2.out', 'w+b')
    #f.write(decomp2)
    #f.close()
    
    # posLen = 0
    # if (len(leveldata) % 8 != 0):
        # posLen = len(leveldata) // 8 + 1
    # else:
        # posLen = len(leveldata) // 8
    # posB = []
    # for x in range(0, posLen):
        # posB.append(0)
    # levelWithPos = DataCompressor.insertPosBytesIntoData(list(leveldata), posB)
    # finaldata = bytearray(romdata)
    # x = 0x100000
    # while x < (0x100000 + len(levelWithPos)):
        # finaldata[x] = levelWithPos[x-0x100000]
        # x += 0x01
    # # insert compression end bytes
    # finaldata[x] = 0x80
    # finaldata[x+1] = 0x00
    # finaldata[x+2] = 0x00
    # finaldata[x+3] = 0x00
    # finaldata[x+4] = 0x00
    # f = open('testfinal.smc', 'w+b')
    # f.write(finaldata)
    # f.close()

    # ui.createLevelEditorWidgets(imageDict.get('imgBankTk0'), imageDict.get('imgBankTk1'), imageDict.get('levelImgTk'))
    
    # x = 0
    # y = 0
    # levelpointer = 0x1000
    # while (levelpointer < 0x3000):
        # for y in range(0,512,8):
            # for x in range(0,512,8):
                # tile = leveldata[levelpointer]
                # prop = leveldata[levelpointer+1]
                # levelpointer += 2
                # bank = ((prop & AND_TILE_BANK) >> AND_TILE_BANK_SHIFT)
                # hflip = ((prop & AND_TILE_HFLIP) >> AND_TILE_HFLIP_SHIFT)
                # vflip = ((prop & AND_TILE_VFLIP) >> AND_TILE_VFLIP_SHIFT)
                # img = imageDict.get('imgTile_' + str(tile+bank*BANK_TILE_AMOUNT))
                # if ((hflip != 0) or (vflip != 0)):
                    # img = IE.createTransposedImage(img, hflip, vflip, 0)
                # ui.pasteOnLevelCanvas(IE.convertImageToTkPhotoImage(img), x, y)

    # ui.mainloop()
    

