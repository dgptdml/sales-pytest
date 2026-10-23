'''
定义公共断言
'''
import json
def assert_common(response,status_code,code,msg=None):
    assert response.status_code == status_code
    assert response.json().get('code') == code
    if msg is not None:
        assert msg in response.text

def read_json_file(fileName):#文件类型进行转换
    test_data2 = []#建立新列表
    with open(fileName, 'r', encoding='utf-8') as f:
        test_data = json.load(f)#读取文件
        for i in test_data:  #把[{}]转成[()]
            test_data2.append(tuple(i.values()))
    return test_data2
    #将列表转为字典



if __name__ == '__main__':
    test_data = read_json_file('../data/login.json')
    print(test_data)
