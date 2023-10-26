from socket import *

def initialize_client():
    server_name = 'localhost'
    server_port = 11235
    client_socket = socket(AF_INET, SOCK_DGRAM)

    # Long message for testing
    long_msg = """
    If debugging is the process of removing software bugs,
    then programming must be the process of putting them in.
    ― Edsger W. Dijkstra
    Your obligation is that of active participation.
    You should not act as knowledge-absorbing sponges,
    but as whetstones on which we can all sharpen our wits
    ― Edsger W. Dijkstra
    Sometimes it pays to stay in bed on Monday,
    rather than spending the rest of the week debugging Monday’s code.
    ― Dan Salomon
    If carpenters made buildings the way programmers make programs,
    the first woodpecker to come along would destroy all of civilization.
    ― Unknown
    """

    sequence_number = 0  # Initial sequence number

    # Send data using RDT
    rdt_send(client_socket, long_msg, server_name, server_port, sequence_number)

def rdt_send(client_socket, data, server_name, server_port, sequence_number):
    end_of_message = False

    while not end_of_message:
        packet = f"{sequence_number}:{data[:200]}"  # Include sequence number and a chunk of data
        data = data[200:]  # Remove the sent chunk

        if not data:
            end_of_message = True

        # Send the packet to the server
        client_socket.sendto(packet.encode(), (server_name, server_port))

        attempts = 0
        client_socket.settimeout(1)  # Changed timeout to 1 second for faster testing

        while attempts < 5:
            try:
                # Wait for an acknowledgment (ACK) from the server
                response, server_address = client_socket.recvfrom(1536)
                ack, _ = response.decode().split(':')
                ack = int(ack)

                if ack == sequence_number:
                    print(f"Received ACK for sequence number {ack}")
                    sequence_number += 1  # Increment sequence number
                    break  # Exit the loop upon successful ACK
            except timeout:
                # Handle timeout (e.g., retransmit the packet)
                attempts += 1

        if attempts >= 5:
            print("Connection failed to transmit packet")

if __name__ == "__main__":
    initialize_client()
