import sys

sys.path.append('/home/ai_data/JW_Yue/my_work')
sys.path.append('/home/ai_data/JW_Yue/my_work')
from my_work_test import train_values
from my_train import classnames


def ll():
    traindatapath, check_out, annotations_dir = train_values()
    ll = classnames(annotations_dir=annotations_dir)
    return ll


def tt():
    traindatapath, check_out, annotations_dir = train_values()
    classname_list = classnames(annotations_dir=annotations_dir)
    tt = tuple(classname_list)
    return tt
tt = tt()
print(tt)
