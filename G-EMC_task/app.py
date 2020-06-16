from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wsgi import LimitedStream
import pandas as pd
import uuid
import os
import json

# 엑셀 보고서 생성
from sample_excel import *
from convert import *
from time_cal import *
from auto_rf3 import *

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rkwlswk1'
app.config['MYSQL_DATABASE_DB'] = 'UserList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Default setting
pageLimit = 5


app.config['UPLOAD_FOLDER'] = 'static/Uploads'

#미들웨어 구현 개시[s]
@app.after_request
def add_header(resp):
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp
#미들웨어 구현 개시[e]

@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':

        # 업로드 파일 처리 분기
        file = request.files['csv']
        if not file: return render_template('ml_pre.html', ml_label="No Files")

        df = pd.read_csv(file)

@app.route('/ml_predict')
def showPredict():
    return render_template('ml_pre.html')


#@app.route('/popup')
#def popup():
#    return render_template('popup.html')

@app.route('/')
def popup():
    return render_template('popup.html') #index.html

@app.route('/main')
def main():
    if session.get('user'):
        print(session.get('user'))
        session.pop('user', None)
        print(session.get('user'))
    return render_template('main_s.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

###### RF ###########
@app.route("/uploadFile", methods=['POST'])
def uploadFile():
    #try
    print('uploadFile')
    conList = []
    conList = request.form['conList']
    con_result = json.loads(conList) # json stringify로 전송된 데이터를 다시 파싱해서 읽는 방법

    fileList = []
    fileList = request.form['fileList']
    file_result = json.loads(fileList) # json stringify로 전송된 데이터를 다시 파싱해서 읽는 방법


    size = len(con_result)
    interface(con_result,file_result)
    return 'success'


@app.route("/taskprac_rf",methods=['POST'])
def taskprac_rf():
    #try
    mid = request.form['mID']
    conn = mysql.connect()
    cursor = conn.cursor()

    # tbl_wish에서 standard 컬럼 가져오기
    cursor.callproc('sp_GetStd',(mid,))
    std = cursor.fetchall()
    std = std[0]
    std = std[0] # 일부러 두번 한것임

    std = std.replace('[','')
    std = std.replace(']','')
    std_list = std.split(',')   # 이거 보내면 된다.
    print('list:',std_list)

    # 해당하는 컬럼(1) 인 경우는 tbl_standard에서 저장된 데이터 가져오기
    get_std=[[] for _ in range(3)]
    for idx,a in enumerate(std_list):
        if a=='1':
            cursor.callproc('sp_GetStd_sub',(mid,idx))
            res = cursor.fetchall()
            get_std[idx] = res
    print(get_std)
    cursor.close()
    conn.close()
    print(get_std[0])

    _get_std_0 = ""
    _get_std_1 = ""
    _get_std_2 = ""
    print(get_std[1], type(get_std[1]))

    for z in range(3):
        if z==0 and get_std[z] != '[]':
            _get_std_0 = str(get_std[0]).replace("(('[","")
            _get_std_0 = _get_std_0.replace("]',),)","")

        elif z==1 and get_std[z] != []:
            print("18")
            _get_std_1 = str(get_std[1]).replace("(('[","")
            _get_std_1 = _get_std_1.replace("]',),)","")

        elif z==2 and get_std[z] != []:
            _get_std_2 = str(get_std[2]).replace("(('[","")
            _get_std_2 = _get_std_2.replace("]',),)","")


    standard_dict = {
        'std_part':std_list,
        'fcc':_get_std_0,
        'ce':_get_std_1,
        'kc':_get_std_2
    }

    print("fccccccccccc",_get_std_0)
    return json.dumps(standard_dict)

@app.route('/standardSave',methods=['POST'])
def standardSave():
    #try
    conn = mysql.connect()
    cursor = conn.cursor()

    wish_id = request.form['wish_id']
    std = request.form['standard']
    fcc = request.form['fcc']
    ce = request.form['ce']
    kc = request.form['kc']

    std_list = std.split(',')
    fcc_list = fcc.split(',')
    ce_list = ce.split(',')
    kc_list = kc.split(',')
    print(len(std_list))

    # update 하는 프로시저를 구현해야 한다.
    _standard = [0 for _ in range(3)]
    for i in std_list:
        if 'fcc' in i:
            _standard[0]=1
        elif 'ce' in i:
            _standard[1]=1
        elif 'kc' in i:
            _standard[2]=1

    _fcc = [0 for _ in range(3)]
    for i in fcc_list:
        if 'power' in i:
            _fcc[0]=1
        elif 'con' in i:
            _fcc[1]=1
        elif 'rad' in i:
            _fcc[2]=1

    _ce = [0 for _ in range(4)]
    for i in ce_list:
        if 'power' in i:
            _ce[0] = 1
        elif 'tx' in i:
            _ce[1] = 1
        elif 'rx' in i:
            _ce[2] = 1
        elif 'rad' in i:
            _ce[3] = 1

    _kc = [0 for _ in range(4)]
    for i in kc_list:
        if 'power' in i:
            _kc[0] = 1
        elif 'nor' in i:
            _kc[1] = 1
        elif '3' in i:
            _kc[2] = 1
        elif 'rad' in i:
            _kc[3] = 1

    cursor.callproc('sp_standardSave',(wish_id, str(_standard)))
    conn.commit()

    print('? here ? ')
    condition_3 = [_fcc, _ce, _kc]
    for idx,i in enumerate(_standard):
        if i==1:
            cursor.callproc('sp_standardSave_det',(wish_id,idx,str(condition_3[idx])))
            conn.commit()

    cursor.close()
    conn.close()

    return "success"

@app.route('/goprac_rf', methods=['POST'])
def goprac_rf():
    #try
    wish_id = request.form['mID']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.callproc('sp_GetStandard',(wish_id,))
    data = cursor.fetchall()

    cur_data = str(data[0]).replace("('[","")
    cur_data = cur_data.replace("]',)","")

    result_dict = {'standard': str(cur_data)}

    return json.dumps(result_dict)



#################### 쿠팡
@app.route("/coupang",methods=['POST'])
def coupang():
    #try
    mid = request.form['mID']
    r = request.form['r']
    v = request.form['v']

    con = mysql.connect()
    cursor = con.cursor()

    query = "SELECT modes_process,modes_complete FROM tbl_modes WHERE model_id=%s AND regulation=%s AND modes_name=%s"
    value = (mid,r,v)

    cursor.execute(query,value)
    data = cursor.fetchall()

    cursor.close()
    con.close()

    data = data[0] # 튜플기호 벗기려고
    whole_mode= data[0][:-1]
    whole_mode = str(whole_mode).replace('"',"")
    whole_mode = str(whole_mode).replace("'","")

    completed = data[1]
    completed = str(completed).replace('"',"")
    completed = str(completed).replace("'","")
    completed = str(completed).replace('[',"")
    completed = str(completed).replace("]","")
    completed = str(completed).replace(' ',"")

    return str(whole_mode) + '@' + str(completed)


@app.route('/coupang_detail', methods=['POST'])
def coupang_detail(): # sample_excel.py랑 이어지게 해야한다.
    #try
    model_id = request.form['mID']
    r = request.form['r']
    v = request.form['v']

    f_name = request.form['file_name'] # 그냥 이건그때마다 file_name ? 이전에 저장했던 file_name도 불러와.?
    array = request.form['checked']

    # 자 일단 해당 mode에 대한 걸 저장해야겠지
    con = mysql.connect()
    cursor = con.cursor()

    query = "SELECT modes_id, modes_process FROM tbl_modes WHERE model_id=%s AND regulation=%s AND modes_name=%s"
    print(model_id,r,v)
    value = (model_id,r,v)

    cursor.execute(query,value)
    data = cursor.fetchall()

    data = data[0]
    modes_id = data[0]

    proc = data[1]
    proc_list = proc.split(',')
    proc_list = proc_list[:-2]

    array_list = array.split(',')
    complete_array=[]

    for i in range(len(proc_list)): # 계획한 모든 시험모드
        for j in array_list: # 현재 완료한 시험모드
            if proc_list[i] == j:
                complete_array.append(j)

    query = "UPDATE tbl_modes SET modes_complete=%s WHERE modes_id=%s;"

    value = (str(complete_array),modes_id)
    cursor.execute(query,value)
    con.commit()

    query = "SELECT wish_title,mode_num FROM tbl_wish WHERE wish_id=%s"
    value = (model_id)
    cursor.execute(query,value)
    wish_title = cursor.fetchall()


    wish_title = wish_title[0]

    user_defined_Fname = list(wish_title)[0]

    query = "SELECT modes_id FROM tbl_modes WHERE model_id=%s;"
    value = (model_id)
    cursor.execute(query,value)
    mode_num = cursor.fetchall()
    cursor.close()
    con.close()
    print(mode_num, "::::::::::::::::::::::::::::",len(mode_num))
    count = len(mode_num)

    print("???????????????????????????????")

    update_excel(user_defined_Fname,count,r,v,complete_array)
    #t = convert(complete_array)
    return "성공" # true 리턴하면 예측일 머신러닝 돌리는 코드 동작하도록.

##################### prac : mode process 설정

@app.route('/checkMode', methods=['POST'])
def checkMode():
    #try
    model_id = request.form['model_id']
    r = request.form['regulation']
    v = request.form['mode']

    con = mysql.connect()
    cursor = con.cursor()

    query = "SELECT modes_id FROM tbl_modes WHERE model_id=%s AND regulation=%s AND modes_name=%s"
    value = (model_id,r,v)

    cursor.execute(query,value)
    data = cursor.fetchall()
    cursor.close()
    con.close()

    print(">",data)
    if data!=():
        return str(True)
    return str(False)

@app.route('/modeProcessSave',methods=['POST'])
def modeProcessSave():
    try:
        _id=session.get('user')
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
        value = _id
        cursor.execute(query,value)
        data = cursor.fetchall()
        user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴

        by_user = user_name
        model_id = request.form['model_id']
        r = request.form['model_regulation']
        v = request.form['model_mode']
        proc = request.form['mode_process']
        created = request.form['created']
        print(created)

        #connect to MySQL
        con = mysql.connect()
        cursor = con.cursor()


        # 먼저 비슷한 이름의 mode를 이전에 생성한 적이 있는지 체크
        check_query = "SELECT * FROM tbl_modes WHERE model_id=%s AND regulation=%s AND modes_name=%s;"
        check_value = (model_id,r,v)
        cursor.execute(check_query,check_value)
        check_data = cursor.fetchall()

        if check_data == (): #아예 처음임 이 모드

            query = "INSERT INTO tbl_modes (model_id,regulation,modes_name,modes_process,created,by_user)"
            query += "VALUES ( %s,%s,%s,%s,%s,%s);"

            print(query)
            value = (model_id,r,v,proc,created,by_user)
            cursor.execute(query,value)
            con.commit()


        else: # 이전에 이 모드 생성한 적이 있음
            print(check_data)
            if check_data[0][4] == proc:
                return "이미 같은 내용을 저장했습니다."
            else:
                # 변경사항 있음. 수정
                query = "UPDATE tbl_modes SET modes_process=%s,created=%s,by_user=%s WHERE model_id=%s AND regulation=%s AND modes_name=%s;"

                value = (proc,created,by_user,model_id,r,v)
                cursor.execute(query,value)
                con.commit()

    finally:
        query = "SELECT wish_title,mode_num FROM tbl_wish WHERE wish_id=%s"
        value = (model_id)
        cursor.execute(query,value)
        wish_title = cursor.fetchall()
        wish_title = wish_title[0]
        print(wish_title)
        user_defined_Fname = list(wish_title)[0]

        query = "SELECT modes_id FROM tbl_modes WHERE model_id=%s;"
        value = (model_id)
        cursor.execute(query,value)
        mode_num = cursor.fetchall()
        print(mode_num, "::::::::::::::::::::::::::::",len(mode_num))
        count = len(mode_num)

        # 여기서 값을 업데이트 하기 전에 엑셀파일이 열려있지는 아는지 확인해야 한다.
        try:
            myfile_name = user_defined_Fname + ".xlsx"
            myfile = open(myfile_name, "r+")
            myfile.close()
            print("myfile",myfile_name)
        except IOError:
            print("열려있다")
            return "엑셀 파일이 열려있으니, 닫고 다시 실행해주세요."
        uquery = "UPDATE tbl_wish SET mode_num=mode_num+1 WHERE wish_id=%s;"
        uvalue = (model_id)

        cursor.execute(uquery,uvalue)
        con.commit()

        cursor.close()
        con.close()
        print(">>>>>>>>>>>>>>>>>>>>>>>",count)
        add_excel (user_defined_Fname,count,r,v) # 모드 추가?
        return "DB 성공"

@app.route('/prac_progress')
def prac_progress():
    return render_template('prac_progress.html')

@app.route('/showAddWish')
def showAddWish():
    _id=session.get('user')
    # connect to mysql

    con = mysql.connect()
    cursor = con.cursor()

    query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
    value = _id
    cursor.execute(query,value)
    data = cursor.fetchall()
    user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴
    cursor.close()
    con.close()
    return render_template('addWish.html',user_name=user_name)

@app.route('/addUpdateLike',methods=['POST'])
def addUpdateLike():
    try:
        if session.get('user'):
            _wishId = request.form['wish']
            _like = request.form['like']
            _user = session.get('user')


            conn = mysql.connect()
            cursor = conn.cursor()

            query = "SELECT user_name FROM tbl_user WHERE user_id=%s;"
            value = (_user)
            cursor.execute(query,value)
            _name = cursor.fetchall()

            _name = _name[0]
            _name = _name[0] # 일부러 두번한것임

            cursor.callproc('sp_AddUpdateLikes',(_wishId,_user,_like))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()

                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_getLikeStatus',(_wishId))

                result = cursor.fetchall()
                likeStatus = []
                for i in range(len(result)):
                    cursor.callproc('sp_getUsername',(result[i]))
                    whoLike = cursor.fetchall()
                    likeStatus.append(whoLike)
                    #print(whoLike)

                print('current_wish_like_users',likeStatus)

                return json.dumps({'status':'OK','likeStatus':likeStatus})
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()



@app.route('/getAllWishes')
def getAllWishes():
    try:
        if session.get('user'):
            _user = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            print(type(_user))
            cursor.callproc('sp_GetAllWishes',(_user+1000000,)) # 만든이는 안보여서 그럼 근데
            result = cursor.fetchall()
            print('getttttttttttttttttt')
            print(result)
            print(type(result))

            wishes_dict = []
            _id = 0
            for wish in result:
                _id = wish[0]
                print('wish')
                print(wish)

                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'FilePath': wish[3],
                        'Like':wish[4],
                        'HasLiked':wish[5],#likeStatus,
                        'rate':wish[6]} # 프로그레스


            #print("?????????????",_wishId,type(_wishId))
                # 프로그레스 계산
                cursor.callproc('sp_getAllModes',(_id,)) #ㄹㄴㅇㅁ ㄹㄴㅁㅇㄱ';ㅎㅍㄹ'
                total_mode_num = cursor.fetchall()
                rate = 0
                print(type(total_mode_num))
                if total_mode_num==(0,):
                    continue

                total_mode_num = total_mode_num[0]
                print("zzzzzzzzzzzzzzzzzzzzzz",total_mode_num)
                total_mode_num = list(total_mode_num)

                if total_mode_num[0] !=0:
                    query = "SELECT modes_complete, modes_process FROM tbl_modes WHERE model_id=%s;"
                    value = (_id)
                    cursor.execute(query,value)
                    div = cursor.fetchall()
                    for q in range(total_mode_num[0]):
                        print(div[q])
                        cp = div[q][0]
                        wp = div[q][1]
                        if cp == None: continue
                        print(cp,type(cp))
                        cp = cp.replace('[','')
                        cp = cp.replace(']','')
                        cp_list = cp.split(',')
                        print(wp,type(wp))
                        wp_list = wp.split(',')

                        print(len(cp_list),len(wp_list))

                        rate += (len(cp_list)/len(wp_list)) * (1/total_mode_num[0]) *100
                    print("rate:",rate)


                cursor.callproc('sp_getLikeStatus',(_id,))

                result = cursor.fetchall()
                print("-----------------------------------------")
                print(result)
                likeStatus = []
                for i in range(len(result)):
                    cursor.callproc('sp_getUsername',(result[i]))
                    whoLike = cursor.fetchall()
                    likeStatus.append(whoLike)
                    #print(whoLike)

                print('current_wish_like_users',likeStatus)
                wish_dict['HasLiked'] = likeStatus#json.dumps(likeStatus)
                wish_dict['rate'] = rate
                wishes_dict.append(wish_dict)



            print(wishes_dict)
            # rate도 마지막에 첨가했으면 좋겠다.
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/showDashboard')
def showDashboard():
    if session.get('user'):
        _id=session.get('user')
        print(_id)
    # connect to mysql
        print("show DBS")

        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
        value = _id
        cursor.execute(query,value)
        data = cursor.fetchall()
        user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴
        cursor.close()
        con.close()
        return render_template('dashboard.html',user_name = user_name)
    else:
        return render_template('main_s.html',message='로그인을 해야 접속할 수 있어요!')


