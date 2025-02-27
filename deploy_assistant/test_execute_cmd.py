"""

tasklist /v | findstr "aio_main_win.py --pipeline_name"

"""

import os

# git clone http://172.16.97.177:3000/YQ_Wang/el_infer_online.git & \
cmd = """D: & \
cd D:\\AI2 & \
git clone http://172.16.97.177:3000/YQ_Wang/el_infer_online.git & \
"""

request_execute_cmd(filename='20221122_test\\latest.pth', ip='172.21.17.33')


#git.exe pull --progress -v --no-rebase "origin" & \

# os.system(cmd)

# ps = os.popen("tasklist /v | findstr \"python\" | findstr \"32416\"").read()


# ps = os.popen("tasklist /v | findstr \"python\"").read()
# print(ps)
# while ('  ' in ps):
#     ps = ps.replace('  ', ' ')
# print()
# pid = [r.split(' ')[1] for r in ps.split('\n') if len(r) > 0]

# # taskkill -PID 32416 -F
# pid = ['32416']
# for p in pid:
#     cmd = f'taskkill -PID {p} -F'
#     r = os.system(cmd)
# print()
