import os
import random

def hex_number( count, padded=False ):
    x = random.randint( 0, 16**count )
    hexdig = "%x" % x
    if padded:
        out = hexdig.zfill( count )
        return out
    else:
        return hexdig

def AESvectors( size, num, padded ):
    if (os.path.exists("inputFile.pt")):
        os.remove("inputFile.pt")

    f = open("inputFile.pt", "a")
    for i in range( num ):
        tempStr =  hex_number( size, padded )
        if len(tempStr) != 32:
            tempStr = tempStr + "0"*(32-len(tempStr))

        if i == num-1:
            f.write( tempStr )
        else:
            f.write( tempStr + "\n" )

    f.close()

AESvectors( size=32, num=100, padded=False )