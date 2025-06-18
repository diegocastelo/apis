import requests

BASE = "http://localhost:8000"

# Usuários
u1 = requests.post(f"{BASE}/usuarios", json={"nome": "Alice", "idade": 30}).json()
u2 = requests.post(f"{BASE}/usuarios", json={"nome": "Bob", "idade": 25}).json()

# Músicas
m1 = requests.post(f"{BASE}/musicas", json={"nome": "Song A", "artista": "Artist X"}).json()
m2 = requests.post(f"{BASE}/musicas", json={"nome": "Song B", "artista": "Artist Y"}).json()

# Playlist para usuário 1
p1 = requests.post(f"{BASE}/usuarios/{u1['id']}/playlists", json={"nome": "Chill"}).json()

# Adicionar músicas na playlist
requests.post(f"{BASE}/playlists/{p1['id']}/musicas/{m1['id']}")
requests.post(f"{BASE}/playlists/{p1['id']}/musicas/{m2['id']}")