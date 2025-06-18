import json
import matplotlib.pyplot as plt

# Define os arquivos JSON gerados pelo K6
arquivos = {
    "REST": "rest_k6.json",
    "GraphQL": "graphql_k6.json",
    "SOAP": "soap_k6.json"
}

labels = []
tempos = []

for nome, caminho in arquivos.items():
    try:
        with open(caminho) as f:
            data = json.load(f)
            metrics = data['metrics']
            tempo_medio = metrics['http_req_duration']['avg']  # média em ms
            labels.append(nome)
            tempos.append(tempo_medio)
    except Exception as e:
        print(f"Erro ao processar {nome}: {e}")

plt.figure(figsize=(10, 6))
plt.bar(labels, tempos, color=["skyblue", "lightgreen", "orange"])
plt.yscale("log")
plt.title("Tempo Médio de Resposta por API (k6)")
plt.xlabel("API")
plt.ylabel("Tempo médio (ms) [escala log]")
plt.grid(axis='y')
plt.savefig("grafico_k6.png")
plt.show()