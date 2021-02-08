#!/usr/bin/env python
# -*- coding:utf8 -*-
# docker pull nmsldd/awd-web_yunnan_simple

import requests
import time

sleep_time = 600  # check等待时间
my_time = 'AAAA'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
checkapi = "http://ip:19999/api/manager/checkDown"
checkapi_token = '3f652617-2564-44d8-8d0d-118a8aab6a7e'

team_data = [
    {"teamid": 1, "teamserver": "ip:port"},
    {"teamid": 2, "teamserver": "ip:port"},
    {"teamid": 3, "teamserver": "ip:port"},
    {"teamid": 4, "teamserver": "ip:port"},
    {"teamid": 5, "teamserver": "ip:port"},
]


def down(teamid):
    res = requests.post(checkapi, json={'GameBoxID': teamid}, headers={'Authorization': checkapi_token}).json()
    if res["error"] != 0:
        print res['msg']


def check(teamserver):
    try:
        res = requests.get(
            'http://' + teamserver + '/index.php?file=news&cid=1&page=1&test=eval&time=%s' % str(my_time),
            headers=headers)
        if 'about.php?file=header.php' in res.content:
            print '[+normal] ' + str(teamserver) + ' index check normal'
            res = requests.get('http://' + teamserver + '/contact.php', headers=headers)
            if 'mail@example.com' in res.content:
                print '[+normal] ' + str(teamserver) + ' contact check normal'
                data = 'username=admin&password=admin&button=SIGN-IN'
                res = requests.post('http://' + teamserver + '/login.php', headers=headers, data=data)
                if 'Forgot your password' in res.content:
                    print '[+normal] ' + str(teamserver) + ' login check normal'
                    res = requests.get('http://' + teamserver + '/footer.php', headers=headers)
                    if 'SHELL' in res.content:
                        print '[+normal] ' + str(teamserver) + ' footer check normal'
                        res = requests.get('http://' + teamserver + '/search.php', headers=headers)
                        if '搜索结果' in res.content:
                            print '[+normal] ' + str(teamserver) + ' search check normal'
                            return False
                        else:
                            print "[×fail] search check fail"
                            return True
                    else:
                        print "[×fail] footer check fail"
                        return True
                else:
                    print "[×fail] login check fail"
                    return True
            else:
                print "[×fail] contact check fail"
                return True
        else:
            print "[×fail] index check fail"
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
