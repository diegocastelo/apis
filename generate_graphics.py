import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt

configs = [
    ("rest", "http://localhost:8000"),
    ("graphql", "http://localhost:5000"),
    ("soap", None),
    ("grpc", None)
]

for name, host in configs:
    print(f"Executando teste para: {name.upper()}")
    cmd = ["locust", "-f", f"locust_{name}.py", "--headless", "-u", "10", "-r", "2", "-t", "10s", "--csv", f"{name}_results"]
    if host:
        cmd.extend(["--host", host])
    subprocess.run(cmd)
    time.sleep(2)

# Geração do gráfico
labels = []
values = []

for name, host in configs:
    csv_file = f"{name}_results_stats.csv"
    try:
        df = pd.read_csv(csv_file)
        target = "/usuarios" if name != "graphql" else "/graphql"
        linha = df[df["Name"] == target]
        if linha.empty:
            linha = df[df["Name"].str.contains("listarUsuarios")]
        media = linha["Average Response Time"].values[0]
        labels.append(name.upper())
        values.append(media)
    except Exception as e:
        print(f"Erro ao processar {name}: {e}")

plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=["skyblue", "lightgreen", "orange", "salmon"])
plt.title("Tempo Médio de Resposta por API")
plt.xlabel("API")
plt.ylabel("Tempo médio (ms)")
plt.grid(axis='y')
plt.savefig("comparativo_apis.png")
plt.show()
