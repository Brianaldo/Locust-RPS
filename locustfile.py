from locust import HttpUser, constant_pacing, task
from requests.adapters import HTTPAdapter


class WebsiteUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=300))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=300))

    wait_time = constant_pacing(1)

    @task
    def scheduled_task(self):
        self.client.get("/s0", name="HTTP Request")
