from bottle import Bottle, run, request
from spider import job_51job
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
        print()
        job_51job.spider_job(data['company'])
        return "success!"
    else:
        return "方法错误"
run(app, host='0.0.0.0', port=8443)