@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        _id=session.get('user')
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
        value = _id
        cursor.execute(query,value)
        data = cursor.fetchall()
        user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴
        cursor.close()
        con.close()
        return render_template('userHome.html',user_name=user_name)
    else:

        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        _id=session.get('user')
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
        value = _id
        cursor.execute(query,value)
        data = cursor.fetchall()
        user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴
        cursor.close()
        con.close()
        return render_template('userHome.html',user_name=user_name)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/prac')
def prac():
    if session.get('user'):
        print("---------------")
        _id=session.get('user')

        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT user_name FROM tbl_user WHERE user_id = %s"
        value = _id
        cursor.execute(query,value)
        data = cursor.fetchall()
        user_name = data[0][0]  # id를 이용해서 db에서 해당하는 user_name을 읽어옴
        cursor.close()
        con.close()

        return render_template('prac.html',user_name = user_name)
    else:
        return render_template('main_s.html',message='로그인을 해야 접속할 수 있어요!')


@app.route('/pracModel', methods=['POST'])
def pracModel():
    print("pracmodel")
    try:
        #if session.get('user'): #로그인 된 상태이면
        _model_id = request.form['mID']
        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()

        query = "SELECT wish_title FROM tbl_wish WHERE wish_id = %s"
        value = _model_id
        cursor.execute(query,value)
        data = cursor.fetchall()
        model_name=str(data[0])
        model_name=model_name.replace("(","")
        model_name=model_name.replace(")","")
        model_name=model_name.replace(",","")
        print(">>>>>>>>>",model_name)

        query = "SELECT regulation,modes_name,modes_process,modes_complete FROM tbl_modes WHERE model_id=%s"
        value = _model_id
        cursor.execute(query,value)
        data = cursor.fetchall()
        print(data)

        size = len(data)
        answer = model_name + ":"
        convert_array=[]
        for i in range(size):
            sub = data[i][0]
            sub += "-"
            sub += data[i][1]
            sub += "@"
            sub += data[i][2]
            #sub += "$"
            #sub += data[i][3] # completed Mode

            sub_convert = data[i][2].split(',')

            convert_array.append(sub_convert[:-1])
            sub += "&"
            answer += sub
        #print(answer)

        print("/////////////////////////////////////////",convert_array)
        predict_time = convert(convert_array)
        print(predict_time)
        res = cal_time(predict_time) # 머신러닝 예측

        import copy
        str_res = copy.deepcopy(res)
        aa = str(str_res).split(' ')
        print(aa[0])

        print("iod",_model_id)
        print(type(aa[0]),type(_model_id))
        cursor.callproc('sp_predictTime',(aa[0],int(_model_id)))
        con.commit()
        print("predict Time success")



        #print("-------------------------------------------------",res)
        answer += '!' + str(res)
        print(res)
        print(answer)
        cursor.close()
        con.close()

        return answer
        #else:
            #return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})

