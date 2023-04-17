import cv2
import numpy as np
from math import sqrt, ceil

class ObjectAndImage:
    @staticmethod
    def objectToImage(object, imageName='temp'):
        '''converts object(currently text only) to its corresponding black and white image'''
        if not object:
            object = 'Nice try'

        bits = ObjectAndImage.objectToBinary(object)
        objectMatrix = ObjectAndImage.bitsToMatrix(bits)
        ObjectAndImage.saveMatrixAsImage(objectMatrix, imageName)


    @staticmethod
    def objectToBinary(string):
        '''Converts string to its corresponding binary digits'''
        res = ''.join(format(ord(i), '08b') for i in string)
        return res
    
    @staticmethod
    def bitsToMatrix(bits):
        '''converts bits to nearest higher square matrix'''
        totalLength = len(bits)
        n = int(ceil(sqrt(totalLength)))
        mat = np.zeros((n, n), dtype = np.uint8)

        pointer = 0

        for i in range(n):
            for j in range(n):
                if pointer>=totalLength:
                    mat[i][j] = 0
                else:
                    mat[i][j] = int(bits[pointer])
                    pointer = pointer+1
        return mat

    @staticmethod
    def saveMatrixAsImage(mat, imageName):
        '''converts matrix to correct color image matrix and saves the corresponding image'''
        img = mat*255   #1->255 for white in image
        path = 'D:/VSStudio/WebImage/static/'
        cv2.imwrite(f'{path + imageName}.png', img) 


    #******************decode******************#

    @staticmethod
    def imageToObjectLoad(imageName):
        '''converts image to its respective object form(currently text only)'''
        #load image as black and white [0-255] numpy array
        imgArray = cv2.imread(imageName, 0)
        #convert numpyarray -> list -> bits
        bits = ObjectAndImage.arrayToBits(imgArray)
        #convert bits -> ascii
        return ObjectAndImage.bitsToObject(bits)

    @staticmethod
    def arrayToBits(imgArray):
        '''converts image to its corresponding matrix and finally bits'''
        imgList = imgArray.tolist()
        bits = ''

        for list in imgList:
            for element in list:
                if element == 0:
                    bits += '0'
                else:
                    bits += '1'

        return bits

    @staticmethod
    def bitsToObject(bits):
        '''converts binary digits to corresponding object(currently text)'''
        n = len(bits)//8
        object = ''

        for _ in range(n):
            section = bits[:8]
            character = chr(int(section,2))
            if character == '\00':
                return object
            object += character
            bits = bits[8:]

        return object
    
    #******************convert image directly from web******************#

    @staticmethod
    def imageToObjectWeb(input):
        '''Converts image to object directly without storing the uploaded file'''
        #input is <FileStorage: 'webTest.png' ('image/png')> type
        imgArray = ObjectAndImage.webToArray(input)
        #convert numpyarray -> list -> bits
        bits = ObjectAndImage.arrayToBits(imgArray)
        #convert bits -> ascii
        return ObjectAndImage.bitsToObject(bits)

    @staticmethod
    def webToArray(input):
        '''Converts image uploaded directly to cv2 format without storing'''
        return cv2.imdecode(np.fromstring(input, np.uint8), cv2.IMREAD_UNCHANGED)


# if __name__ == "__main__":
#     t_o = ObjectAndImage
#     t_o.objectToImage('Enter your text here', 'tempImage')
#     print(t_o.imageToObject('webTest.png')) 
    