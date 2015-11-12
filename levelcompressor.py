import time

class LevelCompressor():
    # returns 
    def decompress(romdata, address, tileamount=4096):
        if ((romdata is None) or (address > len(romdata)) or (tileamount < 1)):
            return
        pointer = address
        leveldata = bytearray()
        for xx in range(0,16):
            leveldata.append(0)
        tilesWritten = 0
        
        while (tilesWritten < tileamount*3):
            currByte = romdata[pointer]
            pointer += 1
            lzByteList = []
            andbyte = 0x80
            xx = 0
            for xx in range(0,8):
                res = currByte & andbyte
                if (res > 0):
                    res = 1
                andbyte = andbyte >> 1
                lzByteList.append(res)
            for lzByte in lzByteList:
                currByte = romdata[pointer]
                pointer += 1
                if lzByte == 0:
                    leveldata.append(currByte)
                    tilesWritten += 1
                else:
                    # TODO: possibility: the bytes behind are uncompressed (leveldata[?])
                    totalBytes = ((currByte & 0b11110000) >> 4) + 1
                    bytesBehind = 0b10000 - (currByte & 0b00001111)
                    behindBuffer = leveldata[len(leveldata)-bytesBehind:]
                    if totalBytes == 1:
                        totalBytes = romdata[pointer] + 1
                        pointer += 1
                    xx = 0
                    yy = 0
                    while (xx < totalBytes):
                        for yy in behindBuffer:
                            leveldata.append(yy)
                            tilesWritten += 1
                            xx += 1
                            if (xx >= totalBytes):
                                break
        del leveldata[:16]
        return leveldata