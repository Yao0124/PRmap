# Copyright (c) 2026 Yao0124
# SPDX-License-Identifier: MIT
import socket
import concurrent.futures
import sys
import time
import argparse
import pyfiglet
from packaging.utils import parse_wheel_filename
import os

BLUE = '\033[94m'
RESET = '\033[0m'
logo = pyfiglet.figlet_format("PRmap", font="standard")
print(f"{BLUE}{logo}{RESET}")
print('by Yao0124')

futureList = []
parser = argparse.ArgumentParser(
    description='prmap 一款端口扫描工具'
)
parser.add_argument('-ip','--IPadders',dest='IPadders',help='目标IP')
parser.add_argument('-p','--port',dest='port',type=int,help='指定扫描单个端口')
parser.add_argument('-p1','--ports1',dest='ports1',type=int,help='起始端口（如果要扫描1-1000端口，这里就写1）：')
parser.add_argument('-p2','--ports2',dest='ports2',type=int,help='结束端口（如果要扫描1-1000端口，这里就写1000）：')
parser.add_argument('-w','--work',dest='work',type=int,default=5,help='线程数 默认5')

def main():
    args = parser.parse_args()
    targetIP = args.IPadders
    targetPort = args.port
    targetPorts1 = args.ports1
    targetPorts2 = args.ports2
    work = args.work

    if args.IPadders is None and args.port is None and args.ports1 is None and args.ports2 is None:
        parser.print_help()
        exit(0)

    if args.port: #如果用户输入了指定端口就调用start
        print(f'正在扫描指定端口:{args.port}，线程数：{args.work}')
        args_start = start(targetIP,targetPort)
        if args_start:
            print(f'开放的端口:{args_start}')

    elif args.ports1 and args.ports2:#如果用户指定了端口范围就调用futu
        print(f'正在扫描范围为{targetPorts1}和{targetPorts2}的端口,线程数：{args.work}')
        futu(targetIP,args.ports1,args.ports2,work)

def futu(targetIP,targetPorts1,targetPorts2,work):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        for port in range(targetPorts1,targetPorts2 + 1):
            futureList.append(executor.submit(start, targetIP, port))
        for future in concurrent.futures.as_completed(futureList):
            result = future.result()

def start(targetIP,targetPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        send = sock.connect((targetIP,targetPort))
        print(f'开放的端口:',targetPort)
    except socket.timeout:
        pass
    sock.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('再见')
        os._exit(0)
