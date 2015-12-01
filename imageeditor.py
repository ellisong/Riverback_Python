from PIL import Image, ImageTk

class ImageEditor():
    def getTileFromTileset(image, tileX, tileY, tileWidth, tileHeight):
        assert(tileX >= 0)
        assert(tileY >= 0)
        assert(tileWidth >= 1)
        assert(tileHeight >= 1)
        return image.crop((tileX*tileWidth, tileY*tileHeight, tileX*tileWidth+tileWidth, tileY*tileHeight+tileHeight))
    
    def getTilesListFromTileset(image, tileAmount, tileWidth, tileHeight):
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
                tiles.append(ImageEditor.getTileFromTileset(image, x, y, tileWidth, tileHeight))
        return tiles
    
    def createTransposedImage(image, horizontal, vertical, rotation):
        img = image
        if horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if rotation == 90:
            img = img.transpose(Image.ROTATE_90)
        elif rotation == 180:
            img = img.transpose(Image.ROTATE_180)
        elif rotation == 270:
            img = img.transpose(Image.ROTATE_270)
        return img
    
    def createTransposedImagesFromList(imageList, horizontal, vertical, rotation):
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