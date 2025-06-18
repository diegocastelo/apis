from locust import User, task, events
from zeep import Client
import time

class SoapUser(User):
    def on_start(self):
        self.client = Client("http://localhost:8005/soap/?wsdl")

    @task
    def listar_usuarios(self):
        start_time = time.time()
        try:
            response = self.client.service.listarUsuarios()
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="SOAP",
                name="listarUsuarios",
                response_time=total_time,
                response_length=len(response),
                exception=None
            )
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="SOAP",
                name="listarUsuarios",
                response_time=total_time,
                response_length=0,
                exception=e
            )
