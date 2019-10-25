package TCP;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;

public class Client {
    private static final String END_MESSAGE = "bye";
    private static final String SERVER_ADDRESS = "127.0.0.1";
    private static final int PORT = 37889;
    private static final int TIMEOUT = 10000;

    public static void main(String[] args) {
        try {
            Socket client = new Socket(SERVER_ADDRESS, PORT);
            client.setSoTimeout(TIMEOUT);

            // get user's input
            BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
            // send msg to server
            PrintStream out = new PrintStream(client.getOutputStream());
            // get msg from server
            BufferedReader buf = new BufferedReader(new InputStreamReader(client.getInputStream()));

            while (true) {
                System.out.print("input:");
                String msg = input.readLine();
                //send msg to server
                out.println(msg);

                if (msg == null || msg.length() == 0 || END_MESSAGE.equals(msg)) {
                    break;
                } else {
                    // get msg from server
                    System.out.println(buf.readLine());
                }
            }
            input.close();
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}
