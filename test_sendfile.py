import requests



url = f'http://172.16.97.177:5001/sendfile'

headers = {
    'Accept': "application/json, text/plain, */*",
    "content_type": 'application/json',
}

file = open(r'D:\AI2\model\20221122_test\latest.pth', 'rb')#.read()

form_data = {
    "filename": 'test2.txt',
}
response = requests.post(url, json=form_data, files = {"file": file}, headers=headers)
# response = requests.post(url=url, json=form_data, headers=headers)
print('response: ', response.status_code, response.content)
