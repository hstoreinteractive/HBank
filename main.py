import socket, threading


# CODES TABLE
#  200 - OK
#  300 - Client Quit
#  301 - Invalid Command
#  302 - Invalid Args

def send_response(response: str, code: int, c: socket.socket, address: tuple):
    payload: str = str(code) + ";" + response
    print(f"[{address[0]}] <- [127.0.0.1]: {payload}")
    c.send(payload.encode('utf-8'))


def handle_client(address: tuple, client_socket: socket.socket):
    t = threading.Thread(target=async_handle_client, args=(address, client_socket))
    t.start()


def async_handle_client(address: tuple, client_socket: socket.socket):
    while True:
        try:
            # Receive data from the client
            received_data = client_socket.recv(1024).decode('utf-8').strip()

            print(f"[{address[0]}] -> [127.0.0.1]: {received_data}")

            args: list = received_data.split(" ")

            match args[0]:
                case "info":
                    send_response("HBank Systems v1.0 by TheHSI", 200, client_socket, address)
                case "quit":
                    send_response("", 300, client_socket, address)
                    client_socket.close()
                    break
                case "echo":
                    if len(args) > 1:
                        send_response(' '.join(args[1:]), 200, client_socket, address)
                    else:
                        send_response("", 302, client_socket, address)
                case _:
                    send_response("", 302, client_socket, address)

        except ConnectionAbortedError as _:
            break


def main():
    # Define host and port
    host = '127.0.0.1'
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    while True:
        server_socket.listen(5)
        print("Socket server listening on port", port)
        client_socket, address = server_socket.accept()
        handle_client(address, client_socket)


if __name__ == "__main__":
    main()
