from locust import HttpUser, task

class GraphQLUser(HttpUser):
    @task
    def graphql_hello(self):
        query = '{ hello(name: "Teste") }'
        self.client.post("/graphql", json={"query": query})

