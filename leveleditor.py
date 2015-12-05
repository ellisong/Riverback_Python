from datacompressor import DataCompressor
from imageeditor import ImageEditor
from graphicbank import GraphicBank
from level import LevelHeader, Level

class LevelEditor():
    TILE_WIDTH = 8
    TILE_HEIGHT = 8
    EDITORTILESET_WIDTH = 16 * TILE_WIDTH
    EDITORTILESET_HEIGHT = 64 * TILE_HEIGHT
    EDITORCANVAS_WIDTH = 64 * TILE_WIDTH
    EDITORCANVAS_HEIGHT = 64 * TILE_HEIGHT
    GRAPHICS_BANK_HEADER_ADDRESS = 0x02E80
    BANK_AMOUNT = 7
    DEFAULT_BANK_PALETTE = 15
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
    
    def __init__(self):
        self.levelHeader = None
        self.level = None
        self.levelBank = None
        self.banks = []
    
    def openLevel(self, romdata, levelNumber):
        self.levelHeader = LevelHeader(levelNumber)
        self.levelHeader.update(romdata)
        levelData = DataCompressor.decompress(romdata, self.levelHeader.levelPointer)
        self.level = Level(self.levelHeader)
        self.level.update(levelData)
    
    def updateGraphicsBanks(self, romdata):
        self.banks = []
        bankAddresses = []
        for bankNum in range(0, self.BANK_AMOUNT):
            bankPointer = self.GRAPHICS_BANK_HEADER_ADDRESS + (bankNum * 8)
            bankAddresses.append(DataCompressor.readSnesPointer(romdata, bankPointer))
            bankAddresses.append(DataCompressor.readSnesPointer(romdata, bankPointer + 3))
        for bankNum in range(0, self.BANK_AMOUNT*2):
            bankData = DataCompressor.decompress(romdata, bankAddresses[bankNum])
            hasPalettes = True
            if (bankNum % 2):
                hasPalettes = False
            bank = GraphicBank(bankData, hasPalettes)
            if not hasPalettes:
                bank.setPalettes(self.banks[bankNum-1].getPalettes())
            bank.updateImage(self.DEFAULT_BANK_PALETTE)
            self.banks.append(bank)
    
    def updateLevelBank(self):
        assert(self.levelHeader.graphicsBankIndex < self.BANK_AMOUNT)
        index = self.levelHeader.graphicsBankIndex * 2
        levelBankData, offset = self.banks[index].getPlanarTilesFromBankData(self.level.tileIndex, 0)
        levelBankData.extend((self.banks[index+1].getPlanarTilesFromBankData(self.level.tileIndex, offset))[0])
        #tileOffset = self.banks[index].calculateTileOffset(self.level.tileIndex, 0)
        self.levelBank = GraphicBank(levelBankData, False)
        self.levelBank.tileAmount = self.level.tileIndexAmount
        self.levelBank.setPalettes(self.banks[index].getPalettes())
        self.levelBank.updateImage(self.DEFAULT_BANK_PALETTE)
    
    def updateEditorCanvasImage(self, ui):
        x = 0
        y = 0
        levelPointer = 0
        while (levelPointer < self.level.LEVEL_TILE_AMOUNT):
            for y in range(0, self.EDITORCANVAS_WIDTH, self.TILE_WIDTH):
                for x in range(0, self.EDITORCANVAS_HEIGHT, self.TILE_HEIGHT):
                    tile = self.level.tilemap[levelPointer]
                    prop = self.level.tilemap[levelPointer+1]
                    levelPointer += 2
                    
                    vflip = ((prop & self.AND_TILE_VFLIP) >> self.AND_TILE_VFLIP_SHIFT)
                    hflip = ((prop & self.AND_TILE_HFLIP) >> self.AND_TILE_HFLIP_SHIFT)
                    priority = ((prop & self.AND_TILE_PRIORITY) >> self.AND_TILE_PRIORITY_SHIFT)
                    palette = ((prop & self.AND_TILE_PALETTE) >> self.AND_TILE_PALETTE_SHIFT)
                    bank = ((prop & self.AND_TILE_BANK) >> self.AND_TILE_BANK_SHIFT)
                    tileImg = self.levelBank.getTileImage(tile + (bank * 256), self.level.paletteIndex[palette] - 1)
                    if hflip or vflip:
                        tileImg = ImageEditor.createTransposedImage(tileImg, hflip, vflip, 0)
                    ui.pasteOnLevelCanvas(ImageEditor.convertImageToTkPhotoImage(tileImg), x, y)