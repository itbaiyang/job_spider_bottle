from bottle import Bottle, run, request
from spider import job_51job, job_yc
app = Bottle()


@app.get('/login')
def login():
    print(request.method)
    return "success!"


@app.post('/spider_job')
def hello():
    print(request.method)
    if request.POST:
        data = request.POST.decode()
        print(data['companyName'])
        job_51job.spider_job(data['companyName'])
        job_yc.spider_job(data['companyName'])
        return "success!"
    else:
        return "方法错误"
run(app, host='0.0.0.0', port=8443)
