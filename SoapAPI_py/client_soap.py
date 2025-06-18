from zeep import Client

def request_soap():
    client = Client("http://localhost:8005/?wsdl")
    return client.service.listarUsuarios()