@app.route('/stateSave', methods=['POST'])
def stateSave():
    #try
    wish_id = request.form['wish_id']
    update_state = request.form['state']
    print("update:",update_state)
    con = mysql.connect()
    cursor = con.cursor()

    idx=4
    update_state = update_state.split(',')
    for st in update_state:
        print(st)
        try:
            if st=='emc':
                idx=0
            elif st=='rf':
                idx=1
            elif st=='rpt':
                idx=2
            elif st=='cy' :
                idx=3
            print('idx',idx)
        finally:
            cursor.callproc('sp_stateSave',(wish_id,idx))
            con.commit()

    cursor.close()
    con.close()
    return '성공'

@app.route('/stateprac', methods=['POST'])
def stateprac():
    #try
    wish_id = request.form['wish_id']

    con = mysql.connect()
    cursor = con.cursor()
    cursor.callproc('sp_prediction',(wish_id))
    data = cursor.fetchall()

    cursor.callproc('sp_state',(wish_id))
    state = cursor.fetchall()

    cursor.close()
    con.close()

    data = data[0]
    created = data[0]
    predicted = data[1]

    created = str(created).split(' ')[0]

    state = state[0]
    print(state)
    state_dict={
        'Created':created,
        'Predicted':predicted,
        'State':list(state)
    }
    return json.dumps(state_dict)



