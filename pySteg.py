from PIL import Image, ImageMath;
import numpy;

import sys;

#read in message
messageFile = open("message.txt", "r");
message = messageFile.read();
    
#get the source image
sourceImage = Image.open("source.png");
userSpaceImg = sourceImage.copy();

pixels = list(userSpaceImg.getdata());

"""
via XOR writes the size of the message to the first 32 bytes(pixels)
then writes the message bits to the lsb needed bytes(pixels)
"""
def doSteg():
    

    if(len(pixels) * 3 < len(message) * 8):
        print "Image is not large enough";
        print "\tImage size: bytes", len(pixels) * 3;
        print "\tMessage size:(bits)", len(message) * 8;
        return;
    else:
        print "Hiding message...";
        print message, "length = " + str(len(message));
        print "\tImage size: bytes", len(pixels) * 3;
        print "\tMessage size:(bits)", len(message) * 8;
        
    #hide the size of the message in the first 32 bits
    HideTextSize(len(message));

    #hide the message in the remaining bits of the message
    HideText(message);

    for i in range((32/3) + 1):
        print pixels[i];


    stegPic = Image.new(sourceImage.mode, sourceImage.size);
    stegPic.putdata(pixels);

    stegPic.save("dest.png");
    
    
    

def getBits(letter):
    bits = [];
    for i in range( 7, -1, -1):
        bits.append((letter >> i) & 1);
    return bits;

def getIntBits(num):
    bits = [];
    for i in range( 31, -1, -1):
        bits.append((num >> i) & 1);
    return bits;

def HideText(message):
    pixIdx = 10;
    tupIdx = 2;
    for letter in message:
        #convert to letter to number and then to bits
        bits = getBits(ord(letter));
        #turn first tuple accessed into a list
        temp = list(pixels[pixIdx]);
        #loop over bits and alter each pixels lsb.
        for bit in bits:
            #set the last bit of temp[idx] to zero, then set it to value of bit 
            temp[tupIdx] = ((temp[tupIdx] & 0xfe) | bit);
            #update the tuple in pixels
            pixels[pixIdx] = tuple(temp);
            #inc tupIdx, then if mods 3 update pixIdx and get new tuple
            tupIdx = tupIdx + 1;
            if tupIdx % 3 == 0:
                tupIdx = 0;
                pixIdx = pixIdx + 1;
                temp = list(pixels[pixIdx]);
                
def HideTextSize(msgSize):
    pixIdx = 0;
    tupIdx = 0;
    #convert number to a 32 bits
    bits = getIntBits(msgSize);
    print bits;
    temp = list(pixels[pixIdx]);
    #loop over bits and alter each pixels lsb.
    for bit in bits:
        temp[tupIdx] = int((temp[tupIdx] & 0xfe) | bit); # mask and replace lsb 
        if bit == 1:
            print bit, tupIdx, temp;
        
        tupIdx = tupIdx + 1;
        if tupIdx % 3 == 0:
            tupIdx = 0;
            pixels[pixIdx] = tuple(temp);
            pixIdx = pixIdx + 1;
            temp = list(pixels[pixIdx]);
    pixels[pixIdx] = tuple(temp);

    
doSteg();
