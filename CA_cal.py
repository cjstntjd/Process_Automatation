import openpyxl as op
from collections import Counter
import sys

send =  op.load_workbook('Big_CA_form.xlsx')
target = op.load_workbook('Big_CA_form_tar.xlsx')
sheet = send['Sheet1']
sheet_tar = target['Sheet1']

index_len=len(sheet['A'])

st = 3
ok_list=[]
no_list=[]

index_list=['A','F','K','P']
cc_list=['B','G','L','Q'] #2cc,3cc,4cc,5cc
rev_list=['E','J','O','T']
cover_list=['D','I','N','S']
ox_list=['C','H','M','R']

for se_n in range(len(cc_list)-1):#2cc부터
    for ta_n in range(se_n+1,len(cc_list)):#끝cc까지
        se = cc_list[se_n]
        ta = cc_list[ta_n]
        r_se = rev_list[se_n]
        r_ta = rev_list[ta_n]

        for i in range(st,index_len):#첫 cc의 출발 범위
            if sheet[se][i].value == None:
                continue

            split_x = sheet[se][i].value.split('-')#있으면 하나씩

            for j in range(st,index_len):
                if sheet[ta][j].value == None:
                    continue

                if sheet[r_ta][j].value != 'No':
                    split_y = sheet[ta][j].value.split('-')
                    cnt=0

                    p= Counter(split_x)
                    q= Counter(split_y)
                    for key in p:
                        for B_key in q:
                            if key == B_key:
                                if p[key]<=q[B_key]:
                                    cnt+=1

                    if cnt == len(p):
                        if sheet[se][i].value not in ok_list:
                            ok_list.append(sheet[se][i].value)
                            sheet_tar[cover_list[se_n]][i].value=sheet[index_list[ta_n]][j].value
                        elif sheet[se][i].value in ok_list:
                            sheet_tar[cover_list[se_n]][i].value=sheet[index_list[ta_n]][j].value

                elif sheet[r_ta][j].value =='No' and sheet[r_se][i].value=='No':
                    split_y = sheet[ta][j].value.split('-')
                    if split_x[0]==split_y[0]:
                        split_x.pop(0)
                        split_y.pop(0)
                        p=len(split_x)
                        cnt = 0
                        for x in split_x:
                            if x in split_y:
                                cnt+=1
                        if cnt==p:
                            if sheet[se][i].value not in ok_list:
                                ok_list.append(sheet[se][i].value)
                                sheet_tar[cover_list[se_n]][i].value=sheet[index_list[ta_n]][j].value
                            elif sheet[se][i].value in ok_list:
                                sheet_tar[cover_list[se_n]][i].value=sheet[index_list[ta_n]][j].value



        for i in range(st,index_len):
            if sheet[se][i].value == None:
                continue

            if sheet[se][i].value not in ok_list:
                if sheet[se][i].value not in no_list:
                    no_list.append(sheet[se][i].value)
        ok_list.append('//')
        no_list.append('//')

target.save('Big_CA_form_tar.xlsx')




print('\n\n측정 안해도 될거')
print(ok_list)

print('*************************')
print('측정 해야될거')
print(no_list)
