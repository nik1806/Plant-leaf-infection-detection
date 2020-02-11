# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 22:14:29 2018

@author: nikhil
"""
#This is the code for leaf_classification
def meanSD(filename):
    file = open(filename, 'r+')
    content = file.read()
    lines = content.split('\n')
    line_cnt = len(lines)
#    SD = float(lines[line_cnt - 1].split('=')[1])
    avg_per = float(lines[line_cnt-1].split('=')[1])
    file.close()
    return avg_per
    
if __name__ == '__main__':
    
    healthy_mean = meanSD('../healthy_result.txt')
    bac_mean = meanSD('../bacterial_result.txt') 
    
    #change name for different leaf type
    file = open('healthy_test_result.txt','r+')
    content = file.read()
    lines = content.split('\n')
    line_cnt = len(lines)
    
    file.seek(0)
    
    file.write(lines[0] + '\t\tDiff_healthy \tDiff_bacterial \tPrediction \tPre_Status')
    
    succ_cnt = 0
    total_cnt = 0
    
    for i in range(1, line_cnt):
        l = lines[i].split()
        
        if len(l) <= 1:
            continue
    
        diff_healthy = round(float(l[3]) - healthy_mean, 3)
        diff_bac= round(float(l[3]) - bac_mean, 3)

        l.append(diff_healthy)     
        l.append(diff_bac)     
    
        if abs(diff_bac) < abs(diff_healthy) :
            l.append('Infected')
        else:
            l.append('Healthy')
            
        if l[4] == l[-1]:
            l.append('Success')
            succ_cnt += 1
        else:
            l.append('Fail')
            
    #    file.write('\n' + lines[i] + '\t\t\t' + str(diff))
        file.write('\n') 
        file.write(('{:<15} {:<10} {:<18} {:<15} {:<15} {:<12} {:<12} {:<12} {:<15}'.format(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8])))
        
        total_cnt += 1
    
    succ_per = round(succ_cnt/ total_cnt * 100, 3)
    file.write('\n\n Correct Prediction (%) = '+ str(succ_per))
       
    file.close()