import socket


def main():
    # Define server address and port
    server_address = '127.0.0.1'
    server_port = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    try:
        # Connect to the server
        while 1:
            # Send data to the server
            message = input("$ ")
            client_socket.send(message.encode('utf-8'))

            # Receive response from the server
            response = client_socket.recv(1024).decode('utf-8').strip()
            f_response: str = ""
            if len(response.split(";")) > 1:
                f_response = ';'.join(response.split(";")[1:])
            match int(response.split(";")[0]):
                case 300:
                    break
                case 301:
                    print(f"Invalid Command: {message}")
                case 302:
                    print(f"Invalid args in: {message}")
                case 200:
                    print('> ' + f_response)

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    finally:
        # Close the connection
        client_socket.close()


if __name__ == "__main__":
    main()
