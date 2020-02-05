#2월 4일 이슈 : 1.4 3 밴드 관련해서 RSO값을 전혀 모름 데이터 받아서 보정하기  + bana 추가 하기
#추가적인 ROW 데이터가 급선무 받아서 보고 들어가는지 확인 하고 내일 중으로 ver1 완성 하는 시간을 갖기
#첫 if 문부터 정확히 들어가 있는지 확인 하기

import sys, UI
import pandas as pd
import openpyxl as op
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication,QDate,Qt


##################################################################################
###################필    수#######################################################

# 주석 읽고 디버깅 하기
#연산 복잡도 Big O 표기에 따른 연산량 계산해서 지금보다 더 낮은 수준으로 고도화 할것
#연산량을 줄이는 가장 좋은 방법은 1:1 매칭 형태로 잡아주는것이 제일 좋음


#원본 파일은 항상 냅두고 복사 파일로 돌려볼것
#인덱스가 달라지면 결과값도 달라짐
#####################################################################################

###############################################################################
#프로그램 시작

class MyApp(UI.Ui_Dialog,QDialog):
    global send_name
    global get_name

    global Max_power
    global Hotspot_power
    global back_off_power
##################################################
#이니셜라이즈 및 셋업 과정
    def __init__(self):
        super().__init__()
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.date = QDate.currentDate()
        self.initUI()
########################################################
#화면 출력에 관해서
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.center()

        #버튼과 ui 상호작용
        self.send_file.clicked.connect(self.OnOpenDocument)#fname1
        self.send_file.setToolTip('파일 불러오기 입니다.')

        self.get_file.clicked.connect(self.OnOpenDocument2)
        self.get_file.setToolTip('파일 불러오기 입니다.')

        self.quit.clicked.connect(QCoreApplication.instance().quit)
        self.quit.setToolTip('종료하기')

        self.ok.clicked.connect(self.okFunction)
        self.ok.setToolTip('확인')

        #체크박스
        self.max_chk.stateChanged.connect(self.chkFunction)
        self.hot_chk.stateChanged.connect(self.chkFunction)
        self.back_chk.stateChanged.connect(self.chkFunction)
        #콤보박스
        self.combo.activated[str].connect(self.comboEvent)
#######################################################################
#상단 위도우 박스 정리 및 크기 레이아웃 정리
#로고 정리


        self.setWindowTitle('SAR Team Excel Assistant')
        self.move(600, 600)
        self.resize(600, 300)
        self.show()
        self.setWindowIcon(QIcon('window_logo.png'))




######################################################################
#지역별로 함수 정리및 디펜던시 체크 할것
#변수가 global에 포함되어있는지 체크 하고 구동할것

    def comboEvent(self,text):
        global Band
        Band = text
#####################################################################
#주의 !!
#여기에 절대로 loc iloc같은 서치형 함수 사용하지 말것
#각 변수에 결과값은 밑에 보이는대로 1:1 매칭을 하면 가장 빠름
#여기서 부터 확인버튼 누르면 돌아가는 코드
    def okFunction(self):
        global Row
        send = pd.read_csv(send_name)
        target = op.load_workbook(get_name)
        Row=len(send.index)
        sheet = target[Band]
        sheet_row = len(sheet['A'])
#for문은 1번만 사용할것
        for i in range(Row):
