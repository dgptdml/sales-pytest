# 配置模板 — 复制一份改名为 config.py 后填入真实值
import os

# 项目根路径（自动获取，不用改）
BASE_DIR = os.path.dirname(__file__)

# 测试服务器地址
BASE_URL = 'http://kdtx-test.itheima.net'

# 后台登录账号（改为你自己的测试账号）
USERNAME = 'your_username'
PASSWORD = 'your_password'

# 以下为测试用默认数据，可按需修改
NAME = '测试开发提升课01'
SUBJECT = '6'
PRICE = 899
APPLICABLE_PERSON = '2'
INFO = '测试开发提升课01'
