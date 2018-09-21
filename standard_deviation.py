# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 15:32:57 2018

@author: nikhil
"""

file = open('../bacterial_result.txt', 'r+')
content = file.read()

file.seek(0)

lines = content.split('\n')

line_cnt = len(lines)

avg_per = float(lines[line_cnt - 1].split('=')[1])

file.write(lines[0] + '\tDifference')

diff_sum = 0
cnt = 0

for i in range(1, line_cnt):
    l = lines[i].split('\t\t')
    
    if len(l) <= 1:
        continue

    diff = round(float(l[3]) - avg_per, 3)
    
#    file.write('\n' + lines[i] + '\t\t\t' + str(diff))
    file.write('\n')

    l.append(diff) 
 
    file.write(('{:<15} {:<10} {:<18} {:<15} {:<15}'.format(l[0], l[1], l[2], l[3], l[4])))
   
    diff_sum += diff**2
    cnt += 1

SD = round((diff_sum / cnt)**0.5, 3)

file.write('\n\n' + lines[line_cnt-1])

file.write('\nStandard Deviation = ' + str(SD))
   
file.close()
