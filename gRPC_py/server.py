import grpc
from concurrent import futures
import music_service_pb2
import music_service_pb2_grpc

# Dados simulados
usuarios = [
    music_service_pb2.Usuario(id=1, nome="Alice", idade=30),
    music_service_pb2.Usuario(id=2, nome="Bob", idade=25)
]

musicas = [
    music_service_pb2.Musica(id=1, nome="Song A", artista="Artist X"),
    music_service_pb2.Musica(id=2, nome="Song B", artista="Artist Y")
]

playlists = [
    {"id": 1, "nome": "Chill", "usuario_id": 1, "musicas": [1, 2]},
    {"id": 2, "nome": "Rock", "usuario_id": 2, "musicas": [2]}
]

class MusicService(music_service_pb2_grpc.MusicServiceServicer):
    def ListUsuarios(self, request, context):
        return music_service_pb2.UsuariosResponse(usuarios=usuarios)

    def ListMusicas(self, request, context):
        return music_service_pb2.MusicasResponse(musicas=musicas)

    def ListPlaylistsDoUsuario(self, request, context):
        result = [
            music_service_pb2.Playlist(id=p["id"], nome=p["nome"])
            for p in playlists if p["usuario_id"] == request.usuario_id
        ]
        return music_service_pb2.PlaylistsResponse(playlists=result)

    def ListMusicasDaPlaylist(self, request, context):
        for p in playlists:
            if p["id"] == request.playlist_id:
                musicas_na_playlist = [m for m in musicas if m.id in p["musicas"]]
                return music_service_pb2.MusicasResponse(musicas=musicas_na_playlist)
        return music_service_pb2.MusicasResponse()

    def ListPlaylistsPorMusica(self, request, context):
        result = [
            music_service_pb2.Playlist(id=p["id"], nome=p["nome"])
            for p in playlists if request.musica_id in p["musicas"]
        ]
        return music_service_pb2.PlaylistsResponse(playlists=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    music_service_pb2_grpc.add_MusicServiceServicer_to_server(MusicService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
