import requests



url = f'http://127.0.0.1:5001/sendfile'

headers = {
    'Accept': "application/json, text/plain, */*",
    "content_type": 'application/json',
}

file = open(r'C:\workspace\AI2\model\fab4_20221215\latest.pth', 'rb')#.read()

form_data = {
    "filename": 'test2.txt',
}
response = requests.post(url, json=form_data, files = {"file": file}, headers=headers)
# response = requests.post(url=url, json=form_data, headers=headers)
print('response: ', response.status_code, response.content)
