from locust import HttpUser, constant_pacing, task, events
from requests.adapters import HTTPAdapter
from locust.exception import StopUser
import pandas as pd
import gevent

# Load the CSV
df = pd.read_csv('freq.csv', parse_dates=[0])
df.sort_values('time', inplace=True)
df = df.tail(24 * 60 * 60)
total_row = len(df.index)
start_time = df['time'].iloc[0]

counter = 0


class WebsiteUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=300))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=300))

    wait_time = constant_pacing(1)

    def scheduled_task(self):
        self.client.get("/s0", name="HTTP Request")

    @task
    def load_test(self):
        global counter

        if counter > total_row:
            raise StopUser()

        time_diff = int((df['time'].iloc[counter] -
                        start_time).total_seconds())
        if time_diff == counter:
            frequency = df['frequency'].iloc[counter]
            task_queue = [gevent.spawn(self.scheduled_task)
                          for _ in range(frequency)]
            gevent.joinall(task_queue)

        counter += 1


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test completed.")
