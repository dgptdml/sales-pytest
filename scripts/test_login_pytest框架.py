# 单接口登录测试 — 正向 + 反向全场景，参数化驱动
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

from api.login import *
from common.utils import *
import config
import pytest


class TestLoginAPI:
    # 每跑一条用例前，先请求一次真实的验证码 uuid
    @pytest.fixture
    def real_uuid(self):
        return get_verify_code().json().get('uuid')

    # 9 种场景全部从 JSON 读取，一条记录 = 一条独立测试用例
    # ids 用 case_id 列表，让 pytest 输出显示 SALES_login_001 这样的名字
    _test_data = read_json_file(f'{config.BASE_DIR}/data/login.json')
    _case_ids = [row[0] for row in _test_data]

    @pytest.mark.parametrize(
        "case_id,desc,username,password,verify_code,uuid,status_code,code,msg",
        _test_data,
        ids=_case_ids
    )
    def test_login_all_scenarios(self, real_uuid, case_id, desc,
                                  username, password, verify_code, uuid,
                                  status_code, code, msg):
        # 核心逻辑：uuid=="auto" 用真实值（A 类场景），否则用 JSON 里写的假值（B 类场景）
        actual_uuid = real_uuid if uuid == "auto" else uuid

        response = login(username, password, actual_uuid, verify_code)
        print(f"\n[{case_id}] {desc}: {response.json()}")

        assert_common(response, status_code, code, msg)

    # ---------- 以下 2 个用例验证 uuid/验证码的时间窗口行为 ----------
    # 实测：sleep 60s / 120s 后仍能登录成功 → 该系统验证码过期阈值 > 120s
    # 若要测「真正过期」场景，需根据后端配置调整 _EXPIRE_WINDOW_SECONDS 到足够大
    _EXPIRE_WINDOW_SECONDS = 60   # 按实测值调整

    @pytest.mark.slow
    def test_login_uuid_not_expired_within_window(self):
        """验证 uuid 在一定时间窗口内不会过期（实测 > 120s）
        先获取真实 uuid，等 _EXPIRE_WINDOW_SECONDS 后提交登录 → 应成功"""
        uuid = get_verify_code().json().get('uuid')
        print(f"\n获取到 uuid={uuid}，等待 {self._EXPIRE_WINDOW_SECONDS} 秒...")
        time.sleep(self._EXPIRE_WINDOW_SECONDS)

        response = login(config.USERNAME, config.PASSWORD, uuid, "2")
        body = response.json()
        print(f"sleep {self._EXPIRE_WINDOW_SECONDS}s 后登录结果: {body}")
        # 窗口内应仍有效 → 登录成功
        assert_common(response, 200, 200, "成功")

    @pytest.mark.slow
    def test_login_verify_code_not_expired_within_window(self):
        """验证验证码在一定时间窗口内不会过期（实测 > 120s）
        逻辑同上：uuid + 验证码都经过 sleep 后仍应有效"""
        uuid = get_verify_code().json().get('uuid')
        print(f"\n获取到 uuid={uuid}，等待 {self._EXPIRE_WINDOW_SECONDS} 秒...")
        time.sleep(self._EXPIRE_WINDOW_SECONDS)

        response = login(config.USERNAME, config.PASSWORD, uuid, "2")
        body = response.json()
        print(f"sleep {self._EXPIRE_WINDOW_SECONDS}s 后登录结果: {body}")
        assert_common(response, 200, 200, "成功")
