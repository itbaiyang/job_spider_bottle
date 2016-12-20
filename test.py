import requests
url = 'http://localhost:8443/spider_job'
# url = 'http://localhost:8080/login'
data = {
    # 'company': '123'
    'companyName': 'CBC(北京)信用管理有限公司'
}
# response = requests.get(url)
response = requests.post(url, data=data)
print(response.status_code)
print(response.reason)
# print(response.headers)
# print(response.request)
# print(response.text)
# print(response.raw)
