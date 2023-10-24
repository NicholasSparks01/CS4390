from socket import *
import sys
import signal

def get_local_ip_address():
    try:
        # Create a socket object to get the local IP address
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(0.1)

        # Connect to a public IP address (doesn't send any data)
        sock.connect(("8.8.8.8", 80))

        # Get the local IP address from the connected socket
        local_ip_address = sock.getsockname()[0]

        # Close the socket
        sock.close()

        return local_ip_address
    except socket.error:
        print("Could not retrieve local IP address")
        return -1
local_ip = get_local_ip_address()
print("Local IP Address:", local_ip)

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
    'Proxy_Client': local_ip,    # <<<< REPLACE WITH ACTUAL IP ADDRESS if script doesn't work<<<<<
    'MAX_REQUEST_LEN' : 4096,       # Maximum request length
    'CONNECTION_TIMEOUT' : 5       # Number of attempts to connect
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
        
        print("+-+-+-+-+-Received Request RAW+-+-+-+-+-")
        print(request.decode())
        print("+-+-+-+-+-End of Request RAW+-+-+-+-+-")

        # Get Domain name
        first_line = request.split(b'\n')[0]
        url = first_line.split(b' ')[1]

        # Parse the URL and extract hostname  
        if (i == 0):
            hostname = url.decode()[1:]
        print("===================")
        print("Hostname:", hostname)        
        print("===================")

        # if first request, ask for domain request, else ask for files associated with first request
        if (i == 0):
            new_request = request[:4].decode() + "http://" + request[5:].decode()
        else:
            new_request = request[:4].decode() + "http://" + hostname + "/" + request[5:].decode()

        print("+-+-+-+-+-NEW Formatted Request+-+-+-+-+-")
        print(new_request)
        print("+-+-+-+-+-End of NEW Request+-+-+-+-+-")

        new_request = new_request.encode()
 
        # Handle the request to destination server
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(config['CONNECTION_TIMEOUT'])


        try:
            s.connect((hostname, 80))
            print("SENDING REQUEST TO DOMAIN....")
            s.sendall(new_request)

            # Receive the response from the destination server
            response = b""
            while True:
                data = s.recv(4096)
                print("")
                print("")
                print("+-+-+-+-+-RESPONSE FROM DOMAIN+-+-+-+-+-")
                print(data)
                print("+-+-+-+-+-END OF DOMAIN RESPONSE+-+-+-+-+-")
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

