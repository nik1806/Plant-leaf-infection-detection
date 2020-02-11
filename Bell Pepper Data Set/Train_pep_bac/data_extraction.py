# -*- coding: utf-8 -*-
"""
@author: nikhil
This is the first program of overall experimentation.
This program calculated average infection percentage of a set of leaf images of specific type. 
It uses modified version of Otsu's threshold method for healthy region segmentation and Iterative Selection (IS) algorithm for segregating leaf from background of image.
It requires a set of images. The user need to put all images in the folder and put the code in the folder.
Also create a text file with name 'disease_result.txt', where all the results will be stored.

"""
import cv2
import numpy as np
import glob


#IS algorithm
def r_c(hist ):
    ''' The method returns the best threshold value for segregation of leaf region from backgournd.'''
    Ng = 255
    tc = 255
    index = 0

    while index <= tc and index <= Ng:
        bck_sum = 0
        hist_sum_bck = 0
        fr_sum = 0
        hist_sum_fr = 0
        b = 0 
        f = 0
               
        for i in range(0, index+1):
            bck_sum += i * hist[i][0]
            hist_sum_bck += hist[i][0]
            
        for j in range(index+1, Ng+1):
            fr_sum += j * hist[j][0]
            hist_sum_fr += hist[j][0]

        try:
            b = (bck_sum / hist_sum_bck)   
            f = (fr_sum / hist_sum_fr)
        
            if hist_sum_bck == 0.0 : 
                raise ZeroDivisionError  
            if hist_sum_fr == 0.0:
                raise ZeroDivisionError 
        except ZeroDivisionError:
            index += 1
            continue

        tc = (b  + f) // 2 

        index += 1
        
    return tc

#Excess green indexing function
def excGrnApp(b, g, r, pmin, pmax):
    row, col = g.shape
    Eg = np.zeros([row, col], np.uint8 )
    
    for i in range(0, row):
        for j in range(0, col):
            try:
                d = (2*g[i][j] - r[i][j] - b[i][j])//(g[i][j] + r[i][j] + b[i][j])
            except:
                d = 0

            try:                
                d = int((d - pmin) * 255 //( pmax - pmin))
            except:
                d = 0
                
            Eg[i][j] = d
            
    return Eg
 
#contour based region fill    
def regionfill(img):
    contour, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Ar = 0
    
    for cnt in contour:
        cv2.drawContours(img, [cnt],0,255,-1)
        Ar += cv2.contourArea(cnt) 
    
    return img, Ar


def lloret(b, g, r, img):
    '''
    The function takes arguments as original image and its color component matrices.
    It returns the segmented healthy region of leaf.
    A gray scale image is derived from original considering pixels values as values of green component pixel with highest values among other components.
    Other pixels are given zero value.
    Then, Otsu method is applied.
    '''
    row, col = b.shape

    z = np.zeros([row, col], np.uint8)
    
    for i in range(0, row):
        for j in range(0, col):
            if g[i][j] > b[i][j] and  g[i][j] > r[i][j]:
                z[i][j] = g[i][j]
                
    _, thresh = cv2.threshold(z, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
    
#Calculating area of the contour
def calArea(img):
    contour, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Ar = 0
    
    for cnt in contour:
        Ar += cv2.contourArea(cnt) 
    
    return Ar



def leafNDisArea(img):
    ''' 
    This takes the specific image for processing.
    Returns the total area of leaf, area of infected region and percentage infection
    First, leaf segmentation from background is performed followed by segregation of infected region.    
    '''
    b, g, r = cv2.split(img)
    # LEAF SEGMENTATION & AREA CALC
    #gray scale conversion using excess green indexing
    gray_grn = excGrnApp(b, g, r, -1, 2)
    hist = cv2.calcHist([gray_grn],[0],None,[256],[0,256])
    #IS algorithm is applied which return the optimum thresholding method
    thr = int(r_c(hist))
    _, bin_img = cv2.threshold(gray_grn, thr, 255, cv2.THRESH_BINARY)
    # Enhancing the output using median bluring filter
    bin_img = cv2.medianBlur(bin_img, 3)
    #region fill is applied
    bin_img, AT = regionfill(bin_img)
        
    # LESION SEGMENTATION & GREEN AREA CALCULATION
    #Modified Otsu's method is applied
    grn_area = lloret(b, g, r, img.copy())
    
    AU = calArea(grn_area)
    
    per_inf = round(((AT - AU) * 100 / AT), 3)

    
    return AT, AT-AU, per_inf


if __name__ == '__main__':
    ''' 
    This is the main function of program.
    Files are read and processed here.
    '''
    #Opening the result file
    file = open('../bacterial_result.txt', 'r+')
    #Writing experimental parameters to file
    file.write('Filenum\t Total Area\t Infected Area\t Infection (%)\t')
    
    filenum = 0 #Variable for file counter
    percentSum = 0 #Varaible for sum of percentage
    
    #Reading the images and algorithm is applied to calculate the results. Both .JPG and .jpg images are processed in the following loops.
    for filename in glob.glob('*.JPG'):
    
        filenum += 1    
            
        leaf = cv2.imread(filename)  

        AT, AI, P = leafNDisArea(leaf)

        percentSum += P    
        
        file.write('\n' + str(filenum)+'\t\t' + str(AT) +'\t\t\t' + str(AI) + '\t\t' + str(P))
        
    for filename in glob.glob('*.jpg'):
        
        filenum += 1    
            
        leaf = cv2.imread(filename)  

        AT, AI, P = leafNDisArea(leaf)

        percentSum += P    
        
        file.write('\n' + str(filenum)+'\t\t' + str(AT) +'\t\t\t' + str(AI) + '\t\t' + str(P))
    #Average percentage error for the particular type of leaf of crop.    
    avg_per = round(percentSum/filenum, 3)

    file.write('\n\n Average percentage error = ' + str( avg_per) )

    file.close()
