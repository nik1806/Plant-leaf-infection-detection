# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 20:16:17 2018

@author: nikhil
"""
import cv2
import numpy as np
import glob

def r_c(hist ):
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
    
def regionfill(img):
    _,contour, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Ar = 0
    
    for cnt in contour:
        cv2.drawContours(img, [cnt],0,255,-1)
        Ar += cv2.contourArea(cnt) 
    
    return img, Ar


def lloret(b, g, r, img):
    row, col = b.shape

    z = np.zeros([row, col], np.uint8)
    
    for i in range(0, row):
        for j in range(0, col):
            if g[i][j] > b[i][j] and  g[i][j] > r[i][j]:
                z[i][j] = g[i][j]
                
    _, thresh = cv2.threshold(z, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
    
    
def calArea(img):
    _,contour, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Ar = 0
    
    for cnt in contour:
        Ar += cv2.contourArea(cnt) 
    
    return Ar


def leafNDisArea(img):
    
    b, g, r = cv2.split(img)
    # LEAF SEGMENTATION & AREA CALC
    gray_grn = excGrnApp(b, g, r, -1, 2)
    hist = cv2.calcHist([gray_grn],[0],None,[256],[0,256])
    
    thr = int(r_c(hist))
    _, bin_img = cv2.threshold(gray_grn, thr, 255, cv2.THRESH_BINARY)
    bin_img = cv2.medianBlur(bin_img, 3)
    
    bin_img, AT = regionfill(bin_img)
        
    # LESION SEGMENTATION & GREEN AREA CALCULATION
    grn_area = lloret(b, g, r, img.copy())
    
    AU = calArea(grn_area)
    
    per_inf = round(((AT - AU) * 100 / AT), 3)

    
    return AT, AT-AU, per_inf


if __name__ == '__main__':
    file = open('late_test_result.txt', 'r+')
    file.write('Filenum\t Total Area\t Infected Area\t Infection (%)\t Category')
    
    filenum = 0
    percentSum = 0
    
    for filename in glob.glob('*.JPG'):
        
        filenum += 1    
            
        leaf = cv2.imread(filename)  

        AT, AI, P = leafNDisArea(leaf)

        percentSum += P    
        
        file.write('\n')
        file.write(('{:<15} {:<15} {:<15} {:<10} {:<15}'.format(filenum, AT, AI, P, 'Infected')))

    for filename in glob.glob('*.jpg'):
        
        filenum += 1    
            
        leaf = cv2.imread(filename)  

        AT, AI, P = leafNDisArea(leaf)

        percentSum += P    
        
        file.write('\n')
        file.write(('{:<15} {:<15} {:<15} {:<10} {:<15}'.format(filenum, AT, AI, P, 'Infected')))

       
    avg_per = round(percentSum/filenum, 3)

    file.write('\n\n Average percentage error = ' + str( avg_per) )

    file.close()