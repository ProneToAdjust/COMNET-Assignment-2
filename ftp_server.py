import socket
import os
from threading import Thread

def server_thread(client_socket):
    # Send a welcome message to the client
    client_socket.send(b'220 Welcome to the FTP server\r\n')

    # Wait for the client to send a command
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Parse the command and arguments
        command = data.strip().decode().split(' ')[0].upper()
        args = ' '.join(data.strip().decode().split(' ')[1:])

        # Handle the command
        if command == 'QUIT':
            client_socket.send(b'221 Goodbye\r\n')
            client_socket.close()
            break

        elif command == 'USER':
            if args == 'anonymous' or args == '':
                client_socket.send(b'331 Password required\r\n')
            else:
                client_socket.send(b'530 Login incorrect\r\n')

        elif command == 'PASS':
            client_socket.send(b'230 Login successful\r\n')
            # client_socket.send(b'200 Switching to Binary mode\r\n')

        elif command == 'PWD':
            client_socket.send(f'257 {os.getcwd()}\r\n'.encode())

        elif command == 'CWD':
            try:
                os.chdir(args)
                client_socket.send(f'250 Directory changed to {os.getcwd()}\r\n'.encode())
            except:
                client_socket.send(b'550 Failed to change directory\r\n')

        elif command == 'TYPE':
            if args == 'I':
                client_socket.send(b'200 Type set to I\r\n')
            elif args == 'A':
                client_socket.send(b'200 Type set to A\r\n')

        elif command == 'PASV':
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind((HOST, 0))
            data_socket.listen(1)
            data_port = data_socket.getsockname()[1]
            data_ip = socket.gethostbyname(socket.gethostname())
            data_address = (data_ip, data_port)
            client_socket.send(f'227 Entering Passive Mode ({",".join(data_ip.split("."))},{data_port//256},{data_port%256})\r\n'.encode())
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind(data_address)
            data_socket.listen(1) 

        elif command == 'LIST':
            try:
                file_list = os.listdir()
                file_str = '\r\n'.join(file_list) + '\r\n'
                client_socket.send(f'150 Opening data connection for LIST\r\n'.encode())

                # Wait for the client to connect to the data port
                data_client_socket, data_client_address = data_socket.accept()

                # Send the file list
                data_client_socket.send(file_str.encode())
                data_client_socket.close()
                data_socket.close()

                client_socket.send(b'226 Transfer complete\r\n')
            except:
                client_socket.send(b'550 Failed to get file list\r\n')

        elif command == 'MKD':
            try:
                os.mkdir(args)
                client_socket.send(f"257 \"{args}\" created\n".encode())
            except:
                client_socket.send(b"550 Failed to create directory\n")

        elif command == 'UPLD' or command == 'STOR':
            data_client_socket, data_client_address = data_socket.accept()

            uploaded_file = open(args, 'wb')
            file_bytes = b''

            incoming_data = data_client_socket.recv(1024)
            while incoming_data:
                file_bytes += incoming_data
                incoming_data = data_client_socket.recv(1024)

            uploaded_file.write(file_bytes)
            uploaded_file.close()
            data_socket.close()

            client_socket.send(b'226 Transfer complete\r\n')

        # Download file
        elif command == 'DWLD':
            client_socket.send(b'502 Command not implemented\r\n')
            
        # Delete file     
        elif command == 'DELF':
            client_socket.send(b'502 Command not implemented\r\n')
            
        # Rename file
        elif command == 'RNTO':
            client_socket.send(b'502 Command not implemented\r\n')

        else:
            client_socket.send(b'502 Command not implemented\r\n')

# Define the server's host and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1006

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print(f'Server listening on {HOST}:{PORT}')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    print(f'Client connected from {client_address}')

    thread = Thread(target= server_thread, args= (client_socket, ))
    thread.start()