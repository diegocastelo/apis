from spyne import Application, rpc, ServiceBase, Unicode, Integer, Array
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple
import uuid


# -----------------------------
# MODELOS
# -----------------------------

class Usuario(ComplexModel):
    id = Unicode
    nome = Unicode
    idade = Integer


class Musica(ComplexModel):
    id = Unicode
    nome = Unicode
    artista = Unicode


class Playlist(ComplexModel):
    id = Unicode
    nome = Unicode
    usuario_id = Unicode
    musicas = Array(Unicode)


# -----------------------------
# DADOS EM MEMÓRIA
# -----------------------------

usuarios = {}
musicas = {}
playlists = {}


# -----------------------------
# SERVIÇO SOAP
# -----------------------------

class MusicService(ServiceBase):

    @rpc(Usuario, _returns=Unicode)
    def criarUsuario(ctx, usuario):
        uid = str(uuid.uuid4())
        usuario.id = uid
        usuarios[uid] = usuario
        return uid

    @rpc(_returns=Array(Usuario))
    def listarUsuarios(ctx):
        return list(usuarios.values())

    @rpc(Musica, _returns=Unicode)
    def criarMusica(ctx, musica):
        mid = str(uuid.uuid4())
        musica.id = mid
        musicas[mid] = musica
        return mid

    @rpc(_returns=Array(Musica))
    def listarMusicas(ctx):
        return list(musicas.values())

    @rpc(Unicode, Playlist, _returns=Unicode)
    def criarPlaylist(ctx, usuario_id, playlist):
        if usuario_id not in usuarios:
            return "Usuário não encontrado"
        pid = str(uuid.uuid4())
        playlist.id = pid
        playlist.usuario_id = usuario_id
        playlist.musicas = []
        playlists[pid] = playlist
        return pid

    @rpc(Unicode, _returns=Array(Playlist))
    def listarPlaylistsDoUsuario(ctx, usuario_id):
        return [p for p in playlists.values() if p.usuario_id == usuario_id]

    @rpc(Unicode, _returns=Array(Musica))
    def listarMusicasDaPlaylist(ctx, playlist_id):
        playlist = playlists.get(playlist_id)
        if not playlist:
            return []
        return [musicas[mid] for mid in playlist.musicas if mid in musicas]

    @rpc(Unicode, Unicode, _returns=Unicode)
    def adicionarMusicaNaPlaylist(ctx, playlist_id, musica_id):
        if playlist_id not in playlists:
            return "Playlist não encontrada"
        if musica_id not in musicas:
            return "Música não encontrada"
        if musica_id not in playlists[playlist_id].musicas:
            playlists[playlist_id].musicas.append(musica_id)
        return "Música adicionada com sucesso"

    @rpc(Unicode, _returns=Array(Playlist))
    def listarPlaylistsPorMusica(ctx, musica_id):
        return [p for p in playlists.values() if musica_id in p.musicas]


# -----------------------------
# APLICAÇÃO SOAP
# -----------------------------

application = Application(
    services=[MusicService],
    tns='musica.soap.api',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, wsgi_app)
