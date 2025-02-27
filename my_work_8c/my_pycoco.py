import os
import shutil
import subprocess

subprocess.call("chmod +x /home/ai_data/JW_Yue/my_work_8c/coco.sh", shell=True)
subprocess.call("/home/ai_data/JW_Yue/my_work_8c/coco.sh", shell=True)
print(os.getcwd())
