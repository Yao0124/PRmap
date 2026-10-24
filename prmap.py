#by Yao0124
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

PORT_DICT = {
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP-Server", 68: "DHCP-Client", 69: "TFTP", 110: "POP3",
    111: "RPCBind", 123: "NTP", 135: "MSRPC", 137: "NetBIOS-NS", 138: "NetBIOS-DGM",
    139: "NetBIOS-SSN", 143: "IMAP", 161: "SNMP", 162: "SNMP-Trap", 389: "LDAP",
    465: "SMTPS", 500: "ISAKMP", 514: "Syslog", 587: "SMTP-Submission", 636: "LDAPS",
    873: "Rsync", 993: "IMAPS", 995: "POP3S", 1080: "SOCKS",
    80: "HTTP", 443: "HTTPS", 3000: "Grafana", 3128: "Squid-Proxy", 7001: "WebLogic",
    7002: "WebLogic-SSL", 8000: "HTTP-Alt", 8009: "AJP", 8080: "HTTP-Proxy", 8081: "HTTP-Alt",
    8443: "HTTPS-Alt", 8888: "Jupyter", 9000: "PHP-FPM", 9090: "Prometheus",
    1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 5432: "PostgreSQL", 5900: "VNC",
    5984: "CouchDB", 6379: "Redis", 9042: "Cassandra", 11211: "Memcached",
    27017: "MongoDB", 27018: "MongoDB-Shard",
    445: "SMB", 3389: "RDP",
    2181: "ZooKeeper", 2375: "Docker", 2376: "Docker-TLS", 4369: "Erlang-EPMD", 5601: "Kibana",
    5672: "RabbitMQ", 6443: "Kubernetes-API", 9092: "Kafka", 9200: "Elasticsearch",
    9300: "Elasticsearch-Cluster", 9418: "Git", 15672: "RabbitMQ-Management", 50070: "Hadoop-NameNode",
    1723: "PPTP", 2049: "NFS", 50000: "SAP",
}
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

def server_port_dict(port):
    return PORT_DICT.get(port,'Unknown')

def start(targetIP,targetPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        send = sock.connect((targetIP,targetPort))
        print(f'开放的端口:{targetPort} {server_port_dict(targetPort)}')
    except Exception:
        pass
    finally:
        sock.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('再见')
        os._exit(0)