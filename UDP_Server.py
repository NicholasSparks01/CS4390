from socket import *
import sys

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

        if int(received_sequence_number) == expected_sequence_number:
            print(f"Received data with sequence number {received_sequence_number}: {received_chunk}")
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
