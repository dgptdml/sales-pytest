import requests
import config
import random
import os


# 获取验证码
def get_verify_code():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    return requests.get(f'{config.BASE_URL}/api/captchaImage', headers=headers)


# 登录
def login(username, password, uuid, code='2'):
    url = f'{config.BASE_URL}/api/login'
    login_data = {
        "username": username,
        "password": password,
        "uuid": uuid,
        "code": code
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    return requests.post(url=url, headers=headers, json=login_data)


# 新增课程
def add_course(name, subject, price, applicablePerson, info, token):
    add_course_data = {
        "name": name,
        "subject": subject,
        "price": price,
        "applicablePerson": applicablePerson,
        "info": info
    }
    url = f'{config.BASE_URL}/api/clues/course'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.post(url=url, headers=headers, json=add_course_data)


# 查询课程
def query_course(token, name):
    url = f'{config.BASE_URL}/api/clues/course/list'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    params = {
        "pageNum": 1,
        "pageSize": 1,
        "name": name
    }
    return requests.get(url=url, headers=headers, params=params)


# 上传合同（修：PDF 用绝对路径 + with open 关文件句柄 + timeout）
def upload_contract(token, pdf_filename='演示.pdf'):
    url = f'{config.BASE_URL}/api/common/upload'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    pdf_path = os.path.join(config.BASE_DIR, 'data', pdf_filename)
    with open(pdf_path, 'rb') as f:
        return requests.post(url=url, headers=headers,
                             files={'file': f}, timeout=60)


# 新增合同（修：参数全部暴露，不再硬编码）
def add_contract(token, file, courseId,
                 name="测试9_22", phone="18038932970",
                 contractNo=None, subject="6",
                 channel="", activityId=None):
    if contractNo is None:
        contractNo = f"HT1{random.randint(1000000, 9999999)}"

    add_contract_data = {
        "name": name,
        "phone": phone,
        "contractNo": contractNo,
        "subject": subject,
        "courseId": courseId,
        "channel": channel,
        "fileName": file
    }
    if activityId is not None:
        add_contract_data["activityId"] = activityId

    url = f'{config.BASE_URL}/api/contract'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.post(url=url, headers=headers, json=add_contract_data)


# 查询合同
def query_contract(token, iphone):
    url = f'{config.BASE_URL}/api/contract/list?phone={iphone}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.get(url=url, headers=headers)


if __name__ == '__main__':
    uuid = get_verify_code().json().get('uuid')
    print(get_verify_code().json())
    response_1 = login(config.USERNAME, config.PASSWORD, uuid)
    print(response_1.json())
    token = response_1.json().get('token')
