import pandas as pd
import openpyxl as op
from pandas import Series,DataFrame
from concurrent.futures import ThreadPoolExecutor
import time

global send
global target
global Row
global sheet
global sheet_row
global time_1

send = pd.read_csv('send.csv')
target = op.load_workbook('target.xlsx')
Row=len(send.index)
sheet = target['LTE B41 (2)']
sheet_row = len(sheet['A'])

time_1 = time.time()


num = [(0,Row//4),((Row//4)-1,Row//2),((Row//2)-1,(Row//4)*3),((Row//4)*3-1,Row)]


def go(pair):
    st,end=pair
    for i in range(st,end):
        for j in range(12,sheet_row):
            x1 = send[' BW'][i].replace(" ","")
            x2 = send[' Mode'][i].replace(" ","")
            x3 = send[' RBO'][i]
            x4 = send[' RBS'][i]
            x5 = send[' CHN'][i]

            y1 = sheet['A'][j].value.replace(" ","")
            y2 = sheet['B'][j].value.replace(" ","")
            y3 = sheet['C'][j].value
            y4 = sheet['D'][j].value

            if x5 == 39750:
                y5 = 'E'
            elif x5 == 40185:
                y5 = 'F'
            elif x5 == 40620:
                y5 = 'G'
            elif x5 == 41055:
                y5 = 'H'
            elif x5 == 41490:
                y5 = 'I'

            if (x1==y1) and (x2==y2) and (x3==y3) and (x4==y4):
                sheet[y5][j].value = send[' UE'][i]
    target.save('result.xlsx')
    print('시간 : ',time.time()-time_1)

pool = ThreadPoolExecutor(max_workers=4)
pool.map(go,num)

#너무 느림 알고리즘 개선이 필요함 코드가 짧을 수록 속도는 느림
#코드의 간결화도 좋지만 결과값만 나온다고 좋은것이 아님
