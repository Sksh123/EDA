import java.io.*;
import java.net.*;
import java.util.*;

public class Subordinate {
    public static void main(String[] args) {
        try {
            // Connect to Coordinator (localhost) on port 12345
            Socket socket = new Socket("localhost", 12345);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            // Display the local port address
            int port = socket.getLocalPort();
            System.out.println("Local port address: " + port);

            // Step 1: Receive PREPARE message from Coordinator
            System.out.println("\nWaiting for PREPARE message from Coordinator...");
            String prepareMessage = in.readLine();
            if ("PREPARE".equals(prepareMessage)) {
                System.out.println("\nReceived PREPARE from Coordinator.");
                Scanner scanner = new Scanner(System.in);
                System.out.print("\nAre you ready to commit? (Enter YES or NO): ");
                String response = scanner.nextLine();
                out.println(response); // Send response to Coordinator
                System.out.println("\nSending " + response + " to the Coordinator.");
            }

            // Step 3: Receive decision from Coordinator
            String decision = in.readLine();
            System.out.println("\nReceived decision from Coordinator: " + decision);

            if (decision.equals("COMMIT")) {
                // Step 4: If the decision is COMMIT, enter a number to send to the Coordinator
                System.out.print("Enter a number to send to the Coordinator: ");
                Scanner scanner = new Scanner(System.in);
                int number = scanner.nextInt();
                out.println(number);  // Send the number to the Coordinator
                System.out.println("Sent number " + number + " to the Coordinator.");
            }

            // Close the connection
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
