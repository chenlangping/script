package TCP;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;

public class ServerThread implements Runnable {
    public static final String END_MESSAGE = "bye";
    private Socket client = null;

    public ServerThread(Socket client) {
        this.client = client;
    }

    @Override
    public void run() {
        try {
            // out -> send msg to client
            PrintStream out = new PrintStream(client.getOutputStream());
            // buf -> get msg from client
            BufferedReader buf = new BufferedReader(new InputStreamReader(client.getInputStream()));
            while (true) {
                String line = buf.readLine();
                if (line == null || line.length() == 0 || END_MESSAGE.equals(line)) {
                    break;
                } else {
                    // do something with the msg, and in this demo just send the same msg back to client

                    // server show!
                    System.out.println("get from client = " + line);

                    // send to the client!
                    out.println("get :" + line);
                }
            }
            out.close();
            buf.close();
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
