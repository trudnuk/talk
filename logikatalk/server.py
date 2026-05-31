import socket
import threading

HOST = "localhost"
PORT = 8080
server_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_con.bind((HOST, PORT))
print("Server is running ... ")
server_con.listen(15)
clients = []

def boardcast(data, exclude_socket=None):
    for c in clients:
        if c != exclude_socket:
            try:
                c.send(data.encode())
            except:
                print("Помилка відправки повідомлення")

def handle_client(client_socket):
    while True:
        try:
            text = client_socket.recv(4096).decode()
            if not text:
                break
            print(text)
            boardcast(f"{text}", exclude_socket=client_socket)
        except:
            client_socket.close()   
            clients.remove(client_socket)  
            boardcast(f"Користувач покинув чат")
            break

while True:
    try:
        con, addr = server_con.accept()
        print(f"{addr}")
        clients.append(con)
        threading.Thread(target=handle_client, args=(con,), daemon=True).start()
    except:
        pass

