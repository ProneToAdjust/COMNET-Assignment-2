import sys
import socket

class FtpClient():

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

    def list_files(self):
        self.ftp_socket.send(f"PASV\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        data_port_start = response.find("(") + 1
        data_port_end = response.find(")")
        data_port = response[data_port_start:data_port_end].split(",")
        data_ip = f'{data_port[0]}.{data_port[1]}.{data_port[2]}.{data_port[3]}'
        print(data_ip)
        data_port = int(data_port[-2]) * 256 + int(data_port[-1])
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((data_ip, data_port))

        self.ftp_socket.send("LIST\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        # Receive the directory listing
        data = data_socket.recv(1024)
        while data:
            print(data.decode(), end='')
            data = data_socket.recv(1024)
        
        data_socket.close()

        response = self.ftp_socket.recv(1024).decode()
        print(response)

    def upload_file(self, file_name):
        self.ftp_socket.send(f"PASV\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        data_port_start = response.find("(") + 1
        data_port_end = response.find(")")
        data_port = response[data_port_start:data_port_end].split(",")
        data_ip = f'{data_port[0]}.{data_port[1]}.{data_port[2]}.{data_port[3]}'
        data_port = int(data_port[-2]) * 256 + int(data_port[-1])
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((data_ip, data_port))

        self.ftp_socket.send(f"UPLD {file_name}\r\n".encode())
        file_to_upload = open(file_name, 'rb')

        data = file_to_upload.read(1024)
        while data:
            data_socket.send(data)
            data = file_to_upload.read(1024)

        file_to_upload.close()
        data_socket.close()

        response = self.ftp_socket.recv(1024).decode()
        print(response)

    def download_file(self, file_name):
        self.ftp_socket.send(f"PASV\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        data_port_start = response.find("(") + 1
        data_port_end = response.find(")")
        data_port = response[data_port_start:data_port_end].split(",")
        data_ip = f'{data_port[0]}.{data_port[1]}.{data_port[2]}.{data_port[3]}'
        data_port = int(data_port[-2]) * 256 + int(data_port[-1])
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((data_ip, data_port))

        self.ftp_socket.send(f"DWLD {file_name}\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)

        file_to_download= open(file_name, 'wb')
        file_bytes = b''

        data = data_socket.recv(1024)
        while data:
            print(data)
            file_bytes += data
            data = data_socket.recv(1024)
            print("LOOPING")
        print(file_bytes)
        file_to_download.write(file_bytes)

        file_to_download.close()
        data_socket.close()

        response = self.ftp_socket.recv(1024).decode()
        print(response)

    def delete_file(self, file_name):
        self.ftp_socket.send(f"PASV\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        #print(response)
        self.ftp_socket.send(f"DELE {file_name}\r\n".encode())
        response = self.ftp_socket.recv(1024).decode()
        print(response)


    def rename_file(self):
        pass

    def quit(self):
        self.ftp_socket.send(b"QUIT\r\n")
        response = self.ftp_socket.recv(1024).decode()
        print(response)

if __name__ == '__main__':
    while True:
        host_ip = input("HOST:")
        port = int(input("PORT:"))
        username = input("USERNAME:")
        password = input("PASSWORD:")

        client = FtpClient(host_ip, port, username, password)

        while True:
            input_command = input("Enter command:")
            input_command = input_command.split(' ')

            command = input_command[0]

            if len(input_command) > 1:
                arg = input_command[1]

            if command == "LIST":
                client.list_files()
            elif command == "QUIT":
                client.quit()
                break
            elif command == "DELF":
                client.delete_file(arg)
            elif command == 'UPLD':
                client.upload_file(arg)
            elif command == 'DWLD':
                client.download_file(arg)
