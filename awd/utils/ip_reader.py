import ipaddress
from .custom_ip_generator import CustomIPGenerator
from .ping import Ping

class IPReader:
    def __init__(self):
        self.ips = []

    def fetch_ips(self, method="file", **kwargs):
        if method == "scan":
            return self.fetch_ips_from_scan(**kwargs)
        elif method == "file":
            return self.fetch_ips_from_file(**kwargs)
        elif method == "cidr":
            return self.fetch_ips_from_cidr(**kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

    def fetch_ips_from_scan(self, network="192.168.1.0/24", is_custom=False,custom_format="test-192-168-1-X-abc123"):
        if is_custom:
            # 如果为自定义 IP，检查格式并生成 IP 列表
            if not custom_format or "X" not in custom_format:
                raise ValueError("Custom format must contain the placeholder 'X'.")
            ip_scan_list =  CustomIPGenerator(ip_format=custom_format).generate_ips()
        else:
            # 如果为普通扫描，解析 CIDR 并生成 IP 列表
            networks = ipaddress.ip_network(network, strict=False)
            ip_scan_list = [str(ip) for ip in networks.hosts()]
        return  Ping(ip_scan_list).ping()


        return ip_scan_list
    def fetch_ips_from_file(self, ip_file="ip_list.txt"):
        try:
            with open(ip_file, "r") as file:
                ips = [line.strip() for line in file.readlines()]
            return ips
        except FileNotFoundError:
            print(f"Error: File '{ip_file}' not found.")
            return []

    def fetch_ips_from_cidr(self, cidr="192.168.1.0/24"):
        network = ipaddress.IPv4Network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]


# 测试
if __name__ == "__main__":
    ip_reader = IPReader()

    # 从扫描方式获取 IP 地址
    ips_from_scan = ip_reader.fetch_ips(method="scan", network="192.168.56.95/24")
    print("IPs from scan:", ips_from_scan)
    # ips_from_scan1 = ip_reader.fetch_ips(method="scan", is_custom=True, custom_format="test-192-168-1-X-abc123")
    # print("IPs from scan1:", ips_from_scan1)


    # 从文件读取 IP 地址
    ips_from_file = ip_reader.fetch_ips(method="file", ip_file="ips.txt")
    print("IPs from file:", ips_from_file)

    # 从 CIDR 地址段获取 IP 地址
    ips_from_cidr = ip_reader.fetch_ips(method="cidr", cidr="192.168.56.91/24")
    print("IPs from CIDR:", ips_from_cidr)
