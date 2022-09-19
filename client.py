import socket as soc

if __name__ == "__main__":
    socketClient = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    host = '127.0.0.1'
    port = 4444
    end_point = (host, port)
    socketClient.connect(end_point)
    while(True):
        data = socketClient.recv(1024).decode()
        print(data)
