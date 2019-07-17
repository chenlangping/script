# --coding:utf-8 --

import requests
import hashlib


def calculate_md5(string):
    mhash = hashlib.md5()
    mhash.update(string.encode('utf-8'))
    sign = mhash.hexdigest()
    return sign


def login(username, password):
    url = "https://superapp.kiwa-tech.com/login/enter"
    json = {"country": "CN", "mobile": username, "passWord": calculate_md5(password)}
    response = requests.post(url, json=json)
    if response.text.find('成功'):
        return True
    else:
        return False


if __name__ == '__main__':

    count = 0
    user_names = []
    passwords = []
    wrong_Password = 0
    for line in open('auth', 'r'):
        user_names.append(line.strip().split('#')[0])
        passwords.append(line.strip().split('#')[1])
        count += 1

    print('The number of Account = ' + str(count))

    for i in range(count):
        if not login(user_names[i], passwords[i]):
            wrong_Password += 1

    print('The number of Wrong Password = ' + str(wrong_Password))