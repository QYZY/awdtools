class CustomIPGenerator:
    def __init__(self, ip_format, range_start=0, range_end=255):
        """
        初始化自定义 IP 地址生成器

        :param ip_format: 自定义的 IP 地址格式，例如 "test-192-168-X"
        :param range_start: 占位符 X 的起始值（包含）
        :param range_end: 占位符 X 的结束值（包含）
        """
        self.ip_format = ip_format
        self.range_start = range_start
        self.range_end = range_end

    def generate_ips(self):
        """
        生成所有自定义 IP 地址

        :return: 返回生成的 IP 地址列表
        """
        if "X" not in self.ip_format:
            raise ValueError("The IP format must contain the placeholder 'X'.")

        return [
            self.ip_format.replace("X", str(i))
            for i in range(self.range_start, self.range_end + 1)
        ]

    def save_ips(self, out_put_file="custom_ip_list.txt"):
        """
        保存生的的自定义ip列表至文件

        :param out_put_file:
        :return:
        """
        with open(out_put_file, "w") as f:
            for ip in self.generate_ips():
                f.write(ip + "\n")


if __name__ == "__main__":
    cig = CustomIPGenerator("test-192-168-X-123", 0, 255)
    print(cig.generate_ips())
    cig.save_ips()