#시리즈나 데이터 프레임을 만들면 메모리 낭비가 심함
            x3 = send[' RBO'][i]
            x4 = send[' RBS'][i]
            x5 = send[' CHN'][i]
            self.textBox.append('Processing....'+str(i)+'\n')

            if (Band =='LTE B41') or (Band == 'LTE B41(HPUE)') or (Band == 'LTE B41(IC)'):
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
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
                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if x5 == 39750:
                        y5 = 'L'
                    elif x5 == 40185:
                        y5 = 'M'
                    elif x5 == 40620:
                        y5 = 'N'
                    elif x5 == 41055:
                        y5 = 'O'
                    elif x5 == 41490:
                        y5 = 'P'
                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if x5 == 39750:
                        y5 = 'S'
                    elif x5 == 40185:
                        y5 = 'T'
                    elif x5 == 40620:
                        y5 = 'U'
                    elif x5 == 41055:
                        y5 = 'V'
                    elif x5 == 41490:
                        y5 = 'W'

                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12


                #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6
                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]



            elif Band == 'LTE B2':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 18700) or (x5 == 18675) or (x5 == 18650) or (x5 == 18625) or (x5 == 18615) or (x5 == 18607):
                        y5 = 'E'
                    elif x5 == 18900:
                        y5 = 'F'
                    elif (x5 == 19100) or (x5 == 19125) or (x5 == 19150) or (x5 == 19175) or (x5 == 19185) or (x5 == 19193) :
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 18700) or (x5 == 18675) or (x5 == 18650) or (x5 == 18625) or (x5 == 18615) or (x5 == 18607):
                        y5 = 'J'
                    elif x5 == 18900:
                        y5 = 'K'
                    elif (x5 == 19100) or (x5 == 19125) or (x5 == 19150) or (x5 == 19175) or (x5 == 19185) or (x5 == 19193) :
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 18700) or (x5 == 18675) or (x5 == 18650) or (x5 == 18625) or (x5 == 18615) or (x5 == 18607):
                        y5 = 'O'
                    elif x5 == 18900:
                        y5 = 'P'
                    elif (x5 == 19100) or (x5 == 19125) or (x5 == 19150) or (x5 == 19175) or (x5 == 19185) or (x5 == 19193):
                        y5 = 'Q'

                if send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12

                elif send[' BW'][i]== ' 3MHz ':
                    st = 136

                elif send[' BW'][i]== ' 1.4MHz ':
                    st = 167

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]########################################################여기서부터***********


            elif Band == 'LTE B4':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 20050) or (x5 == 20025) or (x5 == 20000) or (x5 == 19975) or (x5 == 19965) or (x5 == 19957):
                        y5 = 'E'
                    elif x5 == 20175:
                        y5 = 'F'
                    elif (x5 == 20300) or (x5 == 20325) or (x5 == 20350) or (x5 == 20375) or (x5 == 20385) or (x5 == 20393):
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 20050) or (x5 == 20025) or (x5 == 20000) or (x5 == 19975) or (x5 == 19965) or (x5 == 19957):
                        y5 = 'J'
                    elif x5 == 20175:
                        y5 = 'K'
                    elif (x5 == 20300) or (x5 == 20325) or (x5 == 20350) or (x5 == 20375) or (x5 == 20385) or (x5 == 20393):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 20050) or (x5 == 20025) or (x5 == 20000) or (x5 == 19975) or (x5 == 19965) or (x5 == 19957):
                        y5 = 'O'
                    elif x5 == 20175:
                        y5 = 'P'
                    elif (x5 == 20300) or (x5 == 20325) or (x5 == 20350) or (x5 == 20375) or (x5 == 20385) or (x5 == 20393):
                        y5 = 'Q'

                if send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12

                elif send[' BW'][i]== ' 3MHz ':
                    st = 136

                elif send[' BW'][i]== ' 1.4MHz ':
                    st = 167

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]########################################################여기서부터***********

            elif Band == 'LTE B5':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 20450) or (x5 == 20425) or (x5 == 20415) or (x5 == 20407):
                        y5 = 'E'
                    elif x5 == 20525:
                        y5 = 'F'
                    elif (x5 == 20600) or (x5 == 20625) or (x5 == 20635) or (x5 == 20643):
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 20450) or (x5 == 20425) or (x5 == 20415) or (x5 == 20407):
                        y5 = 'J'
                    elif x5 == 20525:
                        y5 = 'K'
                    elif (x5 == 20600) or (x5 == 20625) or (x5 == 20635) or (x5 == 20643):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 20450) or (x5 == 20425) or (x5 == 20415) or (x5 == 20407):
                        y5 = 'O'
                    elif x5 == 20525:
                        y5 = 'P'
                    elif (x5 == 20600) or (x5 == 20625) or (x5 == 20635) or (x5 == 20643):
                        y5 = 'Q'

                if send[' BW'][i]== ' 1.4MHz ':
                    st = 105

                elif send[' BW'][i]== ' 3MHz ':
                    st = 74

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43

                elif send[' BW'][i]== ' 10MHz ':
                    st = 12

            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]########################################################여기서부터***********
            elif Band == 'LTE B7':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 20850) or (x5 == 20825) or (x5 == 20800) or (x5 == 20775):
                        y5 = 'E'
                    elif x5 == 21100:
                        y5 = 'F'
                    elif (x5 == 21350) or (x5 == 21375) or (x5 == 21400) or (x5 == 21425):
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 20850) or (x5 == 20825) or (x5 == 20800) or (x5 == 20775):
                        y5 = 'J'
                    elif x5 == 21100:
                        y5 = 'K'
                    elif (x5 == 21350) or (x5 == 21375) or (x5 == 21400) or (x5 == 21425):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 20850) or (x5 == 20825) or (x5 == 20800) or (x5 == 20775):
                        y5 = 'O'
                    elif x5 == 21100:
                        y5 = 'P'
                    elif (x5 == 21350) or (x5 == 21375) or (x5 == 21400) or (x5 == 21425):
                        y5 = 'Q'

                if send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12

            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]########################################################여기서부터***********

            elif Band == 'LTE B12':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 23060) or (x5 == 23035) or (x5 == 23025) or (x5 == 23017):
                        y5 = 'E'
                    elif x5 == 23095:
                        y5 = 'F'
                    elif (x5 == 23130) or (x5 == 23155) or (x5 == 23165) or (x5 == 23173):
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 23060) or (x5 == 23035) or (x5 == 23025) or (x5 == 23017):
                        y5 = 'J'
                    elif x5 == 23095:
                        y5 = 'K'
                    elif (x5 == 23130) or (x5 == 23155) or (x5 == 23165) or (x5 == 23173):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 23060) or (x5 == 23035) or (x5 == 23025) or (x5 == 23017):
                        y5 = 'O'
                    elif x5 == 23095:
                        y5 = 'P'
                    elif (x5 == 23130) or (x5 == 23155) or (x5 == 23165) or (x5 == 23173):
                        y5 = 'Q'

                if send[' BW'][i]== ' 1.4MHz ':
                    st = 105

                elif send[' BW'][i]== ' 3MHz ':
                    st = 74

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43

                elif send[' BW'][i]== ' 10MHz ':
                    st = 12

            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]##

            elif Band == 'LTE B13':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 23230):
                        y5 = 'F'
                    elif (x5 == 23205):
                        y5 = 'E'
                    elif (x5 == 23255):
                        y5 = 'G'


                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 23230):
                        y5 = 'K'
                    elif (x5 == 23205):
                        y5 = 'J'
                    elif (x5 == 23255):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 23230):
                        y5 = 'P'
                    elif (x5 == 23205):
                        y5 = 'O'
                    elif (x5 == 23255):
                        y5 = 'Q'


                if send[' BW'][i]== ' 10MHz ':
                    st = 12

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43



            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]

            elif Band == 'LTE B14':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 23305):
                        y5 = 'E'
                    elif (x5 == 23330):
                        y5 = 'F'
                    elif (x5 == 23355):
                        y5 = 'G'


                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 23305):
                        y5 = 'J'
                    elif (x5 == 23330):
                        y5 = 'K'
                    elif (x5 == 23355):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 23305):
                        y5 = 'O'
                    elif (x5 == 23330):
                        y5 = 'P'
                    elif (x5 == 23355):
                        y5 = 'Q'


                if send[' BW'][i]== ' 10MHz ':
                    st = 12

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43



            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]


            elif Band == 'LTE B17':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 23755):
                        y5 = 'E'
                    elif (x5 == 23790):
                        y5 = 'F'
                    elif (x5 == 23825):
                        y5 = 'G'


                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 23755):
                        y5 = 'J'
                    elif (x5 == 23790):
                        y5 = 'K'
                    elif (x5 == 23825):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 23755):
                        y5 = 'O'
                    elif (x5 == 23790):
                        y5 = 'P'
                    elif (x5 == 23825):
                        y5 = 'Q'


                if send[' BW'][i]== ' 10MHz ':
                    st = 12

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43



            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]

            elif Band == 'LTE B25':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if (x5 == 26140) or (x5 == 26115) or (x5 == 26090) or (x5 == 26065) or (x5 == 26055) or (x5 == 26047):
                        y5 = 'E'
                    elif x5 == 26365:
                        y5 = 'F'
                    elif (x5 == 26590) or (x5 == 26615) or (x5 == 26640) or (x5 == 26665) or (x5 == 26675) or (x5 == 26683):
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if (x5 == 26140) or (x5 == 26115) or (x5 == 26090) or (x5 == 26065) or (x5 == 26055) or (x5 == 26047):
                        y5 = 'J'
                    elif x5 == 26365:
                        y5 = 'K'
                    elif (x5 == 26590) or (x5 == 26615) or (x5 == 26640) or (x5 == 26665) or (x5 == 26675) or (x5 == 26683):
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if (x5 == 26140) or (x5 == 26115) or (x5 == 26090) or (x5 == 26065) or (x5 == 26055) or (x5 == 26047):
                        y5 = 'O'
                    elif x5 == 26365:
                        y5 = 'P'
                    elif (x5 == 26590) or (x5 == 26615) or (x5 == 26640) or (x5 == 26665) or (x5 == 26675) or (x5 == 26683):
                        y5 = 'Q'

                if send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12

                elif send[' BW'][i]== ' 3MHz ':
                    st = 136

                elif send[' BW'][i]== ' 1.4MHz ':
                    st = 167

            ######################################

                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6

                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    else:
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value


                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]##
            elif Band == 'LTE B26':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if x5 == 26765 or x5==26740 or x5==26715 or x5==26705 or x5==26697:
                        y5 = 'E'
                    elif x5 == 26865:
                        y5 = 'F'
                    elif x5 == 26965 or x5==26990 or x5==27015 or x5==27025 or x5==27033:
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if x5 == 26765 or x5==26740 or x5==26715 or x5==26705 or x5==26697:
                        y5 = 'J'
                    elif x5 == 26865:
                        y5 = 'K'
                    elif x5 == 26965 or x5==26990 or x5==27015 or x5==27025 or x5==27033:
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if x5 == 26765 or x5==26740 or x5==26715 or x5==26705 or x5==26697:
                        y5 = 'O'
                    elif x5 == 26865:
                        y5 = 'P'
                    elif x5 == 26965 or x5==26990 or x5==27015 or x5==27025 or x5==27033:
                        y5 = 'Q'

                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz ':
                    st = 136

                elif send[' BW'][i]== ' 3MHz ':
                    st = 105

                elif send[' BW'][i]== ' 5MHz ':
                    st = 74

                elif send[' BW'][i]== ' 10MHz ':
                    st = 43

                elif send[' BW'][i]== ' 15MHz ':
                    st = 12

                elif send[' BW'][i]== ' 20MHz ': #NOT EXIST
                    st = 167


            #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6
    #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7 :
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    else:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value

                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]

            elif Band == 'LTE B27':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if x5 == 27090 or x5==27065 or x5==27055 or x5==27047:
                        y5 = 'E'
                    elif x5 == 27125:
                        y5 = 'F'
                    elif x5 == 27160 or x5==27185 or x5==27195 or x5==27203:
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if x5 == 27090 or x5==27065 or x5==27055 or x5==27047:
                        y5 = 'J'
                    elif x5 == 27125:
                        y5 = 'K'
                    elif x5 == 27160 or x5==27185 or x5==27195 or x5==27203:
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if x5 == 27090 or x5==27065 or x5==27055 or x5==27047:
                        y5 = 'O'
                    elif x5 == 27125:
                        y5 = 'P'
                    elif x5 == 27160 or x5==27185 or x5==27195 or x5==27203:
                        y5 = 'Q'

                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz ':
                    st = 105

                elif send[' BW'][i]== ' 3MHz ':
                    st = 74

                elif send[' BW'][i]== ' 5MHz ':
                    st = 43

                elif send[' BW'][i]== ' 10MHz ':
                    st = 12

                elif send[' BW'][i]== ' 15MHz ':#NOT EXIST
                    st = 136

                elif send[' BW'][i]== ' 20MHz ': #NOT EXIST
                    st = 136


            #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6
    #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7 :
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    else:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value

                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]
            elif Band =='LTE B30':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                  if x5 == 27685:
                      y5 = 'E'
                  elif x5 == 27710:
                      y5 = 'F'
                  elif x5 == 27735:
                      y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                  if x5 == 27685:
                      y5 = 'J'
                  elif x5 == 27710:
                      y5 = 'K'
                  elif x5 == 27735:
                      y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                  if x5 == 27685:
                      y5 = 'O'
                  elif x5 == 27710:
                      y5 = 'P'
                  elif x5 == 27735:
                      y5 = 'Q'


                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz':    # NOT EXIST
                  st = 74

                elif send[' BW'][i]== ' 3MHz':    # NOT EXIST
                  st = 74

                elif send[' BW'][i]== ' 5MHz ':
                  st = 43

                elif send[' BW'][i]== ' 10MHz ':
                  st = 12

                elif send[' BW'][i]== ' 15MHz ':    # NOT EXIST
                  st = 12


                #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                  fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                  st = st + 7
                  fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                  st = st + 14
                  fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                  st = st + 21
                  fin= st + 6
                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                  if send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==7 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==3 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==5 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 3MHz ' and x3==3 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-4
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value+1
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  else:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value


                  if (x3==y3) and (x4==y4):
                      sheet[y5][j].value = send[' UE'][i]

            elif Band == 'LTE B38':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                    if x5 == 37850 or x5==37825 or x5==37800 or x5==37775:
                        y5 = 'E'
                    elif x5 == 38000:
                        y5 = 'F'
                    elif x5 == 38150 or x5==38175 or x5==38200 or x5==38225:
                        y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                    if x5 == 37850 or x5==37825 or x5==37800 or x5==37775:
                        y5 = 'J'
                    elif x5 == 38000:
                        y5 = 'K'
                    elif x5 == 38150 or x5==38175 or x5==38200 or x5==38225:
                        y5 = 'L'

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                    if x5 == 37850 or x5==37825 or x5==37800 or x5==37775:
                        y5 = 'O'
                    elif x5 == 38000:
                        y5 = 'P'
                    elif x5 == 38150 or x5==38175 or x5==38200 or x5==38225:
                        y5 = 'Q'

                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz ':
                    st = 106

                elif send[' BW'][i]== ' 3MHz ':
                    st = 106

                elif send[' BW'][i]== ' 5MHz ':
                    st = 105

                elif send[' BW'][i]== ' 10MHz ':
                    st = 74

                elif send[' BW'][i]== ' 15MHz ':
                    st = 43

                elif send[' BW'][i]== ' 20MHz ':
                    st = 12


            #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6
    #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7 :
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    else:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value

                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]

            elif Band == 'LTE B40':
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                      if x5 == 38725:
                          y5 = 'E'
                      elif x5 == 38750:
                          y5 = 'F'
                      elif x5 == 38775:
                          y5 = 'G'
                      elif x5 == 39175:
                          y5 = 'H'
                      elif x5 == 39200:
                          y5 = 'I'
                      elif x5 == 39225:
                          y5 = 'J'
                      elif x5 == 39599 or x5 ==38700: continue

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                      if x5 == 38725:
                          y5 = 'M'
                      elif x5 == 38750:
                          y5 = 'N'
                      elif x5 == 38775:
                          y5 = 'O'
                      elif x5 == 39175:
                          y5 = 'P'
                      elif x5 == 39200:
                          y5 = 'Q'
                      elif x5 == 39225:
                          y5 = 'R'
                      elif x5 == 39599 or x5 ==38700: continue

                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                      if x5 == 38725:
                          y5 = 'U'
                      elif x5 == 38750:
                          y5 = 'V'
                      elif x5 == 38775:
                          y5 = 'W'
                      elif x5 == 39175:
                          y5 = 'X'
                      elif x5 == 39200:
                          y5 = 'Y'
                      elif x5 == 39225:
                          y5 = 'Z'
                      elif x5 == 39599 or x5 ==38700: continue
                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz':  #NOT EXIST
                  st = 74

                elif send[' BW'][i]== ' 3MHz':  #NOT EXIST
                  st = 74

                elif send[' BW'][i]== ' 5MHz ':
                  st = 43

                elif send[' BW'][i]== ' 10MHz ':
                  st = 12

                elif send[' BW'][i]== ' 15MHz ': #NOT EXIST
                  st = 74

                elif send[' BW'][i]== ' 20MHz ': #NOT EXIST
                  st = 74


            #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                    fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                    st = st + 7
                    fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                    st = st + 14
                    fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                    st = st + 21
                    fin= st + 6
    #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                    if send[' BW'][i]== ' 3MHz ' and x3==1 and x4==7 :
                        y3 = sheet['C'][j].value
                        y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==3 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 3MHz ' and x3==8 and x4==5 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 1.4MHz ' and x3==3 and x4==2 :
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-2
                    elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-4
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value+1
                    elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value-1
                    else:
                         y3 = sheet['C'][j].value
                         y4 = sheet['D'][j].value

                    if (x3==y3) and (x4==y4):
                        sheet[y5][j].value = send[' UE'][i]

            elif Band =='LTE B41_3ch': # 주파수대역별로 계산 필요
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                      if x5 == 40340 or x5==40315 or x5==40290 or x5==40265:
                          y5 = 'E'
                      elif x5 == 40740:
                          y5 = 'F'
                      elif x5 == 41140 or x5==41165 or x5==41190 or x5==41215:
                          y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                      if x5 == 40340 or x5==40315 or x5==40290 or x5==40265:
                          y5 = 'J'
                      elif x5 == 40740:
                          y5 = 'K'
                      elif x5 == 41140 or x5==41165 or x5==41190 or x5==41215:
                          y5 = 'L'


                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                      if x5 == 40340 or x5==40315 or x5==40290 or x5==40265:
                          y5 = 'O'
                      elif x5 == 40740:
                          y5 = 'P'
                      elif x5 == 41140 or x5==41165 or x5==41190 or x5==41215:
                          y5 = 'Q'


                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 3MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 5MHz ':
                  st = 105

                elif send[' BW'][i]== ' 10MHz ':
                  st = 74

                elif send[' BW'][i]== ' 15MHz ':
                  st = 43

                elif send[' BW'][i]== ' 20MHz ':
                  st = 12



                #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                  fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                  st = st + 7
                  fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                  st = st + 14
                  fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                  st = st + 21
                  fin= st + 6
                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                  if send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==7 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==3 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==5 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 3MHz ' and x3==3 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-4
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value+1
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  else:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value


                  if (x3==y3) and (x4==y4):
                      sheet[y5][j].value = send[' UE'][i]

            elif Band =='LTE B48':    # 여기는 frequecy가 겹치는게 하나도 없어서 어쩔수 없었음.
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                      if x5 == 55340 or x5 == 55315 or x5 == 55290 or x5 == 55265:
                          y5 = 'E'
                      elif x5 == 55773 or x5 == 55765 or x5 == 55757 or x5 == 55748:
                          y5 = 'F'
                      elif x5 == 56207 or x5 == 56215 or x5 == 56223 or x5 == 56232:
                          y5 = 'G'
                      elif x5 == 56640 or x5 == 56665 or x5 == 56690 or x5 == 56715:
                          y5 = 'H'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                      if x5 == 55340 or x5 == 55315 or x5 == 55290 or x5 == 55265:
                          y5 = 'K'
                      elif x5 == 55773 or x5 == 55765 or x5 == 55757 or x5 == 55748:
                          y5 = 'L'
                      elif x5 == 56207 or x5 == 56215 or x5 == 56223 or x5 == 56232:
                          y5 = 'M'
                      elif x5 == 56640 or x5 == 56665 or x5 == 56690 or x5 == 56715:
                          y5 = 'N'


                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                      if x5 == 55340 or x5 == 55315 or x5 == 55290 or x5 == 55265:
                          y5 = 'Q'
                      elif x5 == 55773 or x5 == 55765 or x5 == 55757 or x5 == 55748:
                          y5 = 'R'
                      elif x5 == 56207 or x5 == 56215 or x5 == 56223 or x5 == 56232:
                          y5 = 'S'
                      elif x5 == 56640 or x5 == 56665 or x5 == 56690 or x5 == 56715:
                          y5 = 'T'

                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 3MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 5MHz ':
                  st = 105

                elif send[' BW'][i]== ' 10MHz ':
                  st = 74

                elif send[' BW'][i]== ' 15MHz ':
                  st = 43

                elif send[' BW'][i]== ' 20MHz ':
                  st = 12



                #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                  fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                  st = st + 7
                  fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                  st = st + 14
                  fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                  st = st + 21
                  fin= st + 6
                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                  if send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==7 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==3 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==5 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 3MHz ' and x3==3 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-4
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value+1
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  else:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value


                  if (x3==y3) and (x4==y4):
                      sheet[y5][j].value = send[' UE'][i]

            elif Band =='LTE B71': # 주파수대역별로 계산 필요
                if (Max_power == 1) and (Hotspot_power == 0) and (back_off_power == 0):
                      if x5 == 133222 or x5==133197 or x5==133172 or x5==133147:
                          y5 = 'E'
                      elif x5 == 133297:
                          y5 = 'F'
                      elif x5 == 133372 or x5==133397 or x5==133172 or x5==133447:
                          y5 = 'G'

                elif (Max_power == 0) and (Hotspot_power == 1) and (back_off_power == 0):
                     if x5 == 133222 or x5==133197 or x5==133172 or x5==133147:
                          y5 = 'J'
                     elif x5 == 133297:
                          y5 = 'K'
                     elif x5 == 133372 or x5==133397 or x5==133172 or x5==133447:
                          y5 = 'L'


                elif (Max_power == 0) and (Hotspot_power == 0) and (back_off_power == 1):
                      if x5 == 133222 or x5==133197 or x5==133172 or x5==133147:
                          y5 = 'O'
                      elif x5 == 133297:
                          y5 = 'P'
                      elif x5 == 133372 or x5==133397 or x5==133172 or x5==133447:
                          y5 = 'Q'


                #시작 값을 정하고
                #이게 각 밴드마다 전부 다름 그러니까 위치를 하나하나 따는게 좋음
                if send[' BW'][i]== ' 1.4MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 3MHz':  #NOT EXIST
                  st = 136

                elif send[' BW'][i]== ' 5MHz ':
                  st = 105

                elif send[' BW'][i]== ' 10MHz ':
                  st = 74

                elif send[' BW'][i]== ' 15MHz ':
                  st = 43

                elif send[' BW'][i]== ' 20MHz ':
                  st = 12



                #여기서 부터 모드별로 시작과 끝을 정함
                if send[' Mode'][i]== ' QPSK ':
                  fin=st+6
                elif send[' Mode'][i]== ' 16QAM ':
                  st = st + 7
                  fin= st + 6
                elif send[' Mode'][i]== ' 64QAM ':
                  st = st + 14
                  fin= st + 6
                elif send[' Mode'][i]== ' 256QAM ':
                  st = st + 21
                  fin= st + 6
                #결측값 보정 해주는 코드 임 다른 밴드에서 고장난 부분이 있으면 추가해서 디버깅 할것
                for j in range(st,fin+1):
                  if send[' BW'][i]== ' 1.4MHz ' and x3==1 and x4==7 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==3 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 1.4MHz ' and x3==8 and x4==5 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 3MHz ' and x3==1 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 3MHz ' and x3==3 and x4==2 :
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4 == 6:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 5MHz ' and x3==12 and x4==11:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 10MHz ' and x3==1 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 10MHz ' and x3==25 and x4==24:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==18:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-2
                  elif send[' BW'][i]== ' 15MHz ' and x3==36 and x4==35:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-4
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==25:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value+1
                  elif send[' BW'][i]== ' 20MHz ' and x3==50 and x4==49:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value-1
                  else:
                      y3 = sheet['C'][j].value
                      y4 = sheet['D'][j].value


                  if (x3==y3) and (x4==y4):
                      sheet[y5][j].value = send[' UE'][i]



