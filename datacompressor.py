import time

class DataCompressor():
    # returns 
    def decompress(data, address, numBytes=10000, endCondition=True):
        if ((data is None) or (address > len(data)) or (numBytes < 1)):
            return
        assert(address >= 0)
        assert(address + numBytes < len(data))
        
        pointer = address
        writtenData = bytearray()
        for xx in range(0,16):
            writtenData.append(0)
        tilesWritten = 0
        
        while (tilesWritten < numBytes):
            currByte = data[pointer]
            
            pointer += 1
            posBitList = []
            andbyte = 0x80
            xx = 0
            for xx in range(0,8):
                posBit = currByte & andbyte
                if (posBit > 0):
                    posBit = 1
                andbyte = andbyte >> 1
                posBitList.append(posBit)
            for posBit in posBitList:
                currByte = data[pointer]
                pointer += 1
                if posBit == 0:
                    writtenData.append(currByte)
                    tilesWritten += 1
                    if (tilesWritten >= numBytes):
                        break
                else:
                    totalBytes = ((currByte & 0b11110000) >> 4) + 1
                    bytesBehind = 0b10000 - (currByte & 0b00001111)
                    behindBuffer = writtenData[len(writtenData)-bytesBehind:]
                    if totalBytes == 1:
                        totalBytes = data[pointer] + 1
                        pointer += 1
                        if ((totalBytes == 1) and (data[pointer+1] == 0) and (data[pointer+2] == 0)):
                            if endCondition:
                                tilesWritten = numBytes
                                break
                    xx = 0
                    yy = 0
                    while (xx < totalBytes):
                        for yy in behindBuffer:
                            writtenData.append(yy)
                            tilesWritten += 1
                            if (tilesWritten >= numBytes):
                                xx = totalBytes
                            xx += 1
                            if (xx >= totalBytes):
                                break
        del writtenData[:16]
        return writtenData
    
    def insertPosBytesIntoData(data, posBytesList):
        #pointer = 0
        #for x in range(0, len(posBytesList)):
        #    data.insert(pointer, 0)
        #    pointer += 9
        pointer = -1
        andbyte = 0x80
        posBitList = []
        for posByte in posBytesList:
            andbyte = 0x80
            pointer += 1
            data.insert(pointer, posByte)
            for xx in range(0,8):
                posBit = posByte & andbyte
                if (posBit > 0):
                    posBit = 1
                andbyte = andbyte >> 1
                posBitList.append(posBit)
            for posBit in posBitList:
                if (posBit == 1):
                   if ((data[pointer] & 0xF0) == 0):
                        pointer += 1
                pointer += 1
            del posBitList[:]
        return data
        