class Color():
    red = 0
    green = 0
    blue = 0
    # 0 = 15bit,   1 = 24bit
    _type = 0
    
    def __init__(self, red=0, green=0, blue=0, type=0):
        self.red = red
        self.green = green
        self.blue = blue
        self._type = type
        
    def getType(self):
        return self._type
    
    def switchType(self):
        if (self._type == 0):
            #15-bit to 24-bit
            self.red *= 8
            self.red += self.red // 32
            self.green *= 8
            self.green += self.green // 32
            self.blue *= 8
            self.blue += self.blue // 32
            self._type  = 1
        else:
            #24-bit to 15-bit
            self.blue = self.blue // 8
            self.green = self.green // 8
            self.red = self.red // 8
            self._type = 0
    
    def get15BitColor(self):
        if (self._type == 0):
            return self.blue*1024 + self.green*32 + self.red
        else:
            #24-bit to 15-bit
            B = self.blue // 8
            G = self.green // 8
            R = self.red // 8
            return B*1024 + G*32 + R
    
    def get24BitColor(self):
        if (self._type == 1):
            return self.red*0x010000 + self.green*0x0100 + self.blue
        else:
            #15-bit to 24-bit
            R = self.red
            R *= 8
            R += R // 32
            G = self.green
            G *= 8
            G += G // 32
            B = self.blue
            B *= 8
            B += B // 32
            return R*0x010000 + G*0x0100 + B
