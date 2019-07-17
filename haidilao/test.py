#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import requests
import random
import time


def CurrentTime():
    currenttime = time.time()
    return int(currenttime * 1000)


class test(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def caclulate_pg_for_g1(self):
        return self.gotoT + "-" + self.startLoad + "-" + self.endLoad + "-" + self.vxy(self.endLoad, self.statew,
                                                                                       self.gkey) + "-" + self.vxy(
            self.endLoad, self.stateh, self.gkey) + "|" + self.startT + "-" + self.vxy(self.startT, self.startX,
                                                                                       self.gkey) + "-" + self.vxy(
            self.startT, self.startY, self.gkey) + "|" + str(self.noTIpsT) + "-" + str(
            self.knowT) + "-" + self.vxy(self.knowT, self.knowX, self.gkey) + "-" + self.vxy(self.knowT,
                                                                                             self.knowY,
                                                                                             self.gkey) + "|" + str(
            self.knowQDT) + "-" + self.vxy(self.knowQDT, self.knowQDX, self.gkey) + "-" + self.vxy(self.knowQDT,
                                                                                                   self.knowQDY,
                                                                                                   self.gkey)

    def caclulate_gs_for_g1(self):
        return self.gameST + "-" + self.gameET + "-" + self.vxy(self.gameST, self.gameC,
                                                                self.gkey) + "-" + self.vxy(self.gameST,
                                                                                            self.gameScore,
                                                                                            self.gkey) + "|" + self.prop1T + "-" + self.vxy(
            self.prop1T, self.prop1X, self.gkey) + "-" + self.vxy(self.prop1T, self.prop1Y,
                                                                  self.gkey) + "|" + self.prop2T + "-" + self.vxy(
            self.prop2T, self.prop2X, self.gkey) + "-" + self.vxy(self.prop2T, self.prop2Y,
                                                                  self.gkey) + "|" + self.prop3T + "-" + self.vxy(
            self.prop3T,
            self.prop3X,
            self.gkey) + "-" + self.vxy(
            self.prop3T, self.prop3Y, self.gkey)

    def caclulate_gd_for_g1(self):
        return self.vxy(self.gameST, self.pillarC, self.gkey) + "-" + self.vxy(self.gameST, self.birdC,
                                                                               self.gkey) + "-" + self.vxy(
            self.gameST, self.gBirdC, self.gkey) + "-" + self.vxy(self.gameST, self.propC,
                                                                  self.gkey) + "-" + self.vxy(self.gameST,
                                                                                              self.hPropC,
                                                                                              self.gkey) + "-" + self.vxy(
            self.gameST, self.add1, self.gkey) + "-" + self.vxy(self.gameST, self.add2,
                                                                self.gkey) + "-" + self.vxy(self.gameST,
                                                                                            self.add3,
                                                                                            self.gkey) + "-" + self.vxy(
            self.gameST, self.add4, self.gkey)

    def vxy(self, t, e, gkey):
        tmp1 = self.get_time_num(t)
        tmp2 = self.get_gkey_num(gkey) + int(e)
        return str(tmp1 * tmp2)

    def get_time_num(self, t):
        try:
            return int(str(t)[10]) + 1
        except IndexError:
            return 1

    def get_gkey_num(self, gkey):
        return int(str(self.char_to_num(gkey[len(gkey) - 3])) + str(self.char_to_num(gkey[len(gkey) - 5])))

    def char_to_num(self, t):
        num = 0
        for i in range(0, len(t)):
            num = num + ord(t[i])
        return num

    def login(self, username, password):
        url = "https://superapp.kiwa-tech.com/login/enter"
        json = {"country": "CN", "mobile": username, "passWord": self.calculate_md5(password)}
        response = requests.post(url, json=json).json()
        try:
            self.user_id = response['data']['id']
            self.pnpName = response['data']['pnpName']
            self.token = response['data']['token']
            self.headImg = response['data']['headImg']
            # print(self.user_id, self.pnpName, self.token, self.headImg)
            return True
        except:
            # exit("用户名或密码不对")
            return False

    def calculate_md5(self, string):
        hash = hashlib.md5()
        hash.update(string.encode('utf-8'))
        sign = hash.hexdigest()
        return sign

    def get_game_token(self):
        url = "https://api-hdl.51h5.com/hdl/game/init"
        data = {
            "uid": self.user_id,
            "mobile": self.username,
            "gid": "hdlgame_01"
        }
        response = requests.post(url, data=data)
        print(response.text)
        try:
            self.gametoken = response.json()['data']['token']
        except:
            print("error")

    def caclulate_pg_for_g2(self):
        self.recobj["pg"] = self.recobj["pg_" + self.reclist[0]]
        t = 0
        for e in range(1, len(self.reclist)):
            i = "-"
            if e == 5 or e == 8 or e == 12:
                i = "|"
            if int(self.recobj["pg_" + self.reclist[e]]) > 9999999:
                t = self.recobj["pg_" + self.reclist[e]]
                if self.recobj["pg_" + self.reclist[e]]:
                    self.recobj['pg'] = self.recobj['pg'] + i + self.recobj["pg_" + self.reclist[e]]
                else:
                    self.recobj['pg'] = self.recobj['pg'] + i + "0"
            else:
                if self.recobj["pg_" + self.reclist[e]]:
                    self.recobj['pg'] = self.recobj['pg'] + i + self.vxy(t, self.recobj["pg_" + self.reclist[e]],
                                                                         self.gkey)
                else:
                    self.recobj['pg'] = self.recobj['pg'] + i + "0"
        return self.recobj['pg']

    def caclulate_gs_for_g2(self):
        self.recobj['gs'] = self.recobj["gs_st"] + "-" + self.recobj["gs_et"] + "-" + self.vxy(self.recobj["gs_st"],
                                                                                               self.tapleft + self.tapright,
                                                                                               self.gkey) + "-" + self.vxy(
            self.recobj["gs_st"], self.score, self.gkey)
        for e in range(0, 3):
            if self.recobj['pg_uc' + str(e)] != "":
                self.recobj['gs'] = self.recobj['gs'] + "|" + self.recobj["pg_uc" + str(e)] + "-" + self.vxy(
                    self.recobj['pg_uc' + str(e)], self.recobj['pg_ux' + str(e)], self.gkey) + "-" + self.vxy(
                    self.recobj["pg_uc" + str(e)], self.recobj['pg_uy' + str(e)], self.gkey)
            else:
                self.recobj['gs'] = self.recobj['gs'] + "|0-0-0"
        return self.recobj['gs']

    def caclulate_gd_for_g2(self):
        self.recobj['gd'] = self.vxy(self.recobj["gs_st"], self.tapleft, self.gkey) + "-" + self.vxy(
            self.recobj["gs_st"],
            self.tapright,
            self.gkey) + "-" + str(self.scoreRecord)
        return self.recobj['gd']

    def g2_score_helper(self):
        self.scoreCount = self.scoreCount + 1
        self.comboNum = self.comboNum + 1
        caveWidth = 1
        if int(self.comboNum) > 6:
            caveWidth = 1 + self.ADDSCOREBEI * (int(self.comboNum) - 6)
        if caveWidth > self.MAXSCOREBEI:
            caveWidth = self.MAXSCOREBEI
        self.score = self.score + int(self.SINGLESCORE) * caveWidth

    def play_game1(self):
        self.gotoT = str(CurrentTime())
        self.startLoad = str(CurrentTime() + random.randint(1000, 1500))
        self.endLoad = str(CurrentTime() + random.randint(4000, 8000))
        self.statew = "750"
        self.stateh = "1624"
        self.startT = "0"
        self.startX = "0"
        self.startY = "0"
        self.noTIpsT = "0"
        self.knowT = "0"
        self.knowX = "0"
        self.knowY = "0"
        self.knowQDT = str(CurrentTime() + random.randint(2000, 4000))
        self.knowQDX = "457"
        self.knowQDY = "1300"
        self.prop1T = "0"
        self.prop1X = "0"
        self.prop1Y = "0"
        self.prop2T = "0"
        self.prop2X = "0"
        self.prop2Y = "0"
        self.prop3T = "0"
        self.prop3X = "0"
        self.prop3Y = "0"
        self.gameST = str(int(self.knowQDT) + random.randint(300, 600))
        self.gameET = str(int(self.gameST) + random.randint(47500, 72500))
        self.propC = "0"
        self.hPropC = "0"
        self.add1 = str(random.randint(80, 100))
        self.add2 = str(random.randint(50, 60))
        self.add3 = str(random.randint(30, 40))
        self.add4 = str(random.randint(15, 20))
        self.gameC = str(int(self.add1) + int(self.add2) + int(self.add3) + int(self.add4) + int(random.randint(1, 20)))
        self.pillarC = str(int(self.gameC) + random.randint(30, 50))
        self.birdC = str(int(self.gameC) + random.randint(15, 50))
        self.gBirdC = str(self.gameC)
        self.gameScore = str(int(self.add1) + 4 * int(self.add2) + 8 * int(self.add3) + 15 * int(self.add4))
        url = "https://api-hdl.51h5.com/hdl/game/begin"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "X-Requested-With": "com.haidilao",
            "Referer": "https://event.ews.m.jaeapp.com/hdlgame_01/",
            "User-Agent": "Haidilao/6.1.0 (Xiaomi 2s 23 Android 7.0.1)",
            "Origin": "https://event.ews.m.jaeapp.com",
            "Accept-Encoding": "gzip, deflate, br"
        }
        data = {
            "token": self.gametoken,
            "gid": "hdlgame_01",
            "iid": ""
        }
        response = requests.post(url, headers=headers, data=data)
        print('response = ', response.text)
        self.gkey = response.json()['data']['gkey']

        url = "https://api-hdl.51h5.com/hdl/game/end"
        data = {
            "token": self.gametoken,
            "gkey": self.gkey,
            "score": self.gameScore,
            "pg": self.caclulate_pg_for_g1(),
            "gs": self.caclulate_gs_for_g1(),
            "gd": self.caclulate_gd_for_g1()
        }
        time.sleep(80)
        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        print(response.json()['data']['credit'])

    def play_game2(self, game_id):
        self.reclist = ["ps", "ls", "le", "w", "h", "sc", "sx", "sy", "nc", "ic", "ix", "iy", "qc", "qx", "qy"]
        self.pg_ps = str(CurrentTime())
        self.pg_ls = str(int(self.pg_ps) + random.randint(400, 600))
        self.pg_le = str(int(self.pg_ls) + random.randint(400, 800))
        self.pg_sc = str(int(self.pg_le) + random.randint(2000, 3000))
        self.pg_ic = str(int(self.pg_sc) + random.randint(2000, 3000))
        self.pg_ix = "419"
        self.pg_iy = "1232"
        self.pg_qx = "407"
        self.pg_qy = "1024"
        self.pg_sx = "417"
        self.pg_sy = "1232"
        self.pg_w = "750"
        self.pg_h = "1624"
        self.pg_qc = str(int(self.pg_ic) + random.randint(1000, 2000))
        self.pg_nc = str(int(self.pg_sc) + random.randint(1000, 2000))
        self.pg_uc0 = ""
        self.pg_uc1 = ""
        self.pg_uc2 = ""
        self.pg_bc = "0"
        self.pg_bx = "0"
        self.pg_by = "0"
        self.pg_ux0 = "0"
        self.pg_ux1 = "0"
        self.pg_ux2 = "0"
        self.pg_uy0 = "0"
        self.pg_uy1 = "0"
        self.pg_uy2 = "0"
        self.gs_st = str(int(self.pg_qc) + random.randint(400, 800))
        self.gs_et = str(int(self.gs_st) + random.randint(480000, 600000))
        self.recobj = {"gs_st": self.gs_st, "gs_et": self.gs_et, "pg_h": self.pg_h, "pg_le": self.pg_le,
                       "pg_ls": self.pg_ls,
                       "pg_ps": self.pg_ps, "pg_qc": self.pg_qc, "pg_qx": self.pg_qx, "pg_qy": self.pg_qy,
                       "pg_sc": self.pg_sc, "pg_sx": self.pg_sx, "pg_sy": self.pg_sy, "pg_w": self.pg_w,
                       "pg_nc": self.pg_nc, "pg_ic": self.pg_ic, "pg_ix": self.pg_ix, "pg_iy": self.pg_iy, "pg": "",
                       "gs": "", "gd": "", "pg_uc0": self.pg_uc0, "pg_uc1": self.pg_uc1, "pg_uc2": self.pg_uc2,
                       "pg_ux0": self.pg_ux0, "pg_ux1": self.pg_ux1, "pg_ux2": self.pg_ux2, "pg_uy0": self.pg_uy0,
                       "pg_uy1": self.pg_uy1, "pg_uy2": self.pg_uy2}
        self.tapleft = random.randint(120, 150)
        self.tapright = random.randint(120, 150)
        self.score = 0
        self.scoreRecord = ""
        self.scoreCount = 0
        self.comboNum = 0
        self.ADDSCOREBEI = 0.1
        self.MAXSCOREBEI = 5
        self.SINGLESCORE = 10
        self.caclulate_score_for_g2()
        url = "https://api-hdl.51h5.com/hdl/game/begin"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "X-Requested-With": "com.haidilao",
            "Referer": "https://event.ews.m.jaeapp.com/hdlgame_01/",
            "User-Agent": "Haidilao/6.1.0 (Xiaomi 2s 23 Android 7.0.1)",
            "Origin": "https://event.ews.m.jaeapp.com",
            "Accept-Encoding": "gzip, deflate, br"
        }
        data = {
            "token": self.gametoken,
            "gid": "hdlgame_02",
            "iid": ""
        }
        response = requests.post(url, headers=headers, data=data)
        self.gkey = response.json()['data']['gkey']

        time.sleep((int(self.gs_et) - int(self.gs_st)) / 1000)

        self.scoreRecord = self.scoreRecord + self.vxy(self.recobj['gs_st'], self.scoreCount, self.gkey) + "-"
        self.scoreRecord = self.scoreRecord + self.vxy(self.recobj['gs_st'], 0, self.gkey) + "-"
        self.scoreRecord = self.scoreRecord + self.vxy(self.recobj['gs_st'], 0, self.gkey) + "-"
        self.scoreRecord = self.scoreRecord + self.vxy(self.recobj['gs_st'], 0, self.gkey) + "-"
        self.scoreRecord = self.scoreRecord + self.vxy(self.recobj['gs_st'], 0, self.gkey)
        # url = "https://dev-api-hdl.51h5.com/hdl/game/end"
        url = "https://api-hdl.51h5.com/hdl/game/end"
        data = {
            "token": self.gametoken,
            "gkey": self.gkey,
            "score": int(self.score),
            "pg": self.caclulate_pg_for_g2(),
            "gs": self.caclulate_gs_for_g2(),
            "gd": self.caclulate_gd_for_g2()
        }
        response = requests.post(url, headers=headers, data=data)
        print(response.json())

    def caclulate_score_for_g2(self):
        for i in range(0, int(self.tapleft)):
            self.g2_score_helper()
        for k in range(0, int(self.tapright)):
            self.g2_score_helper()

    def run(self):
        self.login(self.username, self.password)
        self.get_game_token()
        self.play_game2()


if __name__ == '__main__':
    test('15005756522', 'yangqing66').run()
