import sys
import socket

class FilezillaClient():
    def __init__(self, host_ip, port, username, password):
        self.host_ip = host_ip
        self.port = port
        self.username = username
        self.password = password

        # Connect to the FTP server
        self.ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ftp_socket.connect((self.host_ip, self.port))
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        # Send the login information
        self.ftp_socket.send(f"USER {self.username}\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)
        self.ftp_socket.send(f"PASS {self.password}\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        # Change to the desired directory
        self.ftp_socket.send("CWD /Server/\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)


    def list_files(self):
        self.ftp_socket.send(f"PASV\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        data_port_start = response.find("(") + 1
        data_port_end = response.find(")")
        data_port = response[data_port_start:data_port_end].split(",")
        data_port = int(data_port[-2]) * 256 + int(data_port[-1])
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.host_ip, data_port))

        self.ftp_socket.send("LIST\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        # Receive the directory listing
        data = data_socket.recv(1024)
        while data:
            print(data.decode(), end='')
            data = data_socket.recv(1024)

    def upload_file(self):
        pass

    def download_file(self):
        pass

    def delete_file(self):
        pass

    def rename_file(self):
        pass

    def quit(self):
        pass

if __name__ == '__main__':
    host_ip = input("HOST:")
    port = int(input("PORT:"))
    username = input("USERNAME:")
    password = input("PASSWORD:")

    client = FilezillaClient(host_ip, port, username, password)

    while True:
        command = input("Enter command:")

        if command == "LIST":
            client.list_files()