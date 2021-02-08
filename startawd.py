# -*- coding: utf-8 -*-
# python2

import time
import argparse
import sys
import os
import hashlib


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="靶机 REPOSITORY，执行docker images查看")
    parser.add_argument("-p", "--port", default=80, type=int, help="靶机端口，部分靶机可能不是80端口，需要指定映射关系")
    parser.add_argument("-t", "--team_number", type=int, help="参赛战队数目")
    parser.add_argument("-r", help="重置参赛队伍靶机")
    parser.add_argument("-c", help="清理环境")
    return parser.parse_args()


def generate_pass(teamid):
    salt = 'leishianquan'
    passwd = hashlib.md5(salt + str(time.time()) + str(teamid)).hexdigest()
    open('pass.txt', 'a').write('team' + str(teamid) + ':ctf:' + passwd + "\n")
    return passwd


def generate_run_sh(password):
    content = """#!/bin/sh
cd /var/www/html
a2enmod rewrite
service apache2 restart
service mysql restart
echo ctf:%s | chpasswd
echo root:xxxxx | chpasswd
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
service ssh restart
chmod 700 /home/run.sh
sleep 2
/bin/bash""" % password

    return content


def generate_docker_sh(teamid, my_port, my_image):
    content = """#!/bin/sh
docker run -p %d:%d  -p %d:22 -v `pwd`:/home -d  --name team%d -ti %s /home/run.sh
""" % (8800 + teamid, my_port, 2200 + teamid, teamid, my_image)
    return content


def clean(team_number):
    path = os.getcwd()
    files = os.listdir(path)
    files.remove('startawd.py')
    for f in files:
        os.system("rm -rf %s" % f)
    print "相关文件已删除"
    for i in range(team_number):
        os.system("docker stop team%s" % str(i + 1))
        time.sleep(2)
        os.system("docker rm team%s" % str(i + 1))
        print "team%s 靶机已删除" % str(i + 1)


def reset_docker(teamid):
    os.system("docker stop team%s" % str(teamid))
    os.system("docker rm team%s" % str(teamid))
    print "team%s 靶机已关闭" % str(teamid)
    os.system('cd team%s/ && /bin/sh docker.sh' % str(teamid))
    print "team%s 靶机已重置" % str(teamid)


def main(awdimage, team_number, my_port):
    open('pass.txt', 'w').write('')
    for i in range(team_number):
        password = generate_pass(i + 1)
        team_dir = 'team' + str(i + 1)
        os.system('mkdir %s' % team_dir)
        open(team_dir + '/run.sh', 'w').write(generate_run_sh(password))
        open(team_dir + '/docker.sh', 'w').write(generate_docker_sh(i + 1, my_port, awdimage))
        os.system('cd %s/ && /bin/sh docker.sh' % team_dir)
        print '[*] start docker team%s' % str(i+1)
        time.sleep(2)


if __name__ == '__main__':
    try:
        args = parse_args()
        if args.r:
            reset_docker(teamid=args.r)
            exit()
        elif args.c:
            clean(team_number=args.team_number)
            exit()
        else:
            main(awdimage=args.image, team_number=args.team_number, my_port=args.port)
    except Exception as e:
        print e
        print '\tExample: \r\npython ' + sys.argv[0] + " -i awd/web_yunnan_simple:0.1 -t 5"
