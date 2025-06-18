from locust import TaskSet, User, task, events, between
import grpc
import time
import music_service_pb2
import music_service_pb2_grpc

class GrpcTasks(TaskSet):
    def on_start(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = music_service_pb2_grpc.MusicServiceStub(self.channel)

    @task
    def listar_usuarios(self):
        start_time = time.time()
        try:
            response = self.stub.ListUsuarios(music_service_pb2.Empty())
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name="listarUsuarios",
                response_time=total_time,
                response_length=len(response.usuarios),
                exception=None
            )
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name="listarUsuarios",
                response_time=total_time,
                response_length=0,
                exception=e
            )

class GrpcUser(User):
    wait_time = between(1, 2)
    tasks = [GrpcTasks]
