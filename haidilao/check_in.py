# -*- coding:utf-8 -*-
import requests
import traceback
import hashlib
import time


def CurrentTime():
    currenttime = time.time()
    return int(currenttime * 1000)


def printer(info, file_name='hdl.log', *args):
    at_now = int(time.time())
    time_arr = time.localtime(at_now)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_arr)
    content = f'[{format_time}] {info} {" ".join(f"{str(arg)}" for arg in args)}'
    print(content)
    with open(file_name + '.log', "a+", encoding="utf-8")as f:
        f.write(content + "\n")


def calculate_md5(string):
    mhash = hashlib.md5()
    mhash.update(string.encode('utf-8'))
    sign = mhash.hexdigest()
    return sign


class HaiDiLao:

    def __init__(self):
        self.user_id = ''
        self.pnpName = ''
        self.token = ''
        self.duiba_cookies = ''

    def login(self, username, password):
        url = "https://superapp.kiwa-tech.com/login/enter"
        json = {"country": "CN", "mobile": username, "passWord": calculate_md5(password)}
        response = requests.post(url, json=json).json()
        try:
            self.user_id = response['data']['id']
            self.pnpName = response['data']['pnpName']
            self.token = response['data']['token']
            print("登录成功")
            return True
        except:
            return False

    def get_duiba_cookie(self):
        url = "https://superapp.kiwa-tech.com/login/outside/duiba/redirect"
        headers = {
            "Cookie": f"HAIDILAO_APP_TOKEN={self.token};",
            "Content-Type": "application/json; charset=UTF-8",
            "user-agent": "Redmi 4A(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 720x1280",
            "_HAIDILAO_APP_TOKEN": self.token,
        }

        json = {"_HAIDILAO_APP_TOKEN": self.token, "customerId": self.user_id, "uid": self.user_id,
                "url": f"https://activity.m.duiba.com.cn/signactivity/index?id=307"}
        response = requests.post(url, headers=headers, json=json)
        print(response.text)
        try:
            url = response.json()['data']
        except:
            self.duiba_cookies = ''
        s = requests.session()
        s.headers['User-Agent'] = "Haidilao/6.1.0 (Redmi 4A 23 Android 6.0.1)"
        s.get(url, headers=headers, allow_redirects=False)
        self.duiba_cookies = requests.utils.dict_from_cookiejar(s.cookies)

    def signin(self, activity_id, duiba_cookies):
        s = requests.session()
        s.headers['Referer'] = "http://www.haidilao.com/"
        s.headers['User-Agent'] = "Haidilao/6.1.0 (Redmi 4A 23 Android 6.0.1)"
        s.cookies = requests.utils.cookiejar_from_dict(duiba_cookies)
        url = f"https://activity.m.duiba.com.cn/signactivity/doSign?id={activity_id}&_={str(CurrentTime())}"
        s.get(url).json()

    def run(self, username, password):
        try:
            if self.login(username, password):
                # 登录成功
                printer(f"账号{username}正在运行中...", username)
                self.get_duiba_cookie()
                if len(self.duiba_cookies) > 0:
                    # 获取cookie成功
                    for activity_id in [90, 181, 211, 307]:
                        self.signin(activity_id, self.duiba_cookies)
                else:
                    # 获取cookie失败
                    print("fail to get duiba_cookie")
            else:
                # 登录失败
                print("fail to login")
        except:
            traceback.print_exc()
            exit()


def main():
    usernames = []
    passwords = []

    # read user info from file
    for line in open('auth', 'r'):
        usernames.append(line.strip().split('#')[0])
        passwords.append(line.strip().split('#')[1])

    # start 
    for i1, i2 in zip(usernames, passwords):
        HaiDiLao().run(i1, i2)
        time.sleep(600)


if __name__ == '__main__':
    main()
