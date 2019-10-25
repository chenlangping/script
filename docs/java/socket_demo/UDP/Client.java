package UDP;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Client {
    private final static String SERVER_ADDRESS = "127.0.0.1";
    private final static int SERVER_PORT = 37889;

    public static void main(String[] args) {
        try {
            DatagramSocket datagramSocket = new DatagramSocket();
            // now construct a new UDP package and send it to the client
            String sendMsg = "hello server!";
            DatagramPacket sendPacket = new DatagramPacket(sendMsg.getBytes(), sendMsg.length(), InetAddress.getByName(SERVER_ADDRESS), SERVER_PORT);
            datagramSocket.send(sendPacket);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
