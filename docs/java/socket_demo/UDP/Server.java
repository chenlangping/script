package UDP;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class Server {

    private final static int PORT = 37889;
    private final static int BUFFER_LENGTH = 1024;

    public static void main(String[] args) {
        byte[] buf = new byte[BUFFER_LENGTH];
        try {
            DatagramSocket datagramSocket = new DatagramSocket(PORT);
            DatagramPacket datagramPacket = new DatagramPacket(buf, buf.length);

            while (true) {
                datagramSocket.receive(datagramPacket);
                // now the msg is in the buf
                System.out.println("get msg from " + datagramPacket.getAddress().toString() + ":" + datagramPacket.getPort());
                System.out.println(new String(datagramPacket.getData()));
                // don't forget to set length
                datagramPacket.setLength(BUFFER_LENGTH);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
