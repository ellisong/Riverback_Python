class Color():
    red = 0
    green = 0
    blue = 0
    # False = 15bit,   True = 24bit
    _type = 0
    
    def __init__(self, red=0, green=0, blue=0, type=0):
        self.red = red
        self.green = green
        self.blue = blue
        self._type = type
        if self._type:
            self.assert24Bit()
        else:
            self.assert15Bit()
    
    def getRed(self):
        return self.red
        
    def getGreen(self):
        return self.green
    
    def getBlue(self):
        return self.blue
        
    def getType(self):
        return self._type
    
    def switchType(self):
        if self._type:
            #24-bit to 15-bit
            self.assert24Bit()
            self.blue = self.blue // 8
            self.green = self.green // 8
            self.red = self.red // 8
            self._type = False
        else:
            #15-bit to 24-bit
            self.assert15Bit()
            self.red *= 8
            self.red += self.red // 32
            self.green *= 8
            self.green += self.green // 32
            self.blue *= 8
            self.blue += self.blue // 32
            self._type = True
    
    def get15BitColor(self):
        if self._type:
            #24-bit to 15-bit
            self.assert24Bit()
            B = self.blue // 8
            G = self.green // 8
            R = self.red // 8
            return B*1024 + G*32 + R
        else:
            self.assert15Bit()
            return self.blue*1024 + self.green*32 + self.red
    
    def get24BitColor(self):
        if self._type:
            self.assert24Bit()
            return self.red*0x010000 + self.green*0x0100 + self.blue
        else:
            #15-bit to 24-bit
            self.assert15Bit()
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
            
    def assert15Bit(self):
        assert((self.red >= 0) and (self.red < 32))
        assert((self.green >= 0) and (self.green < 32))
        assert((self.blue >= 0) and (self.blue < 32))
        pass
    
    def assert24Bit(self):
        assert((self.red >= 0) and (self.red < 256))
        assert((self.green >= 0) and (self.green < 256))
        assert((self.blue >= 0) and (self.blue < 256))
        pass
