import pandas as pd
import os
import sys
newpath = os.path.abspath(os.path.curdir)
sys.path.append(newpath)
import config
from csv import reader


#vhsPath = config.PATH_APP + config.PATH_VHS + config.FILE_VHS

valEN ={
    'strongly agree': 1,
    'agree': 2,
    'neither agree or disagree': 3,
    'neither agree nor disagree': 3,
    'disagree': 4,
    'strongly disagree': 5
}

valES ={
    'totalmente de acuerdo': 1,
    'de acuerdo': 2,
    'ni de acuerdo ni en desacuerdo': 3,
    'en desacuerdo': 4,
    'totalmente en desacuerdo': 5
}

valFR ={
    "tout ã\xa0 fait d'accord": 1,
    "tout ã\xa0 fait dâ€™accord": 1,
    "d'accord": 2,
    "dâ€™accord": 2,
    "ni d'accord ni en dã©saccord": 3,
    "ni dâ€™accord ni en dã©saccord": 3,
    "pas d'accord": 4,
    "pas dâ€™accord": 4,
    "pas du tout d'accord": 5,
    "pas du tout dâ€™accord": 5
}


def responseVal(lang, ans, reversed):
    q = ans.rstrip().lstrip().lower()
    if lang == 'EN-US':
        if reversed:
            return valEN[q]
        else: return 6-valEN[q]
    elif lang == 'ES-US':
        if reversed:
            return valES[q]
        else: return 6-valES[q]
    elif lang == 'FR-CA':
        if reversed:
            return valFR[q]
        else: return 6-valFR[q]
    else:
        raise ('Language mismatch error in AnalysisMgr')

datQ = {1:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        2:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        3:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        4:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        5:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        6:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        7:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        8:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        9:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
           'ES-US': {1:0,2:0,3:0,4:0,5:0},
           'FR-CA': {1:0,2:0,3:0,4:0,5:0}},
        10:{'EN-US': {1:0,2:0,3:0,4:0,5:0},
            'ES-US': {1:0,2:0,3:0,4:0,5:0},
            'FR-CA': {1:0,2:0,3:0,4:0,5:0}}}

numLang = {'EN-US': 0, 'ES-US': 0, 'FR-CA': 0}

def ansSum():
    qReverse = ['reverseCheck', True, True, True, True, False, True, True, True, False, False]
    #datPath = os.path.abspath(os.path.curdir) + '/' + config.PATH_DATA + config.FILE_DATA
    datPath = os.path.abspath(os.path.curdir) + '/' + config.PATH_DATA + config.FILE_DATA
    print(datPath)
    with open(datPath,'r') as d:
        dat = reader(d)
        txt = 'lang,qr1,qr2,qr3,qr4,q5,qr6,qr7,qr8,q9,q10'
        for line in dat:
            lang = line[0]
            numLang[lang] += 1

            txt += f'\n{lang}'
            for i, q in enumerate(line):
                if i == 0:
                    pass
                else:
                    val = responseVal(lang, q.lstrip().rstrip().lower(), qReverse[i])
                    #print(val)
                    datQ[i][lang][val] += 1
                    txt += f',{val}'
    return txt


# datQ[2]['EN-US'][5] += 1
# datQ[2]['EN-US'][5] += 1
print(datQ)

outFile = f'{config.PATH_APP}{config.PATH_ANA}{config.FILE_DATA[:-4]}-encoded.csv'
print(outFile)
if os.path.exists(outFile):
    print('The encoded file was previously saved to: ' + outFile)
else:
    with open(outFile,'w') as outf:
        print('The encoded file has been saved to: ' + outFile)
        outf.write(ansSum())



langList = ['EN-US', 'ES-US', 'FR-CA']
qList = [1,2,3,4,5,6,7,8,9,10]
ansList = [1,2,3,4,5]

# numQ = {}
# lang = 'FR-CA'
# q = 2

sum=0
for q in qList:
    for lang in langList:
        for ans in ansList:
            sum += datQ[q][lang][ans]

print(sum)

