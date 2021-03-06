from datacompressor import DataCompressor
from palette import Palette
from color import Color

class LevelHeader(): 
    LEVEL_HEADER_ADDRESS = 0xF298
    LEVEL_HEADER_SIZE = 37
    LEVEL_HEADER_AMOUNT = 64
    
    def __init__(self, levelNumber=0):
        self.levelNumber = levelNumber
        self.levelHeaderAddress = self.LEVEL_HEADER_ADDRESS + (self.levelNumber * self.LEVEL_HEADER_SIZE)
        self.levelPointer = 0
        self.graphicsBankIndex = 0
        self.fieldNumber = 0
        self.musicSelect = 0
        self.enemyType = [0,0,0,0,0,0]
        self.waterHeight = 0
        self.waterType = 0
        self.levelTimer = 0
        self.doorExits = [0,0,0,0]
    
    def update(self, romdata):
        assert(self.levelHeaderAddress >= 0)
        assert(self.levelNumber >= 0)
        #level header amount might be changeable if some level data is moved around
        assert(self.levelNumber < self.LEVEL_HEADER_AMOUNT)
        self.levelPointer = DataCompressor.readSnesPointer(romdata, self.levelHeaderAddress)
        self.graphicsBankIndex = romdata[self.levelHeaderAddress + 0x03]
        self.fieldNumber = romdata[self.levelHeaderAddress + 0x04]
        self.musicSelect = romdata[self.levelHeaderAddress + 0x05]
        self.enemyType[0] = romdata[self.levelHeaderAddress + 0x06]
        self.enemyType[1] = romdata[self.levelHeaderAddress + 0x07]
        self.enemyType[2] = romdata[self.levelHeaderAddress + 0x08]
        self.enemyType[3] = romdata[self.levelHeaderAddress + 0x09]
        self.enemyType[4] = romdata[self.levelHeaderAddress + 0x0A]
        self.enemyType[5] = romdata[self.levelHeaderAddress + 0x0B]
        self.waterHeight = romdata[self.levelHeaderAddress + 0x1C]
        self.waterType = romdata[self.levelHeaderAddress + 0x1D]
        self.levelTimer = DataCompressor.readSnesPointer(romdata, self.levelHeaderAddress + 0x1F)
        self.doorExits[0] = romdata[self.levelHeaderAddress + 0x21]
        self.doorExits[1] = romdata[self.levelHeaderAddress + 0x22]
        self.doorExits[2] = romdata[self.levelHeaderAddress + 0x23]
        self.doorExits[3] = romdata[self.levelHeaderAddress + 0x24]

class Level():
    LEVEL_TILE_AMOUNT = 4096
    LEVEL_TILE_INDEX_SIZE = 256
    LEVEL_PALETTE_INDEX_AMOUNT = 6
    
    def __init__(self, levelHeader=None):
        self.levelHeader = levelHeader
        self.physmap = []
        self.tilemap = []
        self.tileIndexAmount = 0
        self.tileIndex = []
        self.paletteIndex = []
    
    def update(self, leveldata):
        self.setPhysmap(leveldata)
        self.setTilemap(leveldata)
        self.setTileIndexAmount(leveldata)
        self.setTileIndex(leveldata)
        self.setPaletteIndex(leveldata)
    
    def setPhysmap(self, leveldata):
        offset = 0
        self.physmap = leveldata[offset : (offset + self.LEVEL_TILE_AMOUNT)]
    
    def setTilemap(self, leveldata):
        offset = self.LEVEL_TILE_AMOUNT
        self.tilemap = leveldata[offset : (offset + self.LEVEL_TILE_AMOUNT * 2)]
    
    def setTileIndexAmount(self, leveldata):
        offset = (self.LEVEL_TILE_AMOUNT * 3)
        self.tileIndexAmount = leveldata[offset+1] * 0x100 + leveldata[offset]
    
    def setTileIndex(self, leveldata):
        offset = (self.LEVEL_TILE_AMOUNT * 3) + 2
        tileIndexBytes = leveldata[offset : offset + self.LEVEL_TILE_INDEX_SIZE]
        self.tileIndex = DataCompressor.byteListIntoBitList(tileIndexBytes, False)
    
    def setPaletteIndex(self, leveldata):
        offset = (self.LEVEL_TILE_AMOUNT * 3) + 2 + self.LEVEL_TILE_INDEX_SIZE
        self.paletteIndex = leveldata[offset : offset + self.LEVEL_PALETTE_INDEX_AMOUNT]
        self.paletteIndex.insert(0, 7)
        self.paletteIndex.insert(0, 8)
    