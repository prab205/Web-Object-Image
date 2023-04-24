import cv2
import base64
import numpy as np
from math import sqrt, ceil

class ObjectAndImage:
    #******************encode******************#
    @staticmethod
    def objectToBase64(object):
        '''returns base64 encoded string of the image from the uploaded image'''
        if not object:
            object = 'prabin-paudel.com.np'

        bits = ObjectAndImage.objectToBinary(object)
        objectMatrix = ObjectAndImage.bitsToMatrix(bits)
        return ObjectAndImage.convertBase64(objectMatrix)
    
    @staticmethod
    def objectToBinary(string):
        '''Converts string to its corresponding binary digits'''
        return ''.join(format(ord(i), '08b') for i in string)
    
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
    def convertBase64(objectMatrix):
        '''converts matrix to its bytearray and then base64 encoded format for directly displaying the image'''
        img = objectMatrix*255
        _, arr = cv2.imencode('.png', img)
        baseString = base64.b64encode(arr)
        return str(baseString, 'utf-8')
    
    #****************** offline file ******************#
    @staticmethod
    def objectToImageSave(object, imageName='temp'):
        '''convert and save object(currently text only) to its corresponding black and white image'''
        if not object:
            object = 'prabin-paudel.com.np'

        bits = ObjectAndImage.objectToBinary(object)
        objectMatrix = ObjectAndImage.bitsToMatrix(bits)
        ObjectAndImage.saveMatrixAsImage(objectMatrix, imageName)
    
    @staticmethod
    def saveMatrixAsImage(mat, imageName):
        '''converts matrix to correct color image matrix and saves the corresponding image'''
        img = mat*255   #1->255 for white in image
        cv2.imwrite(f'{imageName}.png', img)


    #****************** decode ******************#
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
    
    #****************** offline ******************#
    @staticmethod
    def imageLoadToObject(imageName):
        '''load local image and decode to object form(currently text only). Include extension along with file name'''
        
        #take last 5 characters for checking file extension 
        check = imageName[-5:]
        if (check.find(r'.png') > -1):
            {}
        elif (check.find(r'.jpg') > -1) or (check.find(r'.jpeg') > -1):
            print("File format currently not supported")
            exit(-1)
        else:
            if imageName[-1:]=='.':
                imageName = imageName + 'png'
            else:
                imageName = imageName + r'.png'

        print(imageName)
        imgArray = cv2.imread(imageName, 0)        
        try:
            #convert numpyarray -> list -> bits
            bits = ObjectAndImage.arrayToBits(imgArray)
        except:
            print("Couldnot load image successfully. Check file or location")
            exit(-1)

        #convert bits -> ascii
        return ObjectAndImage.bitsToObject(bits)


# if __name__ == "__main__":
#     t_o = ObjectAndImage
#     t_o.objectToImageSave('Text to convert', 'file_name')
#     print(t_o.imageLoadToObject('file_name.png')) 
    