import sys
import socket
import select

HOST        = ''
CONNECTIONS = []
RECV_BUFFER = 4096
PORT        = 11100

def server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(10)

    # add self to list of readable connections
    CONNECTIONS.append(serverSocket)

    print("server running \nsocket accepting connections on port ", PORT)

    while True:
        # 4th param timeout -> no block, always poll
        readable, writable, exceptional = select.select(CONNECTIONS, [], [], 0 )

        for sock in readable:
            # new connection
            if sock == serverSocket:
                sockfd, addr = serverSocket.accept()
                CONNECTIONS.append(sockfd)
                print("connection from ", addr)
            
            # existing connection
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # broadcast data to clients
                        print(data)
                        broadcast(serverSocket, sock, data)
                    else:
                        if sock in CONNECTIONS:
                            CONNECTIONS.remove(sock)
                        print("connection dropped ", sock)
                        # connection is broken, broadcast?!
                except:
                    # connection is broken, maybe broadcast, continue anyway
                    continue
    
    serverSocket.close()

def broadcast(serverSocket, sock, msg):
    for client in CONNECTIONS:
        if client != serverSocket:
            try:
                client.send(msg)
            except:
                # broken
                client.close()
                if client in CONNECTIONS:
                    CONNECTIONS.remove(client)


if __name__ == "__main__":
    sys.exit(server())