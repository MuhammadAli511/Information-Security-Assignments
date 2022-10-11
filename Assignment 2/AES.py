mode = 128

rijndaelSbox = [
    ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
    ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
    ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
    ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
    ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
    ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
    ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
    ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
    ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
    ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
    ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
    ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
    ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
    ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
    ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
    ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']
]

sBoxMappingColumn = {"00": 0, "01": 1, "02": 2, "03": 3, "04": 4, "05": 5, "06": 6, "07": 7, "08": 8, "09": 9, "0a": 10, "0b": 11, "0c": 12, "0d": 13, "0e": 14, "0f": 15}
sBoxMappingRow = {"00": 0, "10": 1, "20": 2, "30": 3, "40": 4, "50": 5, "60": 6, "70": 7, "80": 8, "90": 9, "a0": 10, "b0": 11, "c0": 12, "d0": 13, "e0": 14, "f0": 15}

rcon = ['01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000', '80000000', '1b000000', '36000000']

def readingKey():
    f = open("testKeyFile.key", "r")
    key = f.read()
    f.close()
    return key

def createChunks(key):
    chunkList = []
    for i in range(0, len(key), 8):
        chunkList.append(key[i:i+8])
    return chunkList

def rotWord(word):
    word = word[2:] + word[:2]
    return word

def substitution(word):
    tempWord = ""
    for i in range(0, len(word), 2):
        row = word[i] + "0"
        column = "0" + word[i+1]
        tempWord += rijndaelSbox[sBoxMappingRow[row]][sBoxMappingColumn[column]]
    return tempWord

def keyValidation(key):
    if len(key) != 8:
        key = "0"*(8-len(key)) + key
    return key


def keyExpansion():
    counter = 0
    completeKey = readingKey()
    completeKey = completeKey.lower()
    wKeyList = createChunks(completeKey)
    initialKeyListSize = len(wKeyList)
    if mode == 128:
        rounds = 10
        dividend = 4

    for i in range(rounds):
        
        currentSize = len(wKeyList)

        # Step 1
        rotatedWord = rotWord(wKeyList[currentSize-1])

        # Step 2
        substitutedWord = substitution(rotatedWord)

        # Step 3

        rconWord = rcon[counter]
        counter+=1
        if counter == 10:
            counter = 0
        subXorRcon = hex(int(substitutedWord, 16) ^ int(rconWord, 16))[2:]
        initialValue = subXorRcon

        # Step 4
        value1 = hex(int(initialValue, 16) ^ int(wKeyList[currentSize-(dividend-0)], 16))[2:]
        value1 = keyValidation(value1)
        wKeyList.append(value1)

        # Step 5
        value2 = hex(int(value1, 16) ^ int(wKeyList[currentSize-(dividend-1)], 16))[2:]
        value2 = keyValidation(value2)
        wKeyList.append(value2)

        # Step 6
        value3 = hex(int(value2, 16) ^ int(wKeyList[currentSize-(dividend-2)], 16))[2:]
        value3 = keyValidation(value3)
        wKeyList.append(value3)

        # Step 7
        value4 = hex(int(value3, 16) ^ int(wKeyList[currentSize-(dividend-3)], 16))[2:]
        value4 = keyValidation(value4)
        wKeyList.append(value4)

    return wKeyList

def keySeperation(wKeyList1):
    tempKeyList = []
    for i in range(len(wKeyList1)):
        if mode == 128:
            if i % 4 == 0:
                tempKeyList.append(wKeyList1[i] + wKeyList1[i+1] + wKeyList1[i+2] + wKeyList1[i+3])
    return tempKeyList

wKeyList1 = keyExpansion()
completeKeyList = keySeperation(wKeyList1)

print(completeKeyList)