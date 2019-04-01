#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

## menerima koneksi
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept() ## mengambil host dan port
        print("%s:%s has connected." % client_address) ## konfirmasi
        client.send(bytes("Selamat Datang!" + "Tuliskan Nama Anda!", "utf8"))## kirim ke client 
        addresses[client] = client_address ## addrsses client diperoleh dari variable client_address
        Thread(target=handle_client, args=(client,)).start() ## Masuk ke fungsi handlle client


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8") ## Menangkap nama dari client.sent()
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name 
    client.send(bytes(welcome, "utf8")) 
    msg = "%s has joined the chat!" % name ## konfirmasi ke client lain bahwa ada client masuk
    broadcast(bytes(msg, "utf8")) 
    clients[client] = name ## Memasukan client ke dalam array client

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"): 
            broadcast(msg, name+": ") ## Inisiasi untuk menuliskan chat
        else:
            client.send(bytes("{quit}", "utf8")) ## definisi untuk keluar chat
            client.close()
            del clients[client] ## Menghapus client dari array clients
            broadcast(bytes("%s has left the chat." % name, "utf8")) # konfirmasi bahwa orang tersebut sudah keluar
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients: ## kirim pesan ke semua client aktif
        sock.send(bytes(prefix, "utf8")+msg)

   
clients = {}
addresses = {}

# HOST = "1.1.1.1"
# PORT = 9999
BUFSIZ = 1024
# ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(("127.0.0.1", 9999))

if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
