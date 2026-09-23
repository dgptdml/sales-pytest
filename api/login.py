import requests
import config
import random
#定义验证码函数
def get_verify_code():
    #return requests.get(f'{config.BASE_URL}/api/captchaImage')
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    return  requests.get(f'{config.BASE_URL}/api/captchaImage', headers=headers)
# 定义登录函数
def login(username,password,uuid,code='2'):
    url=f'{config.BASE_URL}/api/login'
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

#新增课程
def add_course(name,subject,price,applicablePerson,info,token):
    add_course_data = {
    "name": name,
    "subject": subject,
    "price": price,
    "applicablePerson": applicablePerson,
    "info": info}
    url=f'{config.BASE_URL}/api/clues/course'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.post(url=url, headers=headers, json=add_course_data)

#查询自己创建的课程
def query_course(token, name):
    url=f'{config.BASE_URL}/api/clues/course/list'
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

#上传合同
def upload_contract(token):
    url=f'{config.BASE_URL}/api/common/upload'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.post(url=url, headers=headers,files={'file':open("演示.pdf",'rb')})


#新增合同
def add_contract(token, file, courseId):
    url=f'{config.BASE_URL}/api/contract'

    add_course_date = {
        "name": "测试9_22",
        "phone": "18038932970",
        "contractNo": f"HT1{random.randint(1000000,9999999)}",
        "subject": "6",
        "courseId": courseId,
        "channel": "O",
        "activityId": 77,
        "fileName":file
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": token
    }
    return requests.post(url=url,headers=headers,json=add_course_date)

#查询合同
def query_contract(token,iphone):
        url=f'{config.BASE_URL}/api/contract/list?phone={iphone}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Authorization": token
        }
        return requests.get(url=url,headers=headers)


if __name__ == '__main__':
    uuid = get_verify_code().json().get('uuid')#uuid
    print(get_verify_code().json())
    response_1=login(config.USERNAME,config.PASSWORD,uuid)#有数据要调用
    print(response_1.json())
    token=response_1.json().get('token')#token