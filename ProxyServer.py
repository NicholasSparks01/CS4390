from socket import *
import sys
import signal

def initialize_server(config):
    # Create server socket, bind to port, and listen
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    # Re-use the socket
    tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Bind socket to public local host and port
    tcpSerSock.bind((config['Proxy_Client'], 8787))

    tcpSerSock.listen(1)  # Limit to one connection at a time

    # Shutdown on Ctrl+C
    def shutdown_server(sig, frame):
        print("Shutting down the server...")
        tcpSerSock.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_server)

    return tcpSerSock

if len(sys.argv) > 1:
    print("Usage: python3 ProxyServer.py")
    sys.exit(2)

# Initialize the server
config = {'Proxy_Client': '127.0.0.1'}  # Replace with your actual IP
tcpSerSock = initialize_server(config)

while True:
    # Accept a connection (blocking operation)
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from: ", addr)
    
    # Handle the request from the connected client here
    
    # Close the connection when you're done
    tcpCliSock.close()
