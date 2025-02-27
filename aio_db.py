import time
import pymysql


def writehalm(m: str, ai_result: str, docktablesname: str):  # halm软件写入脚本
    s = ai_result
    # if ai_result == 'OK':  # 0
    #     s = 0   # 当为正常片时，则传送信号0
    # elif ai_result == "NG":  # 1
    #     s = 1   # 当有严重故障时，则传送信号1
    # else:
    #     s = ud_num   # 当在中间不确认时，则传送信号2
    name = m[:-4]  # -4
    realname = name.split('_')

    n1 = str(realname[-3])  # id  -3
    n2 = str(realname[-2])  # bin  -2
    n3 = str(realname[-1])  # mose  -1

    db = pymysql.connect(host='localhost', port=3306, user='root', password='303631ZFMzfm@', db='ak_aidata',
                         use_unicode=True, charset="utf8")  # ak_aidata 写死
    db.autocommit(True)
    cursor = db.cursor()

    sql0 = "SELECT  *  FROM " + docktablesname + " WHERE  waferID = %s "  # aidata_a aidata_b
    try:
        # print(n1)
        cursor.execute(sql0, (n1))
        result = cursor.fetchone()
        # print("result",result)
        # print('查询信息成功')
        # db.commit()
    except Exception as e:
        print('查询信息失败')
        print(e)
    ticks = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当前时间戳
    if result is None:
        # print("该数据不存在")
        sql1 = "INSERT INTO " + docktablesname + "(EL_originalname, EL_worktime, waferID, halmbin, color, EL_results) VALUES (%s, %s, %s,  %s,%s, %s)"
        try:
            # 执行SQL语句
            cursor.execute(sql1, (m, ticks, n1, n2, n3, s))
            print('该数据不存在，对接信息插入成功')
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print('该数据不存在，对接信息插入数据失败')
            # db.rollback()
            print(e)

            # pass
    else:
        # print("该数据存在")
        sql1 = "UPDATE " + docktablesname + " SET  EL_originalname = %s, EL_worktime = %s, halmbin = %s,  color = %s,EL_results = %s WHERE waferID = %s"

        try:
            # 执行SQL语句
            cursor.execute(sql1, (m, ticks, n2, n3, s, n1))
            print('对接数据更新成功')
            # 提交修改
            db.commit()
        except:
            # 发生错误时回滚
            print('对接数据更新失败')
            print(e)

        # cursor.close()
    linenum = cursor.execute("select id from  " + docktablesname)
    # linenum = len(cursor.fetchall())
    # print('linenum, dockdatanum', linenum, dockdatanum)
    # """

    if linenum > 50:  # 50
        # db = pymysql.connect(host='127.0.0.1', port=3306, user='root', db='ak_aidata', use_unicode=True,charset="utf8")
        # cursor = db.cursor()
        one_line = cursor.fetchone()
        # print(one_line)
        # print(one_line[0])
        sql = "DELETE FROM " + docktablesname + " WHERE id= '%d' " % (one_line[0])
        # sql = "delete from " + sqlname + "where 1 limit 0"
        try:
            cursor.execute(sql)
            # print('删除对接数据成功')
            # db.commit()
        except:
            # 发生错误时回滚
            print('删除对接数据失败')
            db.rollback()
            pass
    cursor.close()
    # 关闭连接
    db.close()
    # """
