from locust import HttpUser, LoadTestShape, between, task, events
from requests.adapters import HTTPAdapter

class WebsiteUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=300))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=300))

    wait_time = between(1, 5)

    @task
    def load_test(self):
        self.client.get("/s0", name="HTTP Request")
        
        
class StagesShapeWithCustomUsers(LoadTestShape):

    stages = [
        {"duration":  10 * 60, "users": 1, "spawn_rate": 1, "user_classes": [WebsiteUser]},
        {"duration":  10 * 60, "users": 2, "spawn_rate": 1, "user_classes": [WebsiteUser]},
        {"duration":  15 * 60, "users": 5, "spawn_rate": 2, "user_classes": [WebsiteUser]},
        {"duration":  15 * 60, "users": 10, "spawn_rate": 2, "user_classes": [WebsiteUser]},
        {"duration":  15 * 60, "users": 30, "spawn_rate": 3, "user_classes": [WebsiteUser]},
        {"duration":  20 * 60, "users": 50, "spawn_rate": 5, "user_classes": [WebsiteUser]},
        {"duration":  20 * 60, "users": 100, "spawn_rate": 10, "user_classes": [WebsiteUser]},
        {"duration":  15 * 60, "users": 300, "spawn_rate": 5, "user_classes": [WebsiteUser]},
        {"duration":  10 * 60, "users": 200, "spawn_rate": 5, "user_classes": [WebsiteUser]},
        {"duration":  10 * 60, "users": 10, "spawn_rate": 2, "user_classes": [WebsiteUser]},
        {"duration":  15 * 60, "users": 5, "spawn_rate": 2, "user_classes": [WebsiteUser]},
        {"duration":  10 * 60, "users": 2, "spawn_rate": 1, "user_classes": [WebsiteUser]},
        {"duration":  10 * 60, "users": 1, "spawn_rate": 1, "user_classes": [WebsiteUser]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
    
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test completed.")

# locust -f locustfile.py --headless -H http://34.87.71.66:31113 --run-time 60m --stop-timeout 30s