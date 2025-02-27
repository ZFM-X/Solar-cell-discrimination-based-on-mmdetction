import requests
import time
import threading

def i_am_alive(pipeline_name: str):
    while True:
        try:
            url = 'http://172.16.97.177:5000/alive'

            headers = {
                'Accept': "application/json, text/plain, */*",
                "content_type": 'application/json',
            }

            form_data = {
                "pipeline_name": pipeline_name,
            }

            response = requests.post(url=url, json=form_data, headers=headers)

            print('sended: ', response.content)
        except Exception as e:
            # print(e)
            pass

        time.sleep(5)

t1 = threading.Thread(target=i_am_alive, args=('01B',))
t1.start()
while True:

    print('外循环: '+str(time.time()))
    print(threading.active_count())
    time.sleep(1)
    # try:
    #     i_am_alive(pipeline_name='01B')
    # except Exception as e:
    #     print(e)
    #     print(time.time())
    # time.sleep(1)
