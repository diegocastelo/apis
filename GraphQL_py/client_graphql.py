import requests

def request_graphql():
    query = '{ hello(name: "Teste") }'
    r = requests.post("http://localhost:5000/graphql", json={"query": query})
    return r.json()
