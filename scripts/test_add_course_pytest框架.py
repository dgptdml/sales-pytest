# 单接口新增课程测试 — 正向 + 反向全场景，参数化驱动
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.login import *
from common.utils import *
import config
import pytest


class TestAddCourseAPI:
    # 每条课程用例执行前，先登录拿一次 token
    # （课程接口需要鉴权，不像登录/验证码可以匿名调用）
    @pytest.fixture
    def token(self):
        uuid = get_verify_code().json().get('uuid')
        response = login(config.USERNAME, config.PASSWORD, uuid, "2")
        return response.json().get('token')

    # 27 种场景全部从 JSON 读取，一条记录 = 一条独立测试用例
    _test_data = read_json_file(f'{config.BASE_DIR}/data/add_course.json')
    _case_ids = [row[0] for row in _test_data]

    @pytest.mark.parametrize(
        "case_id,desc,name,subject,price,applicablePerson,info,status_code,code,msg",
        _test_data,
        ids=_case_ids
    )
    def test_add_course_all_scenarios(self, token, case_id, desc,
                                       name, subject, price, applicablePerson, info,
                                       status_code, code, msg):
        response = add_course(name, subject, price, applicablePerson, info, token)
        print(f"\n[{case_id}] {desc}: {response.json()}")

        assert_common(response, status_code, code, msg)
