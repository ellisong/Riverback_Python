import color

class Palette():   
    def __init__(self, type=False):
        # False = 15bit,   True = 24bit
        self.__type = type
        self.colors = []
    
    def getColors(self):
        return self.colors
        
    def getType(self):
        return self.__type
    
    def append(self, color):
        self.colors.append(color)
    
    def switchType(self):
        if self.__type:
            #24-bit to 15-bit
            self.__type = False
        else:
            #15-bit to 24-bit
            self.__type = True
        for col in self.colors:
            col.switchType()
    
    def get15BitColors(self):
        colors15bit = []
        for x in self.colors:
            colors15bit.append(x.get15BitColor())
        return colors15bit
    
    def get24BitColors(self):
        colors24bit = []
        for x in self.colors:
            colors24bit.append(x.get24BitColor())
        return colors24bit
    
    def get15BitColorsAsValueList(self):
        valueList = []
        colors15bit = self.get15BitColors()
        for x in colors15bit:
            valueList.append((x & 0x00FF))
            valueList.append((x & 0xFF00) >> 8)
        return valueList