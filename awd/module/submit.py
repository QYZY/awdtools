import requests


class Submit:
    def __init__(self, url, token=None, timeout=10, ):
        """
        初始化 SubmitModule。

        :param submit_url: 提交 Flag 的 URL。
        :param auth_token: 认证 Token（可选）。
        :param timeout: 请求超时时间（秒）。
        """

        self.submit_url = url
        self.token = token
        self.timeout = timeout

    def submit(self, flag):
        response = requests.get(self.submit_url+flag)
        return response.text


if __name__ == "__main__":
    submit = Submit(url="https://ctf.bugku.com/pvp/submit.html?token={}&flag=",token="123", timeout=10)
    print(submit.submit(flag="test"))
