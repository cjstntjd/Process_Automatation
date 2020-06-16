import pandas as pd
import numpy as np
import openpyxl as op
import sys
import sklearn as sk
import joblib as jl
from datetime import datetime, timedelta

def convert(p):
    df = pd.DataFrame(columns=['RE_120','RE_220','RE_230','CE_120','CE_220','CE_230','Hamonic','Flicker','ESD','RS','EFT_Burst_120','EFT_Burst_220','EFT_Burst_230','Surge_120','Surge_220','Surge_230','CS_120','CS_220','CS_230','MF_120','MF_220','MF_230','Dip_120','Dip_220','Dip_230'])
    total_time =0
    mode_list=p
    test_mode =len(mode_list)

    model = jl.load('g_predict.pkl')

    test_li = ['RE_120','RE_220','RE_230','CE_120','CE_220','CE_230','Hamonic','Flicker','ESD','RS','EFT_Burst_120','EFT_Burst_220','EFT_Burst_230','Surge_120','Surge_220','Surge_230','CS_120','CS_220','CS_230','MF_120','MF_220','MF_230','Dip_120','Dip_220','Dip_230']

    for mode_num in range(len(mode_list)):

        set_list=[]

        for x in range(len(test_li)):
            set_list.append(0)

        for x in mode_list[mode_num]:
            if x == 'RE':
                set_list[0]=1
                set_list[1]=1
                set_list[2]=1
            elif x == 'CE':
                set_list[3]=1
                set_list[4]=1
                set_list[5]=1
            elif x == 'Hamonic':
                set_list[6]=1
            elif x == 'Flicker':
                set_list[7]=1
            elif x == 'ESD':
                set_list[8]=1
            elif x == 'RS':
                set_list[9]=1
            elif x == 'EFT':
                set_list[10]=1
                set_list[11]=1
                set_list[12]=1
            elif x == 'Surge':
                set_list[13]=1
                set_list[14]=1
                set_list[15]=1
            elif x == 'CS':
                set_list[16]=1
                set_list[17]=1
                set_list[18]=1
            elif x == 'MF':
                set_list[19]=1
                set_list[20]=1
                set_list[21]=1
            elif x == 'Dip':
                set_list[22]=1
                set_list[23]=1
                set_list[24]=1

        df.loc[mode_num] = set_list

    df = df.astype(int)
    pred = model.predict(df)
    return sum(pred)
