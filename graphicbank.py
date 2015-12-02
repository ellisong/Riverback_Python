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
    editorTilesetWidth = 0
    editorTilesetHeight = 0
    bankHasPalettes = False
    
    data = []
    palettes = []
    image = None
    
    def __init__(self, treeRoot=None, data=None, hasPalettes=False):
        if treeRoot is not None:
            self.readConfig(treeRoot)
        self.data = data
        self.bankHasPalettes = hasPalettes
        if ((self.bankHasPalettes) and (data is not None)):
            self.palettes = self.getPalettesFromBankData()
        self.createImage()
    
    def readConfig(self, treeRoot):
        self.tileWidth = int(treeRoot.find('tile/width').text)
        self.tileHeight = int(treeRoot.find('tile/height').text)
        self.tileAmount = int(treeRoot.find('bank/tileamount').text)
        self.paletteAmount = int(treeRoot.find('bank/paletteamount').text)
        self.paletteColorAmount = int(treeRoot.find('palette/coloramount').text)
        self.editorTilesetWidth = int(treeRoot.find('editortileset/tileamount_width').text)
        self.editorTilesetHeight = int(treeRoot.find('editortileset/tileamount_height').text)
    
    def setBankHasPalettes(val):
        self.bankHasPalettes = val
    
    def setPalettes(self, palettes):
        self.palettes = palettes
        
    def getPalettes(self):
        return self.palettes
    
    def getPalette(self, index):
        return self.palettes[index]
    
    def appendData(self, data):
        this.data.append(data)
    
    def getData(self):
        return self.data
    
    def getImage(self):
        return self.image
    
    def createImage(self):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert(self.tileAmount > 0)
        self.image = Image.new('RGB', (self.editorTilesetWidth * self.tileWidth,
                                       self.editorTilesetHeight * self.tileHeight))
    
    def updateImage(self, paletteIndex):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        for tileNumber in range(0, self.tileAmount):
            self.drawTileOnImage(tileNumber, paletteIndex)
        
    def drawTileOnImage(self, tileNumber, paletteIndex):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        tileimg = self.getTileImage(tileNumber, paletteIndex)
        self.image.paste(tileimg, (self.tileWidth * (tileNumber % self.editorTilesetWidth), 
                                   self.tileHeight * (tileNumber // self.editorTilesetWidth)))
    
    def getTileImage(self, tileNumber, paletteIndex):
        assert(self.tileWidth > 0)
        assert(self.tileHeight > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        planarTileData = self.getPlanarTileFromBankData(tileNumber)
        linearTileData = ImageEditor.convertPlanarTileToLinearTile(planarTileData)
        coloredTileData = ImageEditor.colorLinearTileWithPalette(linearTileData, self.getPalette(paletteIndex))
        return ImageEditor.createImageFromColoredLinearTile(coloredTileData, self.tileWidth, self.tileHeight)
    
    def getPlanarTileFromBankData(self, tileNumber):
        assert(len(self.data) > 0)
        assert(tileNumber >= 0)
        offset = 0
        if self.bankHasPalettes is True:
            offset = 0x1E0
        offset += tileNumber * 0x20
        return self.data[offset:offset+0x20]
    
    def getPlanarTilesFromBankData(self, bitList, offset=0):
        tiles = []
        tileNumber = 0
        for xx in range(0, self.tileAmount):
            if ((offset+xx) > len(bitList)):
                break
            bit = bitList[offset+xx]
            if (bit == 1):
                tile = self.getPlanarTileFromBankData(tileNumber)
                for yy in tile:
                    tiles.append(yy)
            tileNumber += 1
        return (tiles, tileNumber)
    
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
        self.palettes = paletteList
        return self.palettes
    
    def calculateTileOffset(self, bitList, offset=0):
        tileOffset = 0
        for xx in range(0, self.tileAmount):
            if ((offset+xx) > len(bitList)):
                break
            bit = bitList[offset+xx]
            if (bit == 1):
                tileOffset += 1
        return tileOffset