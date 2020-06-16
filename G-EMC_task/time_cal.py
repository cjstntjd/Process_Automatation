import time
from datetime import datetime, timedelta

def cal_time(h):

    now = datetime.utcnow()

    t = ['월','화','수','목','금','토','일']
    n = time.localtime().tm_wday
    y = t[n]
    day_cnt=0

    while h>=0:
        if y =='월':
            h-=5
            y='화'
            day_cnt+=1
        elif y =='화':
            h-=5
            y='수'
            day_cnt+=1
        elif y =='수':
            h-=5
            y='목'
            day_cnt+=1
        elif y =='목':
            h-=5
            y='금'
            day_cnt+=1
        elif y =='금':
            h-=5
            y='토'
            day_cnt+=1
        elif y =='토':
            y='일'
            day_cnt+=1
        elif y =='일':
            y='월'
            day_cnt+=1

    return(now + timedelta(days=day_cnt))
