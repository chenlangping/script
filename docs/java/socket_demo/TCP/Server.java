package TCP;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    private final static int PORT = 37889;

    public static void main(String[] args) {
        try {
            ServerSocket server = new ServerSocket(PORT);
            Socket client;
            while (true) {
                client = server.accept();
                System.out.println("get connect from " + client.getInetAddress());
                new Thread(new ServerThread(client)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
