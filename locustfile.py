from locust import HttpUser, task

class BaseTester(HttpUser):
    @task
    def test_root(self):
        self.client.get("/fast")

    @task
    def test_async(self):
        self.client.get("/slow")
