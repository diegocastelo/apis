from pydantic import BaseModel
from typing import List, Dict


class UsuarioBase(BaseModel):
    nome: str
    idade: int


class Usuario(UsuarioBase):
    id: str


class MusicaBase(BaseModel):
    nome: str
    artista: str


class Musica(MusicaBase):
    id: str


class PlaylistBase(BaseModel):
    nome: str


class Playlist(PlaylistBase):
    id: str
    usuario_id: str
    musicas: List[str] = []
