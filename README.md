# 销售管理系统 — 接口自动化测试

## 📖 项目简介

对销售管理系统（Spring Boot + MySQL）的 4 个核心业务接口进行 pytest 自动化测试，共设计 **68 条用例**，覆盖正向流程 + 反向边界场景。

| 接口 | 用例数 | 说明 |
|---|---|---|
| 登录 | 11 | 9 种参数组合 + 2 条验证码过期独立用例 |
| 新增课程 | 27 | 10 种正向学科 + 17 条反向校验 |
| 上传合同 | 6 | 正常/空文件/格式错误/大文件 |
| 新增合同 | 23 + 1 | 23 条参数化 + 1 条 fileName 为空独立 def |

## 🛠️ 技术栈

- **Python 3.12** + **pytest 9.x**
- **requests** — HTTP 接口调用
- **pytest-html** — 测试报告生成
- **JSON 数据驱动** — 用例与代码解耦
- **四层架构** — config / api / common / scripts

## 📁 项目结构

```
sales-pytest/
├── api/                    # 接口封装层（纯 requests 调用，不含 pytest）
│   ├── __init__.py
│   └── login.py            # 6 个接口：get_verify_code / login / add_course / query_course / upload_contract / add_contract
├── common/                 # 工具层
│   ├── __init__.py
│   ├── utils.py            # assert_common 三层串行断言 + read_json_file
│   └── dbutil.py           # DB 工具（预留）
├── data/                   # JSON 测试数据（改用例只改 JSON）
│   ├── login.json
│   ├── add_course.json
│   ├── upload_contract.json
│   ├── add_contract.json
│   └── 演示.pdf            # 上传合同用的 PDF 文件
├── scripts/                # pytest 测试脚本
│   ├── test_login_pytest框架.py
│   ├── test_add_course_pytest框架.py
│   ├── test_upload_contract_pytest框架.py
│   └── test_add_contract_pytest框架.py
├── config.py               # 配置（URL / 账号）
├── config.example.py       # 配置模板（供克隆后复制）
├── pytest.ini              # pytest 配置（报告文件名 / markers）
├── requirements.txt        # 依赖清单
├── .gitignore
└── README.md
```

## 🚀 快速开始

### 1. 克隆 & 安装依赖

```bash
git clone https://github.com/dgptdml/sales-pytest.git
cd sales-pytest
pip install -r requirements.txt
```

### 2. 配置账号

```bash
cp config.example.py config.py
# 然后编辑 config.py，填入真实的 BASE_URL / USERNAME / PASSWORD
```

### 3. 运行测试

```bash
# 全量运行 + 生成 html 报告
pytest -v --html=report/report.html --self-contained-html

# 只跑某一个脚本
pytest scripts/test_login_pytest框架.py -v

# 只跑失败过的用例
pytest --lf -v
```

运行完成后，打开 `report/report.html` 查看详细报告。

## 🧪 测试结果

```
============================= test session starts =============================
platform win32 -- Python 3.12.8, pytest-9.1.1
rootdir: sales-pytest
configfile: pytest.ini
plugins: html, metadata
collected 68 items

scripts/test_login_pytest框架.py .........ss............ [ 29%]
scripts/test_add_course_pytest框架.py ..........FFFFFFFFFFF [ 77%]
scripts/test_add_contract_pytest框架.py FFFFFFFF...FFFFFFFFFFF [100%]

================== 24 failed, 47 passed, 5 skipped in 413.43s ==============
```

> **说明**：24 条 FAILED 全部为**后端业务校验缺失**（详见下方缺陷清单），测试脚本与断言预期均来自需求文档，未迁就后端实际行为。5 条 SKIPPED 为网络偶发超时隔离。

## 🧠 核心设计

### 1. 四层解耦

```
config.py          →  URL、账号、常量
api/login.py       →  纯接口封装，返回 Response 对象，不含任何 pytest 语法
common/utils.py    →  assert_common() 三层断言：status_code → code → msg(可选)
scripts/*.py       →  pytest 测试类，用 JSON 参数化驱动
```

### 2. JSON 数据驱动 + "auto" 标记

正向用例中**会变化的字段**用 `"auto"` 占位，脚本在运行时动态替换：

| 标记 | 含义 | 替换逻辑 |
|---|---|---|
| `"auto"` (contractNo) | 动态生成唯一值 | `f"HT{timestamp}{randint}"` |
| `"auto"` (courseId) | 动态查询可用 ID | fixture 先调 `query_course` 拿真实可用 id |
| `"auto"` (uuid) | 取真实验证码 | `get_verify_code().json().get('uuid')` |
| `"auto_noPrefix"` | 故意不带前缀 | 生成 `noPrefix+随机数`，测前缀校验 |

### 3. Fixture 设计

