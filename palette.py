class Palette():
    colors = []
    # 0 = 15bit,   1 = 24bit
    _type = 0
    
    def __init__(self, type=0):
        self._type = type
        
    def getType(self):
        return self._type
    
    def switchType(self):
        if (self._type == 0):
            #15-bit to 24-bit
            self._type  = 1
        else:
            #24-bit to 15-bit
            self._type = 0
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