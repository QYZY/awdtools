import os
import paramiko
from scp import SCPClient
from datetime import datetime


class SSHBackup:
    def __init__(self, hostname, username, password=None, port=22, key_file=None):
        """
        初始化 SSHBackup。

        :param hostname: 远程主机地址。
        :param username: SSH 用户名。
        :param password: SSH 密码（如果使用密钥，则为 None）。
        :param port: SSH 端口，默认 22。
        :param key_file: 私钥文件路径（如果使用密钥登录）。
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.key_file = key_file
        self.ssh_client = None

    def connect(self):
        """建立 SSH 连接。"""
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.key_file:
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_file,
                )
            else:
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                )
            return True, "SSH connection established."
        except Exception as e:
            return False, f"Failed to connect to {self.hostname}: {e}"

    def backup(self, remote_path, local_backup_path="./backups", archive_name=None):
        """
        将远程文件或目录打包并下载到本地。

        :param remote_path: 远程文件或目录路径。
        :param local_backup_path: 本地备份路径。
        :param archive_name: 自定义打包文件名（默认基于时间戳生成）。
        :return: 备份文件路径或错误信息。
        """
        if not self.ssh_client:
            return False, "SSH connection is not established. Call `connect()` first."

        os.makedirs(local_backup_path, exist_ok=True)

        # 生成远程打包文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = archive_name or f"backup_{timestamp}.tar.gz"
        remote_archive_path = f"/tmp/{archive_name}"

        try:
            # 打包远程目录
            stdin, stdout, stderr = self.ssh_client.exec_command(
                f"tar -czf {remote_archive_path} -C {os.path.dirname(remote_path)} {os.path.basename(remote_path)}"
            )
            stderr_output = stderr.read().decode()
            if stderr_output:
                return False, f"Error during archive creation: {stderr_output.strip()}"

            # 下载打包文件
            with SCPClient(self.ssh_client.get_transport()) as scp:
                local_archive_path = os.path.join(local_backup_path, archive_name)
                scp.get(remote_archive_path, local_path=local_archive_path)

            # 删除远程打包文件
            self.ssh_client.exec_command(f"rm -f {remote_archive_path}")

            return True, f"Backup completed: {local_archive_path}"

        except Exception as e:
            return False, f"Backup failed: {e}"

    def disconnect(self):
        """断开 SSH 连接。"""
        if self.ssh_client:
            self.ssh_client.close()


# 示例用法
if __name__ == "__main__":
    # 远程主机信息
    remote_host = "219.217.199.214"
    username = "kali"
    password = "kali"
    remote_path = "/var/www/html"

    # 初始化 SSHBackup
    backup_client = SSHBackup(hostname=remote_host, username=username, password=password)

    # 建立 SSH 连接
    success, message = backup_client.connect()
    print(message)

    if success:
        # 执行备份
        success, message = backup_client.backup(remote_path=remote_path, local_backup_path="./backups")
        print(message)

        # 断开连接
        backup_client.disconnect()
