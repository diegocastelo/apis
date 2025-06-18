from fastapi import FastAPI, HTTPException
from typing import List, Dict
import models as m
from uuid import uuid4

app = FastAPI()


# -----------------------------
# DADOS EM MEMÓRIA
# -----------------------------

usuarios: Dict[str, m.Usuario] = {}
musicas: Dict[str, m.Musica] = {}
playlists: Dict[str, m.Playlist] = {}


# -----------------------------
# USUÁRIOS
# -----------------------------

@app.post("/usuarios", response_model=m.Usuario)
def criar_usuario(usuario: m.UsuarioBase):
    uid = str(uuid4())
    novo = m.Usuario(id=uid, **usuario.dict())
    usuarios[uid] = novo
    return novo


@app.get("/usuarios", response_model=List[m.Usuario])
def listar_usuarios():
    return list(usuarios.values())


# -----------------------------
# MÚSICAS
# -----------------------------

@app.post("/musicas", response_model=m.Musica)
def criar_musica(musica: m.MusicaBase):
    mid = str(uuid4())
    nova = m.Musica(id=mid, **musica.dict())
    musicas[mid] = nova
    return nova


@app.get("/musicas", response_model=List[m.Musica])
def listar_musicas():
    return list(musicas.values())


@app.get("/musicas/{musica_id}/playlists", response_model=List[m.Playlist])
def listar_playlists_por_musica(musica_id: str):
    return [p for p in playlists.values() if musica_id in p.musicas]


# -----------------------------
# PLAYLISTS
# -----------------------------

@app.post("/usuarios/{usuario_id}/playlists", response_model=m.Playlist)
def criar_playlist(usuario_id: str, playlist: m.PlaylistBase):
    if usuario_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    pid = str(uuid4())
    nova = m.Playlist(id=pid, usuario_id=usuario_id, nome=playlist.nome, musicas=[])
    playlists[pid] = nova
    return nova


@app.get("/usuarios/{usuario_id}/playlists", response_model=List[m.Playlist])
def listar_playlists_de_usuario(usuario_id: str):
    return [p for p in playlists.values() if p.usuario_id == usuario_id]


@app.get("/playlists/{playlist_id}/musicas", response_model=List[m.Musica])
def listar_musicas_da_playlist(playlist_id: str):
    playlist = playlists.get(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    return [musicas[mid] for mid in playlist.musicas]


@app.post("/playlists/{playlist_id}/musicas/{musica_id}")
def adicionar_musica_na_playlist(playlist_id: str, musica_id: str):
    playlist = playlists.get(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    if musica_id not in musicas:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    if musica_id not in playlist.musicas:
        playlist.musicas.append(musica_id)
    return {"mensagem": "Música adicionada com sucesso"}


@app.delete("/playlists/{playlist_id}/musicas/{musica_id}")
def remover_musica_da_playlist(playlist_id: str, musica_id: str):
    playlist = playlists.get(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")
    if musica_id in playlist.musicas:
        playlist.musicas.remove(musica_id)
    return {"mensagem": "Música removida com sucesso"}
