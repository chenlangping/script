# --coding:utf-8 --

import requests
import hashlib

def calculate_md5(string):
        hash = hashlib.md5()
        hash.update(string.encode('utf-8'))
        sign = hash.hexdigest()
        return sign

def login(username, password):
        url = "https://superapp.kiwa-tech.com/login/enter"
        json = { "country": "CN", "mobile": username,"passWord": calculate_md5(password)}
        response = requests.post(url,json=json)
        # print(response.text)
        if response.text.find('成功'):
            return True
        else:
            return False


if __name__ == '__main__':

    count = 0
    usernames = []
    passwords = []
    wrong_Password =0
    for line in open('auth','r'):
        usernames.append(line.strip().split('#')[0])
        passwords.append(line.strip().split('#')[1])
        count +=1


    print('The number of Account = '+str(count))

    for i in range(count):
        if not login(usernames[i],passwords[i]):
            wrong_Password+=1

    print('The number of Wrong Password = '+str(wrong_Password))