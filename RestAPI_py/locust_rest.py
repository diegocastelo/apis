from locust import HttpUser, task

class RestUser(HttpUser):
    @task
    def get_usuarios(self):
        self.client.get("/usuarios")

