#!/usr/bin/env python
# -*- coding:utf8 -*-
# docker push nmsldd/awd-web-yccms:tagname

import requests
import time

sleep_time = 600  # check等待时间
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
checkapi = "http://ip:8888/api/manager/checkDown"
checkapi_token = '4443d148-a2d5-4e39-a483-e0e050c883e7'

team_data = [
    {"teamid": 1, "teamserver": "ip:port"},
]


def down(teamid):
    res = requests.post(checkapi, json={'GameBoxID': teamid}, headers={'Authorization': checkapi_token}).json()
    if res["error"] != 0:
        print res['msg']


def check(teamserver):
    try:
        res = requests.get(
            'http://' + teamserver + '/', headers=headers)
        if '<h1>CTFCMS</h1>' in res.content:
            print '[+normal] ' + str(teamserver) + ' index check normal'
            res = requests.get('http://' + teamserver + '/search/?s=aa', headers=headers)
            if 'error">抱歉' in res.content:
                print '[+normal] ' + str(teamserver) + ' search check normal'
                data = 'user=admin&pass=admin'
                res = requests.post('http://' + teamserver + '/admin/?a=login&m=ajaxLogin', headers=headers, data=data)
                if '1' in res.content:
                    print '[+normal] ' + str(teamserver) + ' login check normal'
                    res = requests.get('http://' + teamserver + '/admin/?a=call&m=xhUp&type=xh', headers=headers)
                    if 'alert' in res.content:
                        print '[+normal] ' + str(teamserver) + ' upload_Interface check normal'
                        return False
                    else:
                        print "[×fail] " + str(teamserver) + " upload_Interface check fail"
                        return True
                else:
                    print "[×fail] " + str(teamserver) + " login check fail"
                    return True
            else:
                print "[×fail] " + str(teamserver) + " search check fail"
                return True
        else:
            print "[×fail] " + str(teamserver) + " index check fail"
            return True
    except Exception as e:
        print str(teamserver) + ' is not OK!!!'
        return True


def main():
    for i in team_data:
        try:
            if check(i['teamserver']):
                down(i['teamid'])
        except Exception as e:
            print e


if __name__ == '__main__':
    while True:
        main()
        time.sleep(sleep_time)
