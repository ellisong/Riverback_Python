import time

class DataCompressor():
    def compress(data):
        compressedData = bytearray()
        pointer = 0
        posByteList = []
        posBitList = []
        while (pointer < len(data)):
            behind = []
            front = []
            lengthCandidates = []
            lengthResults = []
            if (len(posBitList) >= 8):
                posByteList.append(DataCompressor.bitsIntoByte(posBitList))
                posBitList.clear()
            
            for pos in range(0, 16):
                if (pointer-pos-1 >= 0):
                    behind.insert(0, data[pointer-pos-1])
                else:
                    behind.insert(0, 0)
                    break
            
            for pos in range(0, 16):
                if (pointer+pos < len(data)):
                    front.append(data[pointer+pos])
                    indexList = DataCompressor.checkForSublistInList(behind, front)
                    if indexList:
                        lengthCandidates.append((pos+1, len(behind) - indexList[0]))
            
            if lengthCandidates:
                for frontLength, behindLength in lengthCandidates:
                    frontLengthCandidate = frontLength
                    frontCandidate = front[:frontLengthCandidate]
                    behindCandidate = behind[len(behind)-behindLength:]
                    while (frontLengthCandidate < 0x10000):
                        if (pointer+frontLengthCandidate >= len(data)):
                            break
                        frontCandidate.append(data[pointer+frontLengthCandidate])
                        if (DataCompressor.checkListRepetitionFromSublist(frontCandidate, behindCandidate)):
                            frontLengthCandidate += 1
                        else:
                            break
                    lengthResults.append((frontLengthCandidate, behindLength))
                
                lengthResults.sort(key=lambda result: result[0], reverse=True)
                frontLength = (lengthResults[0])[0]
                behindLength = (lengthResults[0])[1]
                if (frontLength <= 16):
                    lengthResults.sort(key=lambda result: 100000*result[0]-result[1], reverse=True)
                    frontLength = (lengthResults[0])[0]
                    behindLength = (lengthResults[0])[1]
                else:
                    lengthResults.sort(key=lambda result: 100000*result[0]+result[1], reverse=True)
                    frontLength = (lengthResults[0])[0]
                    behindLength = (lengthResults[0])[1]
                
                if (frontLength > 256):
                    posBitList.append(1)
                    compressedByte = 0
                    compressedByte += 0x10 - behindLength
                    compressedData.append(compressedByte)
                    compressedData.append(0)
                    compressedData.append(frontLength-1 & 0x00FF)
                    compressedData.append((frontLength-1)//256)
                    pointer += frontLength
                elif (frontLength > 16):
                    posBitList.append(1)
                    compressedByte = 0
                    compressedByte += 0x10 - behindLength
                    compressedData.append(compressedByte)
                    compressedData.append(frontLength-1)
                    pointer += frontLength
                elif (frontLength > 1):
                    posBitList.append(1)
                    compressedByte = 0
                    compressedByte += 0x10 - behindLength
                    compressedByte += ((frontLength-1 & 0x000F) << 4)
                    compressedData.append(compressedByte)
                    pointer += frontLength
                else:
                    posBitList.append(0)
                    compressedData.append(data[pointer])
                    pointer += 1
            else:
                posBitList.append(0)
                compressedData.append(data[pointer])
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
    
    def decompress(data, address=0):
        assert(address >= 0)
        assert(address < len(data))
        pointer = address
        writtenData = bytearray()
        for xx in range(0,16):
            writtenData.append(0)
        endCondition = False
        
        while (not endCondition):
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
                    if (endCondition):
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
                                endCondition = True
                                break
                            totalBytes = 256*data[pointer+1] + data[pointer] + 1
                            pointer += 2
                    xx = 0
                    while (xx < totalBytes):
                        for yy in behindBuffer:
                            writtenData.append(yy)
                            if (endCondition):
                                xx = totalBytes
                            xx += 1
                            if (xx >= totalBytes):
                                break
        del writtenData[:16]
        return writtenData
    
    def insertPosBytesIntoData(data, posByteList):
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
                        if (data[pointer] == 0):
                            pointer += 1
                            if ((data[pointer] == 0) and (data[pointer+1] == 0)):
                                return data
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
    
    def checkListRepetitionFromSublist(list_, sublist):
        for xx in range(0, len(list_)):
            if (list_[xx] != sublist[xx % len(sublist)]):
                return False
        return True
        
    def checkForSublistInList(list_, sublist):
        indexList = []
        for xx in range(len(list_) - len(sublist), -1, -1):
            count = 0
            for yy in range(0, len(sublist)):
                if (list_[xx+yy] == sublist[yy]):
                    count += 1
                else:
                    break
            if (count == len(sublist)):
                indexList.append(xx)
        indexList.sort(reverse=True)
        return indexList
    
    def convertSnesPointer(bank, pointer):
        return ((bank - 0x80)*0x8000) + (pointer - 0x8000)
    
    def readSnesPointer(data, offset):
        assert(offset+2 < len(data))
        bank = data[offset+2]
        pointer = data[offset+1]*0x100
        pointer += data[offset]
        return DataCompressor.convertSnesPointer(bank, pointer)