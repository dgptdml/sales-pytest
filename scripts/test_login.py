'''
import requests
response = requests.get('http://kdtx-test.itheima.net/api/captchaImage')
print(response.json())
print(response.json().get('uuid'))
'''
#业务接口 - 带验证码登录
#导包
import requests
import config
import base64

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 第1步：获取验证码
response = requests.get(f'{config.BASE_URL}/api/captchaImage', headers=headers)
uuid = response.json()['uuid']
#img_base64 = captcha_data['img']

# 把验证码图片保存到本地
# with open('captcha.jpg', 'wb') as f:
#     f.write(base64.b64decode(img_base64))
# print("验证码图片已保存为 captcha.jpg，请打开查看后输入")

# 第2步：手动输入验证码
#code = input("请输入验证码：")

# 第3步：带验证码登录
login_data = {
    "username": config.USERNAME,
    "password": config.PASSWORD,
    "uuid": uuid,
    "code": '2'
}
response_1 = requests.post(f'{config.BASE_URL}/api/login', headers=headers, json=login_data)
print(response_1.json())
token=response_1.json().get('token')
assert response_1.status_code == 200
assert response_1.json().get('code') == 200
assert '成功' in response_1.text