#만든 파일에 그대로 덮어 씌움
        target.save(get_name)
        print('Finish')

###############################################################################

    def chkFunction(self):
        global Max_power
        global Hotspot_power
        global back_off_power

        if self.max_chk.isChecked():
            Max_power =1
            print(Max_power)
        if self.hot_chk.isChecked():
            Hotspot_power =1
            print(Hotspot_power)
        if self.back_chk.isChecked():
            back_off_power =1
            print(back_off_power)
        if self.max_chk.isChecked() != True:
            Max_power =0
            print(Max_power)
        if self.hot_chk.isChecked() != True:
            Hotspot_power =0
            print(Hotspot_power)
        if self.back_chk.isChecked() != True:
            back_off_power =0
            print(back_off_power)
########################################################################

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

##########################################################################


    def OnOpenDocument(self):
        fname1 = QFileDialog.getOpenFileName(self, 'Open file', "",
                                            "All Files(*);; Python Files(*.py);; CSV Files(*.csv)", '/home')

        global send_name
        send_name = fname1[0]
        self.send_box.setText(fname1[0])
        print(send_name)

    def OnOpenDocument2(self):
        fname2 = QFileDialog.getOpenFileName(self, 'Open file', "",
                                            "All Files(*);; Python Files(*.py);; CSV Files(*.csv)", '/home')
        global get_name
        get_name = fname2[0]
        self.get_box.setText(fname2[0])
        print(get_name)

###################################################################
#실행

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
