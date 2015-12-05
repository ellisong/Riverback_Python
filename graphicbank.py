from PIL import Image, ImageTk
from imageeditor import ImageEditor
from palette import Palette
from imageeditor import ImageEditor
from palette import Palette
from color import Color

class GraphicBank():
    TILE_WIDTH = 8
    TILE_HEIGHT = 8
    PALETTE_AMOUNT = 15
    PALETTE_COLOR_AMOUNT = 16
    EDITOR_TILESET_WIDTH = 16
    EDITOR_TILESET_HEIGHT = 64
    
    COLORS_HARDCODED_1 = [Color(25, 33, 16, True), Color(33, 41, 25, True), 
                          Color(41, 49, 33, True), Color(49, 58, 41, True), 
                          Color(58, 66, 49, True), Color(66, 74, 58, True), 
                          Color(74, 82, 66, True), Color(82, 90, 74, True),
                          Color(90, 99, 82, True), Color(99, 107, 90, True), 
                          Color(107, 115, 99, True), Color(115, 123, 107, True),
                          Color(123, 132, 115, True), Color(132, 140, 123, True), 
                          Color(140, 148, 132, True), Color(148, 156, 140, True)]
    
    COLORS_HARDCODED_2 = [Color(66, 99, 0, True), Color(49, 49, 82, True), 
                          Color(239, 230, 255, True), Color(214, 156, 255, True),
                          Color(66, 99, 0, True), Color(82, 49, 49, True), 
                          Color(255, 107, 140, True), Color(255, 49, 107, True),
                          Color(66, 99, 0, True), Color(49, 74, 49, True), 
                          Color(230, 255, 132, True), Color(189, 255, 0, True),
                          Color(66, 99, 0, True), Color(214, 82, 148, True), 
                          Color(255, 148, 206, True), Color(247, 230, 255, True)]
    
    def __init__(self, data=[], hasPalettes=False):
        self.data = data
        self.bankHasPalettes = hasPalettes
        self.palettes = None
        if ((self.bankHasPalettes) and (data is not None)):
            self.palettes = self.getPalettesFromBankData()
            # two hardcoded palettes, not sure where they are in ROM yet 
            # or why they are part of tilemap's palette selection
            hardcodedPalette1 = Palette(True)
            hardcodedPalette2 = Palette(True)
            for x in range(0, self.PALETTE_COLOR_AMOUNT):
                hardcodedPalette1.append(self.COLORS_HARDCODED_1[x])
                hardcodedPalette2.append(self.COLORS_HARDCODED_2[x])
            self.palettes.append(hardcodedPalette1)
            self.palettes.append(hardcodedPalette2)
        self.image = None
        self.tileAmount = 1024
        self.createImage()
    
    def setBankHasPalettes(val):
        self.bankHasPalettes = val
    
    def setPalettes(self, palettes):
        self.palettes = palettes
        #quick hack to change color 0 to be consistent across palettes (for transparency reasons)
        for pal in self.palettes:
            pal.getColors()[0].red = 96
            pal.getColors()[0].green = 96
            pal.getColors()[0].blue = 96
        
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
        assert(self.TILE_WIDTH > 0)
        assert(self.TILE_HEIGHT > 0)
        assert(self.tileAmount > 0)
        self.image = Image.new('RGB', (self.EDITOR_TILESET_WIDTH * self.TILE_WIDTH,
                                       self.EDITOR_TILESET_HEIGHT * self.TILE_HEIGHT))
    
    def updateImage(self, paletteIndex):
        assert(self.TILE_WIDTH > 0)
        assert(self.TILE_HEIGHT > 0)
        for tileNumber in range(0, self.tileAmount):
            self.drawTileOnImage(tileNumber, paletteIndex)
        
    def drawTileOnImage(self, tileNumber, paletteIndex):
        assert(self.TILE_WIDTH > 0)
        assert(self.TILE_HEIGHT > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        tileimg = self.getTileImage(tileNumber, paletteIndex)
        self.image.paste(tileimg, (self.TILE_WIDTH * (tileNumber % self.EDITOR_TILESET_WIDTH), 
                                   self.TILE_HEIGHT * (tileNumber // self.EDITOR_TILESET_WIDTH)))
    
    def getTileImage(self, tileNumber, paletteIndex):
        assert(self.TILE_WIDTH > 0)
        assert(self.TILE_HEIGHT > 0)
        assert((tileNumber >= 0) and (tileNumber < self.tileAmount))
        planarTileData = self.getPlanarTileFromBankData(tileNumber)
        linearTileData = ImageEditor.convertPlanarTileToLinearTile(planarTileData)
        coloredTileData = ImageEditor.colorLinearTileWithPalette(linearTileData, self.getPalette(paletteIndex))
        return ImageEditor.createImageFromColoredLinearTile(coloredTileData, self.TILE_WIDTH, self.TILE_HEIGHT)
    
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
        assert(self.PALETTE_COLOR_AMOUNT > 0)
        assert(self.PALETTE_AMOUNT > 0)
        paletteList = []
        pointer = 0
        for palNum in range(0, self.PALETTE_AMOUNT):
            pal = Palette(False)
            for colorNum in range(0, self.PALETTE_COLOR_AMOUNT):
                B = ((self.data[pointer+1] & 0b01111100) >> 2)
                G = (((self.data[pointer+1] & 0b00000011) << 3) + ((self.data[pointer] & 0b11100000) >> 5))
                R = self.data[pointer] & 0b00011111
                pal.append(Color(red=R, green=G, blue=B, type=False))
                pointer += 2
            pal.switchType()
            paletteList.append(pal)
        self.setPalettes(paletteList)
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