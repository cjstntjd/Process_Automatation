import openpyxl as op
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import pandas as pd
import copy
data = pd.read_excel("./catest2.xlsx")
targetAd="cacopy2.xlsx"
target = op.load_workbook(targetAd)
targetSheet = target['Sheet1']

#column: 4-PCC 5-SCC1 6-SCC2
CH=[1.4,3,5,10,15,20]
RB=[6,15,25,50,75,100]

Frequency={'LTE1':[(1920,1980),(2110,2170),60,60,(range(2,6)),0],
           'LTE2':[(1850,1910),(1930,1990),60,60,(range(6)),600],
           'LTE3':[(1710,1785),(1805,1880),75,75,(range(6)),1200],
           'LTE4':[(1710,1755),(2110,2155),45,45,(range(6)),1950],
           'LTE5':[(824,849),(869,894),25,25,(range(4)),2400],
           'LTE6':[(830,840),(875,885),10,10,(range(2,4)),2650],
           'LTE7':[(2500,2570),(2620,2690),70,70,(range(2,6)),2750],
           'LTE8':[(880,915),(925,960),35,35,(range(4)),3450],
           'LTE9':[(1749.9,1784.9),(1844.9,1879.9),35,35,(range(2,6)),3800],
           'LTE10':[(1710,1770),(2110,2170),60,60,(range(2,6)),4150],
           'LTE11':[(1427.9,1447.9),(1475.9,1495.9),20,20,(range(2,4)),4750],
           'LTE12':[(699,716),(729,746),17,17,(range(4)),5010],
           'LTE13':[(777,787),(746,756),10,10,(range(2,4)),5180],
           'LTE14':[(788,798),(758,768),10,10,(range(2,4)),5280],
           'LTE17':[(704,716),(734,746),12,12,(range(2,4)),5730],
           'LTE18':[(815,830),(860,875),15,15,(range(2,5)),5850],
           'LTE19':[(830,845),(875,890),15,15,(range(2,5)),6000],
           'LTE20':[(832,862),(791,821),30,30,(range(2,6)),6150],
           'LTE21':[(1447.9,1462.9),(1495.9,1510.9),15,15,(range(2,5)),6450],
           'LTE22':[(3410,3490),(3510,3590),80,80,(range(2,6)),6600],
           'LTE23':[(2000,2020),(2180,2200),20,20,(range(6)),7500],
           'LTE24':[(1626.5,1660.5),(1525,2559),34,34,(range(2,4)),7700],
           'LTE25':[(1850,1915),(1930,1995),65,65,(range(6)),8040],
           'LTE26':[(814,849),(859,894),35,35,(range(5)),8690],
           'LTE27':[(807,824),(852,869),17,17,(range(4)),9040],
           'LTE28':[(703,748),(758,803),45,45,(range(1,6)),9210],
           'LTE29':[(0,0),(717,728),0,11,None,9660],
           'LTE30':[(2305,2315),(2350,2360),10,10,(range(2,4)),9770],
           'LTE31':[(452.5,257.5),(462.5,467.5),5,5,(range(3)),9870],
           'LTE32':[(0,0),(1452,1496),0,44,9920],
           #LTE32: CHANNEL 불확실
           #LTE 33-40 : TDD , else FDD
           'LTE33':[(1900,1920),(1900,1920),20,20,(range(2,6)),36000],
           'LTE34':[(2010,2025),(2010,2025),15,15,(range(2,5)),36200],
           'LTE35':[(1850,1910),(1850,1910),60,60,(range(6)),36350],
           'LTE36':[(1930,1990),(1930,1990),60,60,(range(6)),36950],
           'LTE37':[(1910,1930),(1910,1930),20,20,(range(2,6)),37550],
           'LTE38':[(2570,2620),(2570,2620),50,50,(range(2,6)),37750],
           'LTE39':[(1880,1920),(1880,1920),40,40,(range(2,6)),38250],
           'LTE40':[(2300,2400),(2300,2400),100,100,(range(2,6)),38650],
           'LTE41':[(2496,2690),(2496,2690),194,194,(range(2,6)),39650],
           'LTE42':[(3400,3600),(3400,3600),200,200,(range(2,6)),41590],
           'LTE43':[(3600,3800),(3600,3800),200,200,(range(2,6)),43590],
           'LTE44':[(703,803),(703,803),100,100,(range(1,6)),45590],
           'LTE45':[(1447,1467),(1447,1467),20,20,(range(2,6)),46590],
           'LTE46':[(5150,5925),(5150,5925),775,775,(3,5),46790],
           'LTE47':[(5855,5925),(5855,5925),70,70,(3,5),54540],
           'LTE48':[(3550,3700),(3550,3700),150,150,(range(2,6)),55240],
           'LTE49':[(3550,3700),(3550,3700),150,150,(3,5),56740],
           'LTE50':[(1432,1517),(1432,1517),85,85,(range(1,6)),58240],
           'LTE51':[(1427,1432),(1427,1432),5,5,(range(1,3)),59090],
           'LTE52':[(3300,3400),(3300,3400),100,100,(range(2,6)),59140],
           'LTE65':[(1920,2010),(2110,2200),90,90,(range(6)),65536],
           'LTE66':[(1710,1780),(2110,2200),70,90,(range(6)),66436],
           'LTE67':[(0,0),(738,758),0,20,None,67336],
           'LTE68':[(698,728),(753,783),30,30,(range(2,5)),67536],
           'LTE69':[(0,0),(2570,2620),0,50,None,67836],
           'LTE70':[(1695,1710),(1995,2020),15,25,(range(2,6)),68336],
           'LTE71':[(663,698),(617,652),35,35,(range(2,6)),68586],
           'LTE72':[(451,456),(461,466),5,5,(range(3)),68936],
           'LTE73':[(450,455),(460,465),5,5,(range(3)),68986],
           'LTE74':[(1427,1470),(1475,1518),43,43,(range(6)),69036],
           'LTE75':[(0,0),(1432,1517),0,85,None,69466],
           'LTE76':[(0,0),(1427,1432),0,5,None,70316],
           'LTE85':[(698,716),(728,746),18,18,(range(2,4)),70366]
           }

