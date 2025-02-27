import time

import pymysql


def writehalm_ak_secaidata(m: str, ai_result: str, docktablesname: str):  # halm软件写入脚本
    s = ai_result

    name = m[:-4]  # -4
    realname = name.split('_')

    n1 = str(realname[-3])  # wafer_id  -3
    n2 = str(realname[-2])  # bin  -2

    if n2 == "102":
        s = "NG102"  # NG102 bin
    elif n2 == "108":
        s = "NG108"  # NG108 bin
    else:
        if ai_result == 0:
            s = "OK"  # 当为正常片时，则传送信号OK
        elif ai_result == 1:
            s = "NG"  # 当为NG片时，则传送信号NG

    db = pymysql.connect(host='localhost', port=3306, user='root', password='303631ZFMzfm@', db='ak_secaidata',
                         use_unicode=True, charset="utf8")
    db.autocommit(True)
    cursor = db.cursor()

    ticks = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当前时间戳

    # sql1 = "INSERT INTO " + docktablesname + "(EL_originalname, EL_worktime, waferID, halmbin, color, EL_results) VALUES (%s, %s, %s,  %s,%s, %s)"
    #                                                   m名称       ticks时间      n1       n2      n3     s
    sql1 = "INSERT INTO " + docktablesname + "(wafer_id, photo_id, work_time, grade) VALUES (%s, %s, %s, %s)"
    try:
        # 执行SQL语句
        cursor.execute(sql1, (n1, name, ticks, s))
        print('结果写入成功！')
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        print('结果写入失败！')
        # db.rollback()
        pass
    
    cursor.close()
    # 关闭连接
    db.close()
    # """

def writehalm_ak_secokaidata(c: str,m: str, ai_result: str, docktablesname: str):  # halm软件写入脚本
    s = ai_result

    name = m[:-4]  # -4
    realname = name.split('_')
    n1 = str(realname[-3])  # wafer_id  -3

    if c == "EL_OK_22.6":
        s = "EL_OK_DX"  # EL_OK_DX bin
    else:
        if ai_result == 0:
            s = "OK"  # 当为正常片时，则传送信号OK
        elif ai_result == 1:
            s = "NG"  # 当为NG片时，则传送信号NG

    db = pymysql.connect(host='localhost', port=3306, user='root', password='303631ZFMzfm@', db='ak_secokaidata',
                         use_unicode=True, charset="utf8")
    db.autocommit(True)
    cursor = db.cursor()

    ticks = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当前时间戳

    # sql1 = "INSERT INTO " + docktablesname + "(EL_originalname, EL_worktime, waferID, halmbin, color, EL_results) VALUES (%s, %s, %s,  %s,%s, %s)"
    #                                                   m名称       ticks时间      n1       n2      n3     s
    sql1 = "INSERT INTO " + docktablesname + "(wafer_id, photo_id, work_time, grade) VALUES (%s, %s, %s, %s)"
    try:
        # 执行SQL语句
        cursor.execute(sql1, (n1, name, ticks, s))
        print('结果写入成功！')
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        print('结果写入失败！')
        # db.rollback()
        pass
    
    cursor.close()
    # 关闭连接
    db.close()
    # """
