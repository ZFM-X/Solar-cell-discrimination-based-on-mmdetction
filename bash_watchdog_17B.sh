#查找指定进程的PID
while true;do

    find_name=17B #s_app就是要查找的进程名称
    pid_val=`ps -ef | grep pipline_name | grep $find_name | grep -v grep | awk '{print $2}'`
    if [ $pid_val > 0 ]
    then
        :
        # echo "查找的进程存在,对应的PID=${pid_val}"
    else
        cd /home/aiuser/workspace/mmlab/el_infer_online
        /home/aiuser/miniconda3/envs/mmlab/bin/python main.py --config_file ./config_online.yaml --pipline_name 17B &
        echo "查找的进程不存在"
    fi
done
