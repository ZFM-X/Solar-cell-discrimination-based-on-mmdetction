"""
生成图片脚本
"""
import os
import time

count = 0
# src = r"F:\peter_share\etl_data_flat_freeze"
# src = r"\\172.21.17.33\peter_share\etl_data_flat_freeze"
src = r"\\172.21.17.237\ubuntu18_share\save1"
for png in os.listdir(src):
    print(png)
    with open(os.path.join(src, png), 'rb') as f:
        c = f.read()
        
        dst = os.path.join(r'observer_test\02A\aa\EL_NG\aa', png)
        if os.path.exists(dst):
            os.remove(dst)
        with open(dst, 'wb') as t:
            t.write(c)
        
        if int(count / 100) % 2 == 0:
            dst = os.path.join(r'observer_test\02A2\aa\EL_NG\aa2', png)
            if os.path.exists(dst):
                os.remove(dst)
            with open(os.path.join(r'observer_test\02A2\aa\EL_NG\aa2', png), 'wb') as t:
                t.write(c)

        dst = os.path.join(r'observer_test\02B\aa\EL_NG\aa', png)
        if os.path.exists(dst):
            os.remove(dst)
        with open(os.path.join(r'observer_test\02B\aa\EL_NG\aa', png), 'wb') as t:
            t.write(c)

        if int(count / 100) % 2 == 0:
            dst = os.path.join(r'observer_test\02B2\aa\EL_NG\aa2', png)
            if os.path.exists(dst):
                os.remove(dst)
            with open(os.path.join(r'observer_test\02B2\aa\EL_NG\aa2', png), 'wb') as t:
                t.write(c)
    
    time.sleep(2)
    count += 1
