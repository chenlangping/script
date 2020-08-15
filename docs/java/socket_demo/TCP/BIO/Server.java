import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * @author chenlangping
 * @date 2020/8/10
 */
public class Server {

    public static void main(String[] args) throws IOException {
        // Thread Pool
        ExecutorService executor = Executors.newFixedThreadPool(100);

        ServerSocket serverSocket = new ServerSocket(8088);
        while (true) {
            Socket socket = serverSocket.accept();

            // let thread pool to deal with
            executor.submit(new ConnectIOnHandler(socket));
        }
    }


}

class ConnectIOnHandler extends Thread {
    private Socket socket;
    public final String END_MESSAGE = "bye";

    public ConnectIOnHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try {
            PrintStream out = new PrintStream(socket.getOutputStream());
            BufferedReader buf = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            while (true) {
                String line = buf.readLine();
                if (line == null || line.length() == 0 || END_MESSAGE.equals(line)) {
                    break;
                } else {
                    // server show!
                    System.out.println("get from client = " + line);

                    // send to the client!
                    out.println("get :" + line);
                }
            }
            out.close();
            buf.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


