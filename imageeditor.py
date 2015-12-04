from PIL import Image, ImageTk
import xml.etree.ElementTree
from math import pow
from palette import Palette
from color import Color

class ImageEditor():
    def getTileFromTileset(image, tileX, tileY, tileWidth, tileHeight):
        assert(tileX >= 0)
        assert(tileY >= 0)
        assert(tileWidth >= 1)
        assert(tileHeight >= 1)
        assert(tileX*tileWidth+tileWidth < image.width)
        assert(tileY*tileHeight+tileHeight < image.height)
        return image.crop((tileX*tileWidth, tileY*tileHeight, tileX*tileWidth+tileWidth, tileY*tileHeight+tileHeight))
    
    def getTilesListFromTileset(image, tileAmount, tileWidth, tileHeight):
        assert(image.width > 0)
        assert(image.height > 0)
        assert(tileWidth >= 1)
        assert(tileHeight >= 1)
        assert(tileAmount >= 1)
        tiles = []
        x = 0
        y = 0
        for y in range(0, image.height // tileHeight):
            for x in range(0, image.width // tileWidth):
                if len(tiles) >= tileAmount:
                    return tiles
                tiles.append(ImageEditor.getTileFromTileset(image, x, y))
        return tiles
    
    def convertPlanarTileToLinearTile(tiledata):
        assert(len(tiledata) >= 32)
        bitplane = []
        offset = 0
        for planeNum in range(0, 4):
            plane = bytearray()
            if (planeNum == 2):
                offset = 16
            for byte in range(0, 8):
                bitmask = 0x80
                for bit in range(0, 8):
                    bitValue = (tiledata[offset+(byte*2)] & bitmask)
                    if (bitValue > 0):
                        bitValue = 1
                    plane.append(bitValue * (0x01 << planeNum))
                    bitmask = bitmask >> 1
            bitplane.append(plane)
            offset += 1
        lineardata = bytearray()
        pix = 0
        for pixel in range(0, 64):
            if ((pixel % 2) == 0):
                pix = 0
            for planeNum in range(0, 4):
                pix += (bitplane[planeNum])[pixel]
            if ((pixel % 2) == 0):
                pix = pix << 4
            else:
                lineardata.append(pix)
        return lineardata
    
    def colorLinearTileWithPalette(tiledata, palette):
        assert(len(tiledata) >= 32)
        pointer = 0
        colors = []
        while (pointer < 32):
            tile = (tiledata[pointer] & 0xF0) >> 4
            colors.append(palette.getColors()[tile])
            tile = tiledata[pointer] & 0x0F
            colors.append(palette.getColors()[tile])
            pointer += 1
        return colors
    
    def createImageFromColoredLinearTile(tiledata, width, height):
        assert(width > 0)
        assert(height > 0)
        imagebytes = bytearray()
        for col in tiledata:
            imagebytes.append(col.getRed())
            imagebytes.append(col.getGreen())
            imagebytes.append(col.getBlue())
        return Image.frombytes('RGB', (width, height), bytes(imagebytes))
                
    def createTransposedImage(image, horizontal=False, vertical=False, rotation=0):
        img = image
        if horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if ((rotation % 360) == 90):
            img = img.transpose(Image.ROTATE_90)
        elif ((rotation % 360) == 180):
            img = img.transpose(Image.ROTATE_180)
        elif ((rotation % 360) == 270):
            img = img.transpose(Image.ROTATE_270)
        return img
    
    def createTransposedImagesFromList(imageList, horizontal=False, vertical=False, rotation=0):
        convertedList = []
        for img in imageList:
            convertedList.append(ImageEditor.createTransposedImage(img, horizontal, vertical, rotation))
        return convertedList
    
    def convertImageToTkPhotoImage(image):
        return ImageTk.PhotoImage(image)
    
    def convertImagesToTkPhotoImage(imageList):
        convertedList = []
        for img in imageList:
            convertedList.append(ImageEditor.convertImageToTkPhotoImage(img))
        return convertedList