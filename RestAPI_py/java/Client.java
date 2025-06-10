package RestAPI_py.java;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Client {

    private static final String BASE_URL = "http://localhost:8000";

    public static void main(String[] args) throws Exception {
        // Criar usuário
        String usuarioJson = "{\"nome\": \"João\", \"idade\": 30}";
        String usuario = post("/usuarios", usuarioJson);
        System.out.println("Usuário criado: " + usuario);

        // Criar música
        String musicaJson = "{\"nome\": \"Imagine\", \"artista\": \"John Lennon\"}";
        String musica = post("/musicas", musicaJson);
        System.out.println("Música criada: " + musica);

        // Extrair IDs
        String usuarioId = extractId(usuario);
        String musicaId = extractId(musica);

        // Criar playlist
        String playlistJson = "{\"nome\": \"Favoritas\"}";
        String playlist = post("/usuarios/" + usuarioId + "/playlists", playlistJson);
        System.out.println("Playlist criada: " + playlist);

        String playlistId = extractId(playlist);

        // Adicionar música na playlist
        String respAdd = post("/playlists/" + playlistId + "/musicas/" + musicaId, "");
        System.out.println(respAdd);

        // Listar músicas da playlist
        String musicas = get("/playlists/" + playlistId + "/musicas");
        System.out.println("Músicas na playlist: " + musicas);

        // Remover música da playlist
        String respDel = delete("/playlists/" + playlistId + "/musicas/" + musicaId);
        System.out.println(respDel);
    }

    private static String post(String path, String json) throws IOException {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        if (!json.isEmpty()) {
            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = json.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }
        }

        return readResponse(conn);
    }

    private static String get(String path) throws IOException {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        return readResponse(conn);
    }

    private static String delete(String path) throws IOException {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("DELETE");
        return readResponse(conn);
    }

    private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() < HttpURLConnection.HTTP_BAD_REQUEST) ?
                conn.getInputStream() : conn.getErrorStream();

        BufferedReader in = new BufferedReader(new InputStreamReader(is));
        String inputLine;
        StringBuilder content = new StringBuilder();

        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }

        in.close();
        return content.toString();
    }

    private static String extractId(String json) {
        int start = json.indexOf("\"id\":\"") + 6;
        int end = json.indexOf("\"", start);
        return json.substring(start, end);
    }
}
