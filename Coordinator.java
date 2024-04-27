import java.io.*;
import java.net.*;
import java.util.*;

public class Coordinator {
    private static ServerSocket serverSocket;
    private static List<Socket> participants = new ArrayList<>();
    private static List<String> participantResponses = new ArrayList<>();
    private static int expectedParticipants;
    private static boolean preparePhase = false;

    public static void main(String[] args) {
        try {
            serverSocket = new ServerSocket(12345); // Server socket listening on port 12345
            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter the number of participants: ");
            expectedParticipants = scanner.nextInt();

            // Accept participants until the expected number is reached
            System.out.println("\nWaiting for the participants...");
            while (participants.size() < expectedParticipants) {
                Socket participant = serverSocket.accept();
                participants.add(participant);
                System.out.println("Participant " + (participants.size()) + " connected from: " + participant.getRemoteSocketAddress());

                // If expected number of participants is reached, start the prepare phase
                if (participants.size() == expectedParticipants && !preparePhase) {
                    preparePhase = true;
                    sendPrepareMessage();
                }
            }

            // Receive responses from participants
            receiveResponsesFromParticipants();

            // Make a decision based on received responses
            makeDecision();

            // Calculate the total sum of numbers from participants
            calculateTotalSum();

            // Close all connections
            closeConnections();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void sendPrepareMessage() {
        System.out.println("\nSending PREPARE message to all participants...");
        sendMessageToAll("PREPARE");
    }

    private static void sendMessageToAll(String message) {
        for (Socket participant : participants) {
            try {
                PrintWriter out = new PrintWriter(participant.getOutputStream(), true);
                out.println(message);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private static void receiveResponsesFromParticipants() throws IOException {
        System.out.println();
        for (Socket participant : participants) {
            BufferedReader in = new BufferedReader(new InputStreamReader(participant.getInputStream()));
            String response = in.readLine();
            participantResponses.add(response);
            System.out.println("Received " + response + " response from participant: " + participant.getRemoteSocketAddress());
        }
    }

    private static void makeDecision() {
        if (participantResponses.contains("NO")) {
            System.out.println("\nTransaction aborting...");
            sendMessageToAll("ABORT");
        } else {
            System.out.println("\nTransaction committing...");
            sendMessageToAll("COMMIT");
        }
    }

    private static void calculateTotalSum() throws IOException {
        int totalSum = 0;

        // Receive numbers from each participant and calculate the total sum
        for (Socket participant : participants) {
            BufferedReader in = new BufferedReader(new InputStreamReader(participant.getInputStream()));
            int number = Integer.parseInt(in.readLine());
            totalSum += number;
            System.out.println("Received number " + number + " from participant: " + participant.getRemoteSocketAddress());
        }

        // Display total sum
        System.out.println("\nTotal sum of all numbers received from participants: " + totalSum);
    }

    private static void closeConnections() {
        try {
            serverSocket.close();
            for (Socket participant : participants) {
                participant.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