whole=data[4:][:].dropna(how='all')
c="LTE"

def Non(k,a,List):
    targetSheet[k+6][List[0]].value=CH[max(Frequency[c+a][4])]
    targetSheet[k+6][List[1]].value=Frequency[c+a][5]+(Frequency[c+a][3]*10)/2
    targetSheet[k+6][List[2]].value=sum(Frequency[c+a][1])/2

for k in range(len(whole)):
    current_pcc=whole.iloc[k][3] #엑셀 -3
    current_scc1=whole.iloc[k][4]
    current_scc2=whole.iloc[k][5]

    for i in range(len(current_pcc)):
        if current_pcc[i] in ['A','B','C','D']:
            current_pcc=current_pcc[:i]
            break
    for i in range(len(current_scc1)):
        if current_scc1[i] in ['A','B','C','D']:
            current_scc1=current_scc1[:i]
            break
    # CA 3을 위하여
    if str(type(current_scc2)) != "<class 'float'>":
        for i in range(len(current_scc2)):
            if current_scc2[i] in ['A','B','C','D']:
                current_scc2=current_scc2[:i]
                break


    targetSheet[k+6][11].value=whole.iloc[k][7] #?
    print(whole.iloc[k][7])
    targetSheet[k+6][12].value=Frequency[c+current_pcc][5]+(Frequency[c+current_pcc][3]*10)/2
    targetSheet[k+6][13].value=sum(Frequency[c+current_pcc][1])/2

    #intra band , non contiguous : 최대한 멀리 떨어져라
    if current_pcc != current_scc1: Non(k,current_scc1,[14,15,16])
    if current_pcc == current_scc1:
        targetSheet[k+6][14].value=CH[max(Frequency[c+current_scc1][4])]
        rvBW = list(Frequency[c+current_scc1][4])
        rvBW.reverse()
        for j in rvBW:
            print(">>",j)
            if sum(Frequency[c+current_pcc][1])/2+CH[j] < Frequency[c+current_scc1][1][1]:
                targetSheet[k+6][15].value = targetSheet[k+6][12].value + CH[j]*10
                targetSheet[k+6][16].value = targetSheet[k+6][13].value + targetSheet[k+6][14].value
            break

    if str(type(current_scc2)) != "<class 'float'>":
        if current_scc1 != current_scc2: Non(k,current_scc2,[17,18,19])
        if current_scc1 == current_scc2:
            targetSheet[k+6][17].value=CH[max(Frequency[c+current_scc2][4])]
            rvBW = list(Frequency[c+current_scc2][4])
            rvBW.reverse()
            for j in rvBW:
                if sum(Frequency[c+current_scc1][1])/2+CH[j] < Frequency[c+current_scc2][1][1]:
                    targetSheet[k+6][18].value = targetSheet[k+6][15].value + CH[j]*10
                    targetSheet[k+6][19].value = targetSheet[k+6][16].value + targetSheet[k+6][17].value
                break

#targetsheet는 엑셀에서 보이는 그 자체 만큼의 index로 설정

target.save(targetAd)
