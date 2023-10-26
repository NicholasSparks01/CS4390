from socket import *
import sys

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

def initialize_server():
    server_port = 11235
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', server_port))

    print("The server is ready to receive")

    expected_sequence_number = 0
    received_data = ""

    # Receive data using RDT
    while True:
        data, client_address = server_socket.recvfrom(1536)
        received_sequence_number, received_chunk = data.decode().split(':')

        if int(received_sequence_number) == expected_sequence_number and received_chunk in long_msg:
            print(f"Received data with sequence number {received_sequence_number}:\n{received_chunk}")
            expected_sequence_number += 1  # Increment sequence number
            received_data += received_chunk

            # Simulate sending an ACK
            ack_packet = f"{received_sequence_number}:ACK"
            server_socket.sendto(ack_packet.encode(), client_address)

            if not received_chunk:
                break  # End of message

def shutdown_server(sig, frame):
    print("Shutting down the server...")
    sys.exit(0)

if __name__ == "__main__":
    initialize_server()
