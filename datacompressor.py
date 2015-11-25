import time

class DataCompressor():
    def compress(data):
        compressedData = data[:]
        pointer = 0
        posByteList = []
        posBitList = []
        while (pointer < len(compressedData)):
            behind = []
            behindLength = 0
            front = []
            frontLength = 0
            #if the length is > 8, let the assert in the method throw an error because it should never happen
            if (len(posBitList) >= 8):
                posByteList.append(DataCompressor.bitsIntoByte(posBitList))
                posBitList.clear()
            for pos in range(0, 16):
                if (pointer-pos-1 >= 0):
                    behind.insert(0, compressedData[pointer-pos-1])
                else:
                    behind.insert(0, 0)
                if (pointer+pos < len(compressedData)):
                    front.append(compressedData[pointer+pos])
                if (front == behind):
                    frontLength = pos+1
                    behindLength = pos+1
            if (behindLength >= 1):
                front = front[:frontLength]
                behind = behind[len(behind)-behindLength:len(behind)]
                if (behind.count(behind[0]) == len(behind)):
                    behindLength = 1
                behindExpanded = []
                while (len(behindExpanded) < 0x100):
                    for x in range(0, behindLength):
                        behindExpanded.append(behind[x])
                while (frontLength < 0x100):
                    if (pointer+frontLength >= len(compressedData)):
                        break
                    front.append(compressedData[pointer+frontLength])
                    if (front == behindExpanded[0:frontLength+1]):
                        frontLength += 1
                    else:
                        break
                if (frontLength > 16):
                    posBitList.append(1)
                    del compressedData[pointer:pointer+frontLength]
                    compressedData.insert(pointer, frontLength)
                    pointer += 1
                elif (frontLength > 1):
                    posBitList.append(1)
                    compressedbyte = 0
                    compressedbyte += 0x10 - behindLength
                    compressedbyte += ((frontLength-1 & 0x000F) << 4)
                    del compressedData[pointer:pointer+frontLength]
                    compressedData.insert(pointer, compressedbyte)
                    pointer += 1
                else:
                    posBitList.append(0)
                    pointer += 1
            else:
                posBitList.append(0)
                pointer += 1
        if (len(posBitList) == 8):
            posByteList.append(DataCompressor.bitsIntoByte(posBitList))
            posBitList.clear()
        posBitList.append(1)
        posByteList.append(DataCompressor.bitsIntoByte(posBitList))
        for x in range(0, 4):
            compressedData.append(0)
        DataCompressor.insertPosBytesIntoData(compressedData, posByteList)
        return compressedData
    
    def decompress(data, address):
        assert(address >= 0)
        #assert(address + numBytes < len(data))
        
        pointer = address
        writtenData = bytearray()
        for xx in range(0,16):
            writtenData.append(0)
        tilesWritten = 0
        
        while (tilesWritten < len(data)):
            currByte = data[pointer]
            pointer += 1
            posBitList = []
            andbyte = 0x80
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
                    if (tilesWritten >= len(data)):
                        break
                else:
                    totalBytes = ((currByte & 0b11110000) >> 4) + 1
                    bytesBehind = 0b10000 - (currByte & 0b00001111)
                    behindBuffer = writtenData[len(writtenData)-bytesBehind:]
                    if totalBytes == 1:
                        totalBytes = data[pointer] + 1
                        pointer += 1
                        if (totalBytes == 1):
                            if ((data[pointer] == 0) and (data[pointer+1] == 0)):
                                tilesWritten = len(data)
                                break
                    xx = 0
                    while (xx < totalBytes):
                        for yy in behindBuffer:
                            writtenData.append(yy)
                            tilesWritten += 1
                            if (tilesWritten >= len(data)):
                                xx = totalBytes
                            xx += 1
                            if (xx >= totalBytes):
                                break
        del writtenData[:16]
        return writtenData
    
    def insertPosBytesIntoData(data, posByteList):
        #pointer = 0
        #for x in range(0, len(posByteList)):
        #    data.insert(pointer, 0)
        #    pointer += 9
        pointer = 0
        andbyte = 0x80
        posBitList = []
        for posByte in posByteList:
            andbyte = 0x80
            data.insert(pointer, posByte)
            pointer += 1
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
    
    def bitsIntoByte(bitList):
        assert(len(bitList) <= 8)
        myByte = 0;
        for x in range(0, len(bitList)):
            if (bitList[x] == 1):
                myByte += 0x80 >> x
        return myByte
        