import os
import datetime
import json
import time
import threading
import shutil

import flask


app = flask.Flask(__name__)

src_base = '\\\\172.16.97.177\\model'
dst_base = 'D:\\AI2\\model'


def py_copy_file(src_file, dst_file):
    folder = '\\'.join(dst_file.split('\\')[:-1])
    if not os.path.exists(folder):
        os.makedirs(folder)
    shutil.copyfile(src_file, dst_file)


def exec_cmd(cmd):
    output = os.system(cmd)


@app.route("/execute_cmd", methods=["POST"])
def execute_cmd():

    data = {"success": False, 'output': None}

    if flask.request.method == 'POST':
        if flask.request.content_type.startswith('application/json'):
            cmd = flask.request.json.get('cmd')
            async_exec = flask.request.json.get('async_exec')
            
            if async_exec:
                thread_ = threading.Thread(target=exec_cmd, args=(cmd, ))
                thread_.start()
                # output = os.system(cmd)
                output = f'async_exec: {cmd}...'
            else:
                output = os.popen(cmd).read()

            data['success'] = True
            data['output'] = output

    return flask.jsonify(data)


@app.route("/copy_file", methods=["POST"])
def copy_file():

    global src_base, dst_base

    data = {"success": False, "filename": ''}

    if flask.request.method == 'POST':
        if flask.request.content_type.startswith('application/json'):
            filename = flask.request.json.get('filename')

            src_file = os.path.join(src_base, filename)
            dst_file = os.path.join(dst_base, filename)

            thread_copy_file = threading.Thread(target=py_copy_file, args=(src_file, dst_file ))
            thread_copy_file.start()

            data['success'] = True
            data['filename'] = filename

    return flask.jsonify(data)


@app.route("/is_complete_copy_file", methods=["POST"])
def is_complete_copy_file():

    global src_base, dst_base

    data = {"success": False, 'src_file_size': -1, 'dst_file_size': -1, 'is_complete': False}

    if flask.request.method == 'POST':
        if flask.request.content_type.startswith('application/json'):
            filename = flask.request.json.get('filename')

            src_file = os.path.join(src_base, filename)
            dst_file = os.path.join(dst_base, filename)

            src_file_size = os.path.getsize(src_file)
            dst_file_size = os.path.getsize(dst_file)

            data['success'] = True
            data['src_file_size'] = src_file_size
            data['dst_file_size'] = dst_file_size
            if data['src_file_size'] == data['dst_file_size']:
                data['is_complete'] = True
            
    return flask.jsonify(data)

# 上传文件
@app.route('/sendfile',methods=['POST'])
def send_file():
    file = flask.request.files.get('file')
    if file is None:
		# 表示没有发送文件
        return {
			'message':"文件上传失败"
		}
    file_name = file.filename# print(file.filename)
	# 获取前缀（文件名称）print(os.path.splitext(file_name)[0])
	# 获取后缀（文件类型）print(os.path.splitext(file_name)[-1])
    # suffix = os.path.splitext(file_name)[-1]#获取文件后缀（扩展名）
    basePath = os.path.dirname(__file__)  # 当前文件所在路径print(basePath)
	# # nowTime = calendar.timegm(time.gmtime())#获取当前时间戳改文件名print(nowTime)
    # nowTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    # # nowTime = time.time()
    upload_path = os.path.join(basePath, 'upload')#改到upload目录下# 注意：没有的文件夹一定要先创建，不然会提示没有该路径print(upload_path)
    upload_path = os.path.abspath(upload_path) # 将路径转换为绝对路径print("绝对路径：",upload_path)
    fileNameSave = os.path.join(upload_path, file_name)
    file.save(fileNameSave)#保存文件
	#http 路径
    # url = 'http://xxxx.cn/upload/'+ str(nowTime) + str(nowTime) + suffix

    return {
        'code':200,
        'message':"upload success!",
        'fileNameOld': file_name,
        'fileNameSave': fileNameSave,
        # 'url':url
    }


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
