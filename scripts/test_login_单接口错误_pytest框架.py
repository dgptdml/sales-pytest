#定义一个测试类
from api.login import *
from common.utils import *
import config
import pytest
'''
test_data=[
    ("admin","HM_2023_test","2",200,200,'成功'),
    ("admin","HM_2026_test","2",200,500,'错误'),
    ("admin","HM_2023_test","3",200,500,'失效')
]
class TestLoginAPI:
    def setup_method(self):
        self.uuid = get_verify_code().json().get('uuid')  # uuid
    #登录成功
    @pytest.mark.parametrize("username,password,verify_code,status_code,code,msg",test_data)
    def test01_login_success(self,username,password,verify_code,status_code,code,msg):
        response_1 = login(username, password, self.uuid, verify_code)
        print(response_1.json())
        assert_common(response_1, status_code, code, msg)
'''
class TestLoginAPI:
    def setup_method(self):
        self.uuid = get_verify_code().json().get('uuid')  # uuid
    #登录成功
    @pytest.mark.parametrize("username,password,verify_code,status_code,code,msg", read_json_file(f'{config.BASE_DIR}/data/login.json'))
    def test01_login_success(self,username,password,verify_code,status_code,code,msg):
        response_1 = login(username, password, self.uuid, verify_code)
        print(response_1.json())
        assert_common(response_1, status_code, code, msg)
    #密码错误
    def test01_login_password_error(self):
        response_2 = login(config.USERNAME, "Aa1234567", self.uuid, 2)
        print(response_2.json())
        assert_common(response_2, 200, 500, "错误")
    #验证码错
    def test01_login_verify_code_error(self):
        response_3 = login(config.USERNAME, config.PASSWORD, self.uuid, 3)
        print(response_3.json())
        assert_common(response_3, 200, 500, "失效")
