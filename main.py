import requests
import json
from hyper.contrib import HTTP20Adapter

# 项目首页：https://ljjs.ca163.net/

phone = "13824819841"
password = "440822196809201431"


class LJStudy(object):
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password

        self.session = requests.session()
        self.session.mount("https://jspx.ca163.net", HTTP20Adapter())

        self.headers = {
            ":authority": "jspx.ca163.net",
            ":method": "POST",
            # ":path": "/purchased/get",
            ":scheme": "https",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }

        self.token = None

    def login(self):
        login_api = "https://jspx.ca163.net/users/login"
        self.headers[":path"] = "/users/login"
        data = {
            "phone": self.phone,
            "password": self.password,
            "shop_id": "8"
        }

        print("[!] Try login:", self.phone)

        res = self.session.post(login_api, data=data, headers=self.headers)
        login_ret = json.loads(res.text)

        if login_ret["status"] == "success":
            print("[*] Login success. ")
            self.token = login_ret['result']['token']
        else:
            print("[!] Login failed. Please try again. ")
            exit(0)

    def submit_rate(self, rate):
        sumbit_rate_api = "https://jspx.ca163.net/purchased/sumbitRate"
        self.headers[":path"] = "/purchased/sumbitRate"
        data = {
            "token": self.token,
            "id": "75995",
            "progress": 1,   # 完整进度拉满
            "end_time": "",
            "rate": rate
        }

        res = self.session.post(
            sumbit_rate_api, data=data, headers=self.headers)
        if json.loads(res.text)['status'] == "success":
            print("[*] 学习成功 ✅")

    def get_study_rate(self):
        get_project_api = "https://jspx.ca163.net/purchased/get"
        self.headers[":path"] = "/purchased/get"
        data = {
            "token": self.token,
            "id": "75995"
        }
        res = self.session.post(
            get_project_api, data=data, headers=self.headers)
        rate = json.loads(json.loads(res.text)['result']['rate'])

        for task in rate[:]:
            # print("", task['task_name'])
            for activity in task['task_activities'][:2]:  # 视频 + 电子书
                print("【当前任务】", activity['activitie_name'])
                activity['activeState'] = 2  # 活动状态变绿色
                for resource in activity['resources'][:]:  # 章节
                    print("  ", resource['name'])
                    resource['state'] = 2  # 章节状态变绿色
                    for item in resource['items']:  # 小节
                        print("    ", item['name'])
                        item['progress'] = 1  # 进度条直接拉满
                        item['state'] = 2  # 进度条状态变绿色
                        item['currentTime'] = 0   # 开始时间拉至开头

                        # 每进入一章节，提交一次进度
                        self.submit_rate(json.dumps(rate))

    def run(self):
        self.login()
        self.get_study_rate()


if __name__ == "__main__":
    new_study = LJStudy(phone, password)
    new_study.run()
