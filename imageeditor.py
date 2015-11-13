from PIL import Image, ImageTk

class ImageEditor():
    def getTileFromTileset(self, image, tileX, tileY, tileWidth, tileHeight):
        return image.crop((tileX*tileWidth, tileY*tileHeight, tileX*tileWidth+tileWidth, tileY*tileHeight+tileHeight))
    
    def getTilesListFromTileset(self, image, tileAmount, tileWidth, tileHeight):
        if ((tileWidth < 1) or (tileHeight < 1) or (tileAmount < 1) or (image is None)):
            return
        tiles = []
        x = 0
        y = 0
        for y in range(0, image.height // tileHeight):
            for x in range(0, image.width // tileWidth):
                if len(tiles) >= tileAmount:
                    return tiles
                tiles.append(self.getTileFromTileset(image, x, y, tileWidth, tileHeight))
        return tiles
    
    def createTransposedImage(self, image, horizontal, vertical, rotation):
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
    
    def createTransposedImagesFromList(self, imageList, horizontal, vertical, rotation):
        convertedList = []
        for img in imageList:
            convertedList.append(self.createTransposedImage(img, horizontal, vertical, rotation))
        return convertedList
    
    def convertImageToTkPhotoImage(self, image):
        return ImageTk.PhotoImage(image)
    
    def convertImagesToTkPhotoImage(self, imageList):
        convertedList = []
        for img in imageList:
            convertedList.append(self.convertImageToTkPhotoImage(img))
        return convertedList