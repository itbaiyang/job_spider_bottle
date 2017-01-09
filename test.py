import requests
# url = 'http://localhost:8443/spider_job'
url = 'http://123.206.29.128:8443/spider_job'
# url = 'http://localhost:8080/login'
data = {
    'companyName': '百度在线网络技术（北京）有限公司'
}
# response = requests.get(url)
response = requests.post(url, data=data)
print(response.status_code)
print(response.reason)
# print(response.headers)
# print(response.request)
# print(response.text)
# print(response.raw)
