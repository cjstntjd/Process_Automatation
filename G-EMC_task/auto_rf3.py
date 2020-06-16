import openpyxl as op
from rf_test import *

# 엑셀 파일 수정해야 할듯

doc = Document('C:\\Users\\84430\\Desktop\\FlaskApp - 복사본\\empty.docx') # 테이블을 만들고자 하는 word 파일 open

def interface(seqList, fList):
    global doc
    for i in range(len(seqList)):
        auto_rf(i,seqList[i], fList[i])
    doc.save('test_result.docx')

def auto_rf(i,sequenceName, findFile):
    global doc
    print("start!")
    wb = op.load_workbook(findFile, data_only = True) # 데이터를 읽어오고자 하는 엑셀 파일 open

    total_sheet = wb.get_sheet_names()
    sheet_num = len(total_sheet)

    idx = 0
    while idx<sheet_num:

        if idx == 0:

            res_dict = getValue(idx,total_sheet,wb)

            #test_mode = res_dict['test_mode']
            #print('test_mode',type(test_mode),str(test_mode))
            f = res_dict['f']
            temp = res_dict['temp']

            introduction(i,doc,sequenceName,f,temp) #가장 기본적인 정보 입력 (최상단 테이블)

            ws1_name = total_sheet[idx]
            data = res_dict['data']
            regulation = res_dict['limit']

            single_table(doc,ws1_name,data,regulation)

            idx += 1


        elif idx > 0 and (sheet_num-1)%2 == 0: #계속 이거 돌리면 될듯 / 첫번째 빼고 남은게 짝수개니깐

            ws1_name = total_sheet[idx]
            res_dict = getValue(idx,total_sheet,wb)

            data1 = res_dict['data']
            regulation1 = res_dict['limit']

            idx += 1

            ws2_name = total_sheet[idx]
            res_dict = getValue(idx,total_sheet,wb)

            data2 = res_dict['data']
            regulation2 = res_dict['limit']

            idx += 1

            double_table(doc, ws1_name, data1, regulation1, ws2_name, data2, regulation2)

        elif idx > 0 and (sheet_num-1)%2 != 0: # 얘는 2로 나눈 몫 만큼 double돌리고 그다음 single 한번 마무리 -
            t = (sheet_num - 1)//2
            for _ in range(t):

                ws1_name = total_sheet[idx]
                res_dict = getValue(idx,total_sheet,wb)

                data1 = res_dict['data']
                regulation1 = res_dict['limit']

                idx += 1

                ws2_name = total_sheet[idx]
                res_dict = getValue(idx,total_sheet,wb)

                data2 = res_dict['data']
                regulation2 = res_dict['limit']

                idx += 1

                double_table(doc, ws1_name, data1, regulation1, ws2_name, data2, regulation2)

            ws1_name = total_sheet[idx]
            res_dict = getValue(idx,total_sheet,wb)

            data1 = res_dict['data']
            regulation1 = res_dict['limit']

            idx += 1
            single_table(doc,ws1_name,data,regulation)


def getValue(i,total_sheet,wb):
    ws1_name = total_sheet[i]
    ws1 = wb[ws1_name]

    #시험모드 802.11b
    test_mode = ws1['F16'].value

    # 시험주파수 F1, F2, F3
    f1 = ws1['I12'].value
    f2 = ws1['I13'].value
    f3 = ws1['I14'].value

    # 시험 환경
    temp1 = str(ws1['Z11'].value) + '℃' #상온
    temp2 = str(ws1['Z12'].value) + '℃' # 고온
    temp3 = str(ws1['Z13'].value) + '℃' #저온
    temp4 = str(ws1['Z14'].value) + '℃, ' + str(ws1['AD14'].value) +'%' # 습도

    # 복사해야 하는 데이터
    colList = ['BD','BE','BF']
    data = []
    for row in range(22,34):
        sub_data = []
        for col in colList:
            combo = col+str(row)
            if ws1[combo].value == '-' or ws1[combo].value == None:
                sub_data.append('-')

            elif float(ws1[combo].value) >= 0:
                sub_data.append("+%0.2f" %ws1[combo].value)

            else: sub_data.append(ws1[combo].value)
        data.append(sub_data)

    # 합격기준
    column = 'AR'
    regulation = ""
    if ws1_name == '주파수허용편차':

        regulation += str(ws1['AR23'].value) + "\n"
        regulation += str(ws1['AR25'].value) + "\n"
        regulation += '[' + str(ws1['AR27'].value) + ']' + "\n"

        f1 = str(ws1['AR30'].value) + str(ws1['AT30'].value) + str(ws1['AW30'].value)
        f2 = str(ws1['AR31'].value) + str(ws1['AT31'].value) + str(ws1['AW31'].value)
        f3 = str(ws1['AR32'].value) + str(ws1['AT32'].value) + str(ws1['AW32'].value)

        regulation += f1 + "\n" + f2 + "\n"+ f3

    if ws1_name == '안테나공급전력밀도':

        regulation += str(ws1['AR24'].value) + "\n"
        regulation += str(ws1['AR26'].value) + "\n"

        f1 = str(ws1['AT30'].value) + str(ws1['AT28'].value)
        f2 = '[ 정격 ' + str(ws1['AR28'].value) + str(ws1['AT28'].value) +']'
        f3 = 'limit: '+ str(ws1['AR30'].value)

        regulation += f1 + "\n" + f2  + "\n" + f3

    if ws1_name != '안테나공급전력밀도' and ws1_name != '주파수허용편차': # 점유주파수대역폭으 ㅣ합격기준 틀을 기준을 ㅗ잡기
        regulation += str(ws1['AR24'].value) + "\n"
        regulation += str(ws1['AR26'].value) + "\n"

        f1 = '['+ str(ws1['AR28'].value) + str(ws1['AU28'].value) + ' ' + str(ws1['AW28'].value) +']'
        regulation += f1

    result_dict = {'test_mode' : test_mode,
                    'f' : [f1,f2,f3],
                    'temp':[temp1,temp2,temp3,temp4],
                    'data':data,
                    'limit':regulation}

    return result_dict



findFile = 'rf_test.xlsx'
