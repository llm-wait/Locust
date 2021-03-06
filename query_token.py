import os
from locust import HttpUser
from locust import TaskSet
from locust import between
from locust import task
#token关联
class ApiQuery(TaskSet):
  @task
  def login(self):
      resp=self.client.post("/pinter/bank/api/login2",data={"userName":"admin","password":1234})
      login_token=resp.json()["data"]
      return login_token
  @task
  def query_cookie(self):
      header = {"testfan-token": self.on_start()}
      res=self.client.get("/pinter/bank/api/query2",params={"userName":"admin"},headers=header)
      print(res.json())
  def on_start(self):
      self.login()

class AddUser(HttpUser):
    tasks=[ApiQuery]
    wait_time = between(1,2)
    host="http://127.0.0.1:8080"


if __name__ == '__main__':
    os.system("locust -f Demo3.py --host=http://127.0.0.1:8080 --web-host=127.0.0.1")