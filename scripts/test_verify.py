'''
import requests
response = requests.get('http://kdtx-test.itheima.net/api/captchaImage')
print(response.json())
'''
#业务接口
#导包
import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
#发送接口请求
response = requests.get('http://kdtx-test.itheima.net/api/captchaImage', headers=headers)
#打印响应结果
#print(response.json())
uuid=response.json().get('uuid')

