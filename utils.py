import re
import logging


def is_month_pattern(month):
    """判断是否符合月份格式"""
    pattern = r'^20\d{2}-\d{1,2}$'
    if re.match(pattern, month):
        return True
    else:
        return False
    

def is_later_month(later: str, current: str):
    """判断later月份是否较current更晚"""
    if is_month_pattern(later) and is_month_pattern(current):

        later_year = int(later.split('-')[0])
        current_year = int(current.split('-')[0])

        later_month = int(later.split('-')[1])
        current_month = int(current.split('-')[1])

        if (later_year >= current_year) and (later_month > current_month):
            return True
        else:
            return False
    else:
        logging.getLogger('report').warning('不规则的月份目录名称')
        return False


def get_latest_month(monthes: list):
    """获取最晚的月份"""
    latest_month = None
    for month in monthes:  # 先随便找一个月份
        if is_month_pattern(month):
            latest_month = month
            break
    # 再找最晚的月份
    for month in monthes:
        if is_month_pattern(month):
            if is_later_month(month, latest_month):
                latest_month = month
    
    return latest_month
