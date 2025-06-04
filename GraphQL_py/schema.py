import graphene

# ==== TYPES ====

class Musica(graphene.ObjectType):
    id = graphene.String()
    nome = graphene.String()
    artista = graphene.String()

class Playlist(graphene.ObjectType):
    id = graphene.String()
    nome = graphene.String()
    usuario_id = graphene.String()
    musicas = graphene.List(graphene.String)

class Usuario(graphene.ObjectType):
    id = graphene.String()
    nome = graphene.String()
    idade = graphene.Int()

class GenericResponse(graphene.ObjectType):
    result = graphene.String()

# ==== INPUT TYPES ====

class UsuarioInput(graphene.InputObjectType):
    nome = graphene.String(required=True)
    idade = graphene.Int(required=True)

class MusicaInput(graphene.InputObjectType):
    nome = graphene.String(required=True)
    artista = graphene.String(required=True)

class PlaylistInput(graphene.InputObjectType):
    nome = graphene.String(required=True)
    usuario_id = graphene.String(required=True)
    musicas = graphene.List(graphene.String)

class AdicionarMusicaNaPlaylistInput(graphene.InputObjectType):
    playlist_id = graphene.String(required=True)
    musica_id = graphene.String(required=True)

# ==== QUERIES ====

class Query(graphene.ObjectType):
    listar_usuarios = graphene.List(Usuario)
    listar_musicas = graphene.List(Musica)
    listar_playlists_do_usuario = graphene.List(Playlist, usuario_id=graphene.String(required=True))
    listar_musicas_da_playlist = graphene.List(Musica, playlist_id=graphene.String(required=True))
    listar_playlists_por_musica = graphene.List(Playlist, musica_id=graphene.String(required=True))

    def resolve_listar_usuarios(root, info):
        return []

    def resolve_listar_musicas(root, info):
        return []

    def resolve_listar_playlists_do_usuario(root, info, usuario_id):
        return []

    def resolve_listar_musicas_da_playlist(root, info, playlist_id):
        return []

    def resolve_listar_playlists_por_musica(root, info, musica_id):
        return []

# ==== MUTATIONS ====

class CriarUsuario(graphene.Mutation):
    class Arguments:
        usuario = UsuarioInput(required=True)

    Output = GenericResponse

    def mutate(root, info, usuario):
        return GenericResponse(result="Usuário criado com sucesso.")

class CriarMusica(graphene.Mutation):
    class Arguments:
        musica = MusicaInput(required=True)

    Output = GenericResponse

    def mutate(root, info, musica):
        return GenericResponse(result="Música criada com sucesso.")

class CriarPlaylist(graphene.Mutation):
    class Arguments:
        playlist = PlaylistInput(required=True)

    Output = GenericResponse

    def mutate(root, info, playlist):
        return GenericResponse(result="Playlist criada com sucesso.")

class AdicionarMusicaNaPlaylist(graphene.Mutation):
    class Arguments:
        input = AdicionarMusicaNaPlaylistInput(required=True)

    Output = GenericResponse

    def mutate(root, info, input):
        return GenericResponse(result="Música adicionada à playlist.")

class Mutation(graphene.ObjectType):
    criar_usuario = CriarUsuario.Field()
    criar_musica = CriarMusica.Field()
    criar_playlist = CriarPlaylist.Field()
    adicionar_musica_na_playlist = AdicionarMusicaNaPlaylist.Field()

# ==== SCHEMA ====

schema = graphene.Schema(query=Query, mutation=Mutation)
