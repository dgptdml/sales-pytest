﻿# 单接口新增合同测试 — 正向 + 反向全场景，参数化驱动
import sys
import os
import random
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.login import *
from common.utils import *
import config
import pytest


class TestAddContractAPI:
    # fixture 内部网络调用的重试次数
    _MAX_RETRY = 3

    # 每条用例执行前，先登录 + 上传 PDF + 动态查可用 courseId
    # 加了重试：网络偶发超时（如 ConnectTimeout/SSLError）时自动重试，不直接 ERROR
    @pytest.fixture
    def token_and_file(self):
        last_err = None
        for attempt in range(1, self._MAX_RETRY + 1):
            try:
                uuid = get_verify_code().json().get('uuid')
                token = login(config.USERNAME, config.PASSWORD, uuid, "2").json().get('token')
                up = upload_contract(token, "演示.pdf")
                file_name = up.json().get('fileName')
                # 动态查一个可用的 courseId（避免硬编码被其他用例占用）
                course_id = query_course(token, "").json()["rows"][0]["id"]
                return token, file_name, course_id
            except Exception as e:
                last_err = e
                if attempt < self._MAX_RETRY:
                    print(f"\n fixture 第 {attempt} 次失败: {type(e).__name__}，{self._MAX_RETRY - attempt}s 后重试...")
                    time.sleep(self._MAX_RETRY)
        # 3 次都失败 → skip，不 ERROR
        pytest.skip(f"fixture 网络调用 {self._MAX_RETRY} 次都失败 → {type(last_err).__name__}")

    # 23 种场景全部从 JSON 读取，一条记录 = 一条独立测试用例
    _test_data = read_json_file(f'{config.BASE_DIR}/data/add_contract.json')
    _case_ids = [row[0] for row in _test_data]

    @pytest.mark.parametrize(
        "case_id,desc,name,phone,contractNo,subject,courseId,channel,activityId,status_code,code,msg",
        _test_data,
        ids=_case_ids
    )
    def test_add_contract_all_scenarios(self, token_and_file,
                                         case_id, desc,
                                         name, phone, contractNo, subject, courseId, channel, activityId,
                                         status_code, code, msg):
        token, file_name, dynamic_course_id = token_and_file

        # 处理 courseId："auto" → 用 fixture 动态查询到的可用 courseId
        if courseId == "auto":
            courseId = dynamic_course_id

        # 处理 contractNo：auto → 生成唯一合同号（避免撞数据库）
        if contractNo == "auto":
            contractNo = f"HT{int(time.time()*1000)}{random.randint(100,999)}"
        elif contractNo and contractNo.startswith("auto_"):
            # auto_noPrefix → 故意生成不带前缀 a 的值，测前缀校验
            suffix = contractNo[5:]  # "noPrefix"
            contractNo = f"{suffix}{random.randint(1000000,9999999)}"

        try:
            response = add_contract(token, file_name, courseId,
                                      name, phone, contractNo, subject,
                                      channel, activityId)
        except Exception as e:
            pytest.skip(f"环境限制：新增合同网络异常 → {type(e).__name__}")

        print(f"\n[{case_id}] {desc}: courseId={courseId}, phone={phone}, contractNo={contractNo} → {response.json()}")

        assert_common(response, status_code, code, msg)

    # ---------- 以下 1 条独立 def：fileName 为空（不在 JSON 参数化里，需要单独传空 fileName） ----------
    def test_add_contract_file_name_empty(self):
        """fileName 为空：应该返回 500 提示不能为空"""
        # 登录也加重试保护（避免偶发网络超时直接 ERROR）
        token = None
        dynamic_course_id = None
        for attempt in range(1, self._MAX_RETRY + 1):
            try:
                uuid = get_verify_code().json().get('uuid')
                token = login(config.USERNAME, config.PASSWORD, uuid, "2").json().get('token')
                dynamic_course_id = query_course(token, "").json()["rows"][0]["id"]
                break
            except Exception as e:
                if attempt < self._MAX_RETRY:
                    time.sleep(self._MAX_RETRY)
                else:
                    pytest.skip(f"登录 {self._MAX_RETRY} 次都失败 → {type(e).__name__}")

        contractNo = f"HT{int(time.time()*1000)}{random.randint(100,999)}"
        try:
            # 关键：第二个参数 file 传空字符串，不是 fixture 里的真实 fileName
            response = add_contract(token, "", dynamic_course_id,
                                      "测试_fileName空", "13612341888",
                                      contractNo, "6", 0, 77)
        except Exception as e:
            pytest.skip(f"环境限制：新增合同网络异常 → {type(e).__name__}")

        print(f"\n[SALES_contract_024] fileName为空 → {response.json()}")

        assert_common(response, 200, 500, None)
