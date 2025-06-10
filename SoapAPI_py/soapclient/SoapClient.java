package soapclient;

public class SoapClient {

    public static void main(String[] args) {
        try {
            // Inicializa o serviço
            MusicServiceImplService service = new MusicServiceImplService();
            MusicService port = service.getMusicServiceImplPort();

            // Criar usuário
            Usuario usuario = new Usuario();
            usuario.setNome("Maria");
            usuario.setIdade(28);
            String usuarioId = port.criarUsuario(usuario);
            System.out.println("Usuário criado com ID: " + usuarioId);

            // Criar música
            Musica musica = new Musica();
            musica.setNome("Yellow Submarine");
            musica.setArtista("The Beatles");
            String musicaId = port.criarMusica(musica);
            System.out.println("Música criada com ID: " + musicaId);

            // Criar playlist
            Playlist playlist = new Playlist();
            playlist.setNome("Playlist da Maria");
            String playlistId = port.criarPlaylist(usuarioId, playlist);
            System.out.println("Playlist criada com ID: " + playlistId);

            // Adicionar música na playlist
            String resp = port.adicionarMusicaNaPlaylist(playlistId, musicaId);
            System.out.println("Adição de música: " + resp);

            // Listar músicas da playlist
            System.out.println("Músicas da playlist:");
            for (Musica m : port.listarMusicasDaPlaylist(playlistId)) {
                System.out.println("- " + m.getNome() + " por " + m.getArtista());
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
