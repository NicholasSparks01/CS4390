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

    tcpSerSock.listen(10)  # Limit to one connection at a time

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
config = {
    'Proxy_Client': '192.168.68.68',    # Replace with your actual IP if needed
    'MAX_REQUEST_LEN' : 4096,       # Maximum request length
    'CONNECTION_TIMEOUT' : 30        # Number of attempts to connect
    }  
tcpSerSock = initialize_server(config)
i = 0
while True:
    # Accept a connection (blocking operation)
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from: ", addr)
    
    # Handle the request from the connected client here
    try: 
        # get the request from browser
        request = tcpCliSock.recv(config['MAX_REQUEST_LEN']) #set max request length to 4096

        if not request:
            continue

        print("Received Request:", request.decode())

        # Get Domain name
        first_line = request.split(b'\n')[0]
        url = first_line.split(b' ')[1]

        # Parse the URL and extract hostname  
        if (i == 0):
            hostname = url.decode()[1:]
        print("Hostname:", hostname)        
        
        # Parsing
        if (i == 0):
            new_request = request[:4].decode() + "http://" + request[5:].decode()
        else:
            new_request = request[:4].decode() + "http://" + hostname + "/" + request[5:].decode()

        print("NEW:", new_request)
        new_request = new_request.encode()

            
        # Handle the request to destination server
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(config['CONNECTION_TIMEOUT'])


        try:
            s.connect((hostname, 80))
            print("SENDING REQUEST")
            s.sendall(new_request)

            # Receive the response from the destination server
            response = b""
            while True:
                data = s.recv(4096)
                print("")
                print("")
                print(data)
                # Continue until data is empty
                if (len(data) > 0):
                    tcpCliSock.send(data)
                    print(data)
                else:
                    break
                
        except OSError as e:
            print("Socket error:", e)

        finally:
            # Close the client socket
            tcpCliSock.close()

             # Close the server socket to the destination server
            s.close()

    except OSError as e:
        print("Socket error:", e)
    i = i + 1

