import subprocess
import platform
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class Ping:
    def __init__(self, ips, count=1, timeout=5, max_workers=10):
        """
        初始化 Ping 对象

        :param ips: 要 ping 的 IP 地址列表
        :param count: ping 请求的次数
        :param timeout: 超时时间（单位：秒）
        :param max_workers: 最大线程数
        """
        self.ips = ips
        self.count = count
        self.timeout = timeout
        self.max_workers = max_workers
        self.reachable_ips = []

    def ping(self):
        """启动多线程执行 ping 操作"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交 ping 任务
            future_to_ip = {executor.submit(self._ping_ip, ip): ip for ip in self.ips}

            # 获取任务执行结果
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    if result:
                        self.reachable_ips.append(ip)
                except Exception as exc:
                    print(f"{ip} generated an exception: {exc}")
        return self.reachable_ips

    def _ping_ip(self, ip):
        """单独的 ping 操作，用于线程池中的每个任务"""
        system = platform.system().lower()

        # 根据操作系统设置 ping 命令
        if system == "windows":
            command = ["ping", ip, "-n", str(self.count), "-w", str(self.timeout * 1000)]  # Windows timeout in ms
        else:
            command = ["ping", ip, "-c", str(self.count), "-W", str(self.timeout)]  # Linux/macOS timeout in seconds

        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=self.timeout)
            print(f"{ip} is alive")
            return True  # 如果 ping 成功，返回 True
        except subprocess.CalledProcessError:
            return False  # 如果 ping 失败，返回 False
        except subprocess.TimeoutExpired:
            return False  # 如果超时，返回 False