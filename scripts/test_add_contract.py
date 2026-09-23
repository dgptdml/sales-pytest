#业务接口
#新增合同
import requests
import config
from api.login import *
#登录成功
#1.获取验证码
uuid = get_verify_code().json().get('uuid')#uuid
#2.登录
response_1=login(config.USERNAME,config.PASSWORD,uuid)#有数据要调用
token=response_1.json().get('token')#token
print(get_verify_code().json())
print(response_1.json())
assert response_1.status_code == 200
assert  response_1.json().get('code') == 200
assert "成功" in response_1.text
#新增课程
#1.新增课程
response_2=add_course(config.NAME,config.SUBJECT,config.PRICE,config.APPLICABLE_PERSON,config.INFO,token)
print(response_2.json())
assert response_2.status_code == 200
assert  response_2.json().get('code') == 200
assert "成功" in response_2.text
#2.查询课程
response_3=query_course(token, config.NAME)
print(response_3.json())
courseId = response_3.json().get("rows")[0].get("id")
print(f"课程ID: {courseId}")
assert response_3.status_code == 200
assert  response_3.json().get('code') == 200
assert "成功" in response_3.text
#新增合同
#1.上传合同
response_4=upload_contract(token)
print(response_4.json())
file=response_4.json().get('fileName')#得到文件名
assert response_4.status_code == 200
assert  response_4.json().get('code') == 200
assert "成功" in response_4.text
#2.新增合同
response_5=add_contract(token, file, courseId)
print(response_5.json())
assert response_5.status_code == 200
assert response_5.json().get("code")==200
assert "成功" in response_5.text
#3.查询合同
iphone=int(input("输入电话号码"))
response_6=query_contract(token,iphone)
print(response_6.json())
assert response_6.status_code == 200
assert response_6.json().get("code")==200
assert "成功" in response_6.text