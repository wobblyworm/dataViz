import os
from csv import reader


txt = 'run,q1,q2,q3,q4,qr5,q6,q7,q8,qr9,qr10,en_yn,es_yn,fr_yn,val\n'

with open('lewandowski12.csv','r', encoding='UTF-8') as f:
    inFile = reader(f)
    next(inFile)
    for x in inFile:
        for i in range(1,11):
            txt += x[14] + ','
            for j in range(1,11):
                if i==j:
                    txt += '1,'
                else:
                    txt += '0,'
            
            txt += f'{x[11]},{x[12]},{x[13]},{x[i]}\n'
#print(txt)

with open('lewandowski12-regression.csv', 'w', encoding='UTF-8') as fw:
    fw.write(txt)
