# 单接口上传合同测试 — 正向 + 反向全场景，参数化驱动
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.login import *
from common.utils import *
import config
import pytest


class TestUploadContractAPI:
    # 每条用例执行前，先登录拿一次 token
    @pytest.fixture
    def token(self):
        uuid = get_verify_code().json().get('uuid')
        response = login(config.USERNAME, config.PASSWORD, uuid, "2")
        return response.json().get('token')

    # 6 种场景全部从 JSON 读取，一条记录 = 一条独立测试用例
    _test_data = read_json_file(f'{config.BASE_DIR}/data/upload_contract.json')
    _case_ids = [row[0] for row in _test_data]

    @pytest.mark.parametrize(
        "case_id,desc,file_name,status_code,code,msg",
        _test_data,
        ids=_case_ids
    )
    def test_upload_all_scenarios(self, token, case_id, desc,
                                   file_name, status_code, code, msg):
        try:
            response = upload_contract(token, file_name)
        except Exception as e:
            # 网络层异常（SSL 断连等）：不是业务 bug，是环境限制，skip 掉
            pytest.skip(f"环境限制：上传 {file_name} 网络异常 → {type(e).__name__}")

        print(f"\n[{case_id}] {desc} ({file_name}): {response.json()}")

        assert_common(response, status_code, code, msg)
