import requests, json
from hyper.contrib import HTTP20Adapter

session =  requests.session()
session.mount("https://jspx.ca163.net", HTTP20Adapter())

token = "eyJpdiI6IkJxQU1GeVJ5ZFdKVUh5MXlkdmcrYWc9PSIsInZhbHVlIjoidWw0SXRKanFmNmRZWDlyNFJSYzd3a25tOFNXUFdOdkE2SUM2Q0pJU3ArYUR1dG1OQU5hRGRqSUJiaHFaVXhmQiIsIm1hYyI6ImMwNTg5MjExMTQ0ZWI1NmNlN2ViZjY5NDZjMTNkZTM4Y2RhODc2OTEyYzA1YTdiZWYzMThmOWJmMmVlYzg4ZTkifQ=="

headers = {
    ":authority": "jspx.ca163.net", 
    ":method": "POST", 
    ":path": "/purchased/get",
    ":scheme": "https",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
}

data = {
    "token": token,
    "id": "75995"
}

getProjectData = "https://jspx.ca163.net/purchased/get"
res = session.post(getProjectData, data=data, headers=headers)
rate = json.loads(json.loads(res.text)['result']['rate'])

# print(rate)

sumbitRateUrl = "https://jspx.ca163.net/purchased/sumbitRate"

def submitRate(rate):
    headers = {
        ":authority": "jspx.ca163.net", 
        ":method": "POST", 
        ":path": "/purchased/sumbitRate",
        ":scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }
    data = {
        "token": token,
        "id": "75995", 
        "progress": 1,   # 完整进度拉满
        "end_time": "",
        "rate": rate
    }

    res = session.post(sumbitRateUrl, data=data, headers=headers)
    print(res.text)
    

for task in rate[:]:
#     print("", task['task_name'])
    for activity in task['task_activities'][:2]:  # 视频 + 电子书
        print("【当前任务】", activity['activitie_name'])
        for resource in activity['resources'][:]:  # 章节
            print("  ", resource['name']) 
            resource['state'] = 2  # 章节状态变绿色
            for item in resource['items']:  # 小节
                print("    ", item['name'])  
                item['progress'] = 1  # 进度条直接拉满
                item['state'] = 2  # 进度条状态变绿色
                item['currentTime'] = 0   # 开始时间拉至开头
                                
                # 每进入一章节，提交一次进度
                submitRate(json.dumps(rate))
