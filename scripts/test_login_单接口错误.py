import pytest

from api.login import *
from common.utils import *
from config import *
'''
test_data=[
    ("admin","HM_2023_test","2",200,200,'成功'),
    ("admin","HM_2026_test","2",200,500,'错误'),
    ("admin","HM_2023_test","3",200,500,'失效')
]
def test_login():
    for i in test_data:
        uuid = get_verify_code().json().get('uuid')#uuid
        #登录成功
        response_1=login(i[0],i[1],uuid,i[2])
        assert_common(response_1,i[3],i[4],i[5])
'''
test_data=[
 {
    "username": "admin",
    "password": "HM_2023_test",
    "verify_code":"2",
    "status_code": 200,
     "code":200,
     "msg":"成功"
},
{
    "username": "admin",
    "password": "HM_2026_test",
    "verify_code":"2",
    "status_code": 200,
    "code":500,
     "msg":"错误"
},
{
    "username": "admin",
    "password": "HM_2023_test",
    "verify_code":"3",
    "status_code": 200,
    "code":500,
     "msg":"失效"
}
]
def test_login():
    for i in test_data:
        uuid = get_verify_code().json().get('uuid')#uuid
        #登录成功
        response_1=login(i.get("username"),i.get("password"),uuid,i.get("verify_code"))
        assert_common(response_1,i.get("status_code"),i.get("code"),i.get("msg"))
    #密码错误
    # uuid = get_verify_code().json().get('uuid')#每次都要重新引用uuid
    # response_2=login(USERNAME,"Aa1234567",uuid,2)
    #print(response_2.json())
    # assert response_2.json().get('code')==500
    # assert response_2.status_code == 200
    # assert "错误" in response_2.text
    #assert_common(response_2,200,500,"错误")
# for i in test_data:
#     uuid = get_verify_code().json().get('uuid')#uuid
#     #登录成功
#     response_1=login(USERNAME,PASSWORD,uuid,2)
#     assert_common(response_1,200,200,"成功")
#     #密码错误
#     uuid = get_verify_code().json().get('uuid')#每次都要重新引用uuid
#     response_2=login(USERNAME,"Aa1234567",uuid,2)
#     #print(response_2.json())
#     # assert response_2.json().get('code')==500
#     # assert response_2.status_code == 200
#     # assert "错误" in response_2.text
#     assert_common(response_2,200,500,"错误")
#验证码错误
'''
uuid = get_verify_code().json().get('uuid')#每次都要重新引用uuid
response_3=login(USERNAME,PASSWORD,uuid,3)
print(response_3.json())
assert response_3.json().get('code')==500
assert response_3.status_code == 200
assert "失效" in response_3.text
'''