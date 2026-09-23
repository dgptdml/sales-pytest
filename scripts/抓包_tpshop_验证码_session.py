import requests
session=requests.session()
#1.获取验证码
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response=session.get('https://hmshop-test.itheima.net/index.php?m=Home&c=User&a=verify',headers=headers)
print(response.status_code)
with open('../image/验证码.png', 'wb') as f:
    f.write(response.content)#返回二进制文件
#请求url
# print(response.url)
# #请求查看响应头部字符编码
# print(response.headers.get('Content-Type'))
# #请求查看头信息
# print(response.headers)
# #请求查看响应cookie信息
# print(response.cookies)
#2.登录
data_1={
    "username":"18038932970",
    "password":"Aa123456",
    "verify_code":"8888"
}
response1=session.post('https://hmshop-test.itheima.net/index.php?m=Home&c=User&a=do_login&t=0.04134450801957745',headers=headers,json=data_1)#登录
print(response1.json())
#3.查看订单
response2=session.get('https://hmshop-test.itheima.net/Home/Order/order_list.html',headers=headers)
print(response2.text)