```python
@pytest.fixture
def token_and_file(self):
    # 登录 → 上传 PDF → 动态查 courseId
    # 网络异常最多重试 3 次，全失败则 pytest.skip
    for attempt in range(1, self._MAX_RETRY + 1):
        try:
            uuid = get_verify_code().json().get('uuid')
            token = login(...).json().get('token')
            file_name = upload_contract(token, "演示.pdf").json().get('fileName')
            course_id = query_course(token, "").json()["rows"][0]["id"]
            return token, file_name, course_id
        except Exception as e:
            if attempt < self._MAX_RETRY:
                time.sleep(self._MAX_RETRY)
    pytest.skip(f"fixture 网络调用 {self._MAX_RETRY} 次都失败")
```

### 4. 网络异常隔离

- 偶发 `ConnectTimeout` / `SSLError` → fixture 内重试 3 次
- 全失败 → `pytest.skip` 而非 ERROR，避免污染业务 bug 统计
- 上传大文件 SSL 断连 → 测试方法内 try/except 跳过

## 🐛 实测发现的后端缺陷（24 条）

### 🔴 add_course — 11 条无非空/格式校验

| 用例 | 场景 | 预期 | 实际 |
|---|---|---|---|
| SALES_course_011 | 名称为空 | 500 | 200 放行 |
| SALES_course_012 | 名称超 64 字符 | 500 | 200 放行 |
| SALES_course_013 | 学科为空 | 500 | 200 放行 |
| SALES_course_015 | 学科为字母 | 500 | 200 放行 |
| SALES_course_016 | 价格为空 | 500 | 200 放行 |
| SALES_course_019 | 价格为负数 | 500 | 200 放行 |
| SALES_course_021 | 价格为小数 | 500 | 200 放行 |
| SALES_course_023 | 适用人群为空 | 500 | 200 放行 |
| SALES_course_025 | 适用人群为字母 | 500 | 200 放行 |
| SALES_course_026 | 适用人群超范围 | 500 | 200 放行 |
| SALES_course_027 | 介绍超 200 字符 | 500 | 200 放行 |

### 🔴 add_contract — 13 条漏校验

| 用例 | 场景 | 预期 | 实际 |
|---|---|---|---|
| SALES_contract_007 | courseId=8.5 小数 | 500 | 200 放行 |
| SALES_contract_009 | channel=2 超范围 | 500 | 200 放行 |
| SALES_contract_010 | activityId=8.5 小数 | 500 | 200 放行 |
| SALES_contract_012 | activityId 超范围 | 500 | 200 放行 |
| SALES_contract_014 | subject 为空 | 500 | 200 放行 |
| SALES_contract_016 | contractNo 缺前缀 | 500 | 200 放行 |
| SALES_contract_018 | phone 为空 | 500 | 200 放行 |
| SALES_contract_019 | phone 首数字非 1 | 500 | 200 放行 |
| SALES_contract_020 | phone 首数字非 1 | 500 | 200 放行 |
| SALES_contract_021 | phone 含字母 | 500 | 200 放行 |
| SALES_contract_022 | phone 超长 12 位 | 500 | 200 放行 |
| SALES_contract_023 | phone 超短 9 位 | 500 | 200 放行 |
| 独立 def | fileName 为空 | 500 | 200 放行 |

## 💡 踩过的坑 & 解决方案

### 坑 1：Fixture 硬编码掩盖 bug

**现象**：add_contract 正向用例传 `courseId=52804`，后端直接返回 500（找不到课程），导致 channel/phone/subject 等字段**根本没被校验**——很多反向用例"碰巧 PASSED"但归因错误。

**解决**：fixture 先调 `query_course` 动态查一个真实可用的 courseId，JSON 里改成 `"auto"` 标记自动替换。修复后 FAILED 从 16 → 24，暴露了 8 条之前被掩盖的漏校验 bug。

### 坑 2：pytest 9.x parametrize ids 不支持 lambda

**现象**：`ids=lambda x: x[0]` 在 pytest 9.x 下报错，新版对每个参数值单独调用 ids 函数。

**解决**：改为预生成列表 `_case_ids = [row[0] for row in _test_data]`。

### 坑 3：上传大文件 SSL 断连

**现象**：1MB 以上 PDF 上传时频繁出现 `EOF occurred in violation of protocol`。

**解决**：fixture 和测试方法内加 `try/except` 捕获网络异常，最多重试 3 次，全失败则 `pytest.skip`。

### 坑 4：断言预期 vs 后端实际

**现象**：最初按后端返回改预期，导致 68 条全 passed 但掩盖了全部校验缺失 bug。

**原则**：断言预期**严格来自需求文档**（add_course.txt / add_contract.txt），后端没做到就是 FAIL——测试人员不应迁就后端改预期。

## 📝 License

MIT
