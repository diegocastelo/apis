from zeep import Client

client = Client("http://localhost:8005/soap/?wsdl")

# Usuários
u1_id = client.service.criarUsuario({"nome": "Alice", "idade": 30})
u2_id = client.service.criarUsuario({"nome": "Bob", "idade": 25})

# Músicas
m1_id = client.service.criarMusica({"nome": "Song A", "artista": "Artist X"})
m2_id = client.service.criarMusica({"nome": "Song B", "artista": "Artist Y"})

# Playlist
p1_id = client.service.criarPlaylist(u1_id, {"nome": "Chill"})

# Adicionar músicas
client.service.adicionarMusicaNaPlaylist(p1_id, m1_id)
client.service.adicionarMusicaNaPlaylist(p1_id, m2_id)

print("SOAP populado com sucesso.")
