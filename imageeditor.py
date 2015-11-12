from PIL import Image, ImageTk

class ImageEditor():
    def convertToTkImage(image):
        if image:
            return ImageTk.PhotoImage(image)
        return None
    
    def getTilesListFromTileset(image, tileAmount, tileWidth, tileHeight):
        if ((tileWidth < 1) or (tileHeight < 1) or (tileAmount < 1) or (image is None)):
            return None
        tiles = []
        x = 0
        y = 0
        for y in range(0, image.height, tileHeight):
            for x in range(0, image.width, tileWidth):
                if len(tiles) >= tileAmount:
                    return tiles
                tiles.append(image.crop((x, y, x+tileWidth, y+tileHeight)))
        return tiles