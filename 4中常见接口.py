import hashlib
import os
import random

import time
from locust import HttpUser,task,between
from locust import TaskSet


class ApiDemo(TaskSet):
    wait_time = between(1, 2)
    @task(1)
    #get类型接口
    def getinfo(self):
        id=random.randint(1,100)
        with self.client.get("/pinter/com/getSku",params={"id":id},catch_response=True) as respon:
            if respon.json()["code"]=="0":
               respon.success()
            else:
                respon.failure("断言失败")
    @task(1)
    #k=v类型post接口
    def post1(self):
        with open(r"./userinfo.txt")as f:
            result=f.readlines()
            for i in result:
                i.strip()
                print(i[0])
        self.client.post("/pinter/com/login",data={"userName":"admin","password":"1234"})
    @task(1)
    #json类型post接口
    def post2(self):
        header={"content-type":"application"}
        self.client.post("/pinter/com/register",json={"userName":"test","password":"1234","gender":1,"phoneNum":"110","email":"beihe@163.com","address":"Beijing"})
    @task(1)
    # k=json混合类型post接口
    def post3(self):
        self.client.post("/pinter/com/buy",data={"param":{"skuId":123,"num":10}})
    @task
    #需要签名验证接口
    def post4(self):
        phone = "18031443067"
        optcode = "testfan"
        timestam = time.time() * 1000
        after_timestam = int(timestam)
        mysign = phone + optcode + str(after_timestam)
        md5_sign = hashlib.md5(mysign.encode(encoding="utf-8")).hexdigest()
        self.client.post("/pinter/com/userInfo",json={"phoneNum":"18031443067","optCode":"testfan","timestamp":after_timestam,"sign":md5_sign})

class AddUser(HttpUser):
    tasks=[ApiDemo]
    host="http://localhost:8080"
if __name__ == '__main__':
    os.system("locust -f Study.py --host=http://localhost:8080 --web-host=127.0.0.1")
