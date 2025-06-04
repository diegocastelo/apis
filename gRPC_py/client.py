import grpc
import music_service_pb2
import music_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = music_service_pb2_grpc.MusicServiceStub(channel)

        print("\n🔸 Listando usuários:")
        users = stub.ListUsuarios(music_service_pb2.Empty())
        for u in users.usuarios:
            print(f"- {u.id}: {u.nome} ({u.idade} anos)")

        print("\n🔸 Listando músicas:")
        songs = stub.ListMusicas(music_service_pb2.Empty())
        for s in songs.musicas:
            print(f"- {s.id}: {s.nome} de {s.artista}")

        print("\n🔸 Playlists do usuário 1:")
        playlists = stub.ListPlaylistsDoUsuario(music_service_pb2.UsuarioIdRequest(usuario_id=1))
        for p in playlists.playlists:
            print(f"- {p.id}: {p.nome}")

        print("\n🔸 Músicas da playlist 1:")
        songs = stub.ListMusicasDaPlaylist(music_service_pb2.PlaylistIdRequest(playlist_id=1))
        for s in songs.musicas:
            print(f"- {s.id}: {s.nome}")

        print("\n🔸 Playlists que contêm a música 2:")
        playlists = stub.ListPlaylistsPorMusica(music_service_pb2.MusicaIdRequest(musica_id=2))
        for p in playlists.playlists:
            print(f"- {p.id}: {p.nome}")

if __name__ == '__main__':
    run()