@app.route('/removeMode',methods=['POST'])
def removeMode():
    #try
    model_id = request.form['model_id']
    r = request.form['model_regulation']
    v = request.form['model_mode']

    query = "DELETE FROM tbl_modes WHERE model_id=%s AND regulation=%s AND modes_name=%s;"
    value = (model_id,r,v)

    # connect to mysql
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query,value)
    con.commit()

    query = "UPDATE tbl_wish SET mode_num=mode_num-1 WHERE wish_id=%s;"
    value = (model_id)

    cursor.execute(query,value)
    con.commit()

    cursor.close()
    con.close()
    return "성공"


@app.route('/makeProcess')
def makeProcess():
    return render_template("ajax_test.html")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteWish',(_id,_user))
            result = cursor.fetchall()

            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):

            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById',(_id,_user))
            result = cursor.fetchall()

            wish = []
            wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2],'FilePath':result[0][3],'Private':result[0][4],'Done':result[0][5]})

            return json.dumps(wish)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/getWish',methods=['POST'])
def getWish():
    try:
        print(session.get('user'))
        if session.get('user'):
            _user = session.get('user')
            _limit = pageLimit
            _offset = request.form['offset']
            _total_records = 0

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,_limit,_offset,_total_records))

            wishes = cursor.fetchall()
            cursor.close()

            cursor = con.cursor()

            cursor.execute('SELECT @_sp_GetWishByUser_3');

            outParam = cursor.fetchall()

            response = []
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4].strftime('%Y-%m-%d, %d:%d:%d')} #json에서 datetime serialize한 특성을 읽지못함.
                wishes_dict.append(wish_dict)
            response.append(wishes_dict)
            response.append({'total':outParam[0][0]})
            print("-------------------")
            print(response)
            return json.dumps(response)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
            if request.form.get('filePath') is None:
                _filePath = ''
            else:
                _filePath = request.form.get('filePath')
            if request.form.get('private') is None:
                _private = 0
            else:
                _private = 1
            if request.form.get('done') is None:
                _done = 0
            else:
                _done = 1

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('sp_addWish',(_title,_description,_user,_filePath,_private,_done))
            data = cursor.fetchall()



            if len(data) is 0:
                conn.commit()
                user_defined_Fname = _title

                import time
                created = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
                print(created)
                query = "SELECT user_name FROM tbl_user WHERE user_id=%s"
                value = (_user)
                cursor.execute(query,value)
                sub_data = cursor.fetchall()


                user_name = sub_data[0]
                user_name = str(user_name).replace("('","")
                user_name = str(user_name).replace("',)","")

                query = "UPDATE tbl_wish SET wish_join=%s WHERE wish_title = %s;"
                value = (user_name, _title)
                cursor.execute(query,value)
                conn.commit()

                print(_title)
                cursor.callproc('sp_addState',(_title,))
                conn.commit()

                cursor.callproc('sp_addStandard',(_title,))
                conn.commit()

                sample_excel(user_defined_Fname,_title,_description,str(user_name),created)
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _wish_id = request.form['id']
            _filePath = request.form['filePath']
            _isPrivate = request.form['isPrivate']
            _isDone = request.form['isDone']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user,_filePath,_isPrivate,_isDone))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        print("----------------------------------------------------")
        print(_username,_password)

        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name=%s AND user_password=%s"
        value = (_username,_password)
        cursor.execute(query,value)
        data = cursor.fetchall()

        cursor.close()
        con.close()


        if len(data) > 0:
            if str(data[0][2])==str(_password):
                session['user'] = data[0][0]
                user_name = data[0][1]
                return redirect('/showDashboard')#render_template('dashboard.html',user_name=user_name)
            else:
                return 'error'# alert로 되도로고 처리하기.
        else:
            return 'error'


    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/signUp',methods=['POST'])
def signUp():

    #_name = request.form['inputEmail']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _email and _password:

        # All Good, let's call MySQL

        conn = mysql.connect()
        cursor = conn.cursor()
        #_hashed_password = _password
        #cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

        query = "SELECT * FROM tbl_user WHERE user_name=%s AND user_password=%s"
        value = (_email,_password)
        cursor.execute(query,value)
        data = cursor.fetchall()
        cursor.close()
        conn.close()


        if len(data) is 0:  # data : 이미 회원인지 아닌지확인하는 코드
            conn = mysql.connect()
            cursor = conn.cursor()

            iquery = "INSERT IGNORE INTO tbl_user (user_name,user_password) VALUES(%s,%s);"
            ivalue = (_email,_password)

            cursor.execute(iquery,ivalue)
            conn.commit()
            print(_email,_password)
            print("00 return ")

            cursor.close()
            conn.close()

            return redirect('/main')

        else:
            print(data)
            return '이미 존재하는 아이디 입니다.'
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})



if __name__ == "__main__":
    app.debug=True
    app.run()
