from PIL import Image, ImageTk
import xml.etree.ElementTree
from imageeditor import ImageEditor
from palette import Palette
from imageeditor import ImageEditor
from palette import Palette
from color import Color

class GraphicBank():
    tileWidth = 0
    tileHeight = 0
    tileAmount = 0
    paletteAmount = 0
    paletteColorAmount = 0
    bankHasPalettes = True
    
    data = []
    image = None
    
    def __init__(self, treeRoot=None, data=None):
        if treeRoot is not None:
            self.readConfig(treeRoot)
        self.data = data
        self.createImage()
    
    def readConfig(self, treeRoot):
        self.tileWidth = int(treeRoot.find('tile/width').text)
        self.tileHeight = int(treeRoot.find('tile/height').text)
        self.tileAmount = int(treeRoot.find('bank/tileamount').text)
        self.paletteAmount = int(treeRoot.find('bank/paletteamount').text)
        self.paletteColorAmount = int(treeRoot.find('palette/coloramount').text)
    
    def setBankHasPalettes(val):
        self.bankHasPalettes = val
    
    def getData(self):
        return self.data
    
    def getImage(self):
        return self.image
    
    def createImage(self):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert(self.tileAmount > 0)
        self.image = Image.new('RGB', (self.tileWidth*self.tileAmount, self.tileHeight))
    
    def updateImage(self, palette):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        for tileNumber in range(0, self.tileAmount):
            self.drawTileOnImage(tileNumber, palette)
        
    def drawTileOnImage(self, tileNumber, palette):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        tileimg = self.getTileImage(tileNumber, palette)
        self.image.paste(tileimg, (self.tileWidth*tileNumber, 0))
    
    def getTileImage(self, tileNumber, palette):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        planarTileData = self.getPlanarTileFromBankData(tileNumber)
        linearTileData = ImageEditor.convertPlanarTileToLinearTile(planarTileData)
        coloredTileData = ImageEditor.colorLinearTileWithPalette(linearTileData, palette)
        return ImageEditor.createImageFromColoredLinearTile(coloredTileData, self.tileWidth, self.tileHeight)
    
    def getPlanarTileFromBankData(self, tileNumber):
        assert(len(self.data) > 0)
        assert(tileNumber >= 0)
        offset = 0
        if self.bankHasPalettes:
            offset = 0x1E0
        offset += tileNumber * 0x20
        return self.data[offset:offset+0x20]
    
    def getPalettesFromBankData(self):
        assert(self.paletteColorAmount > 0)
        assert(self.paletteAmount > 0)
        paletteList = []
        pointer = 0
        for palNum in range(0, self.paletteAmount):
            pal = Palette(False)
            for colorNum in range(0, self.paletteColorAmount):
                B = ((self.data[pointer+1] & 0b01111100) >> 2)
                G = (((self.data[pointer+1] & 0b00000011) << 3) + ((self.data[pointer] & 0b11100000) >> 5))
                R = self.data[pointer] & 0b00011111
                pal.append(Color(red=R, green=G, blue=B, type=False))
                pointer += 2
            pal.switchType()
            paletteList.append(pal)
        return paletteList 