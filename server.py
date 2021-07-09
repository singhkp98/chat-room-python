import socket
import threading

#real scenario (server online): HOST = private IP address (ipconfig, ifconfig)
HOST = '127.0.0.1'
#reak scenario (server online): Open ports on server side
PORT = 9090

#socket di tipo internet (AF_INET) e TCP socket (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind tuple HOST and PORT
server.bind((HOST, PORT))

server.listen()

#lista vuota di clients e nickanmes
clients = []
nicknames = []

#broadcast function (manda un messaggio a tutti i client connessi)
def broadcast(message):
    for client in clients:
        client.send(message)


#handle function (gestisce le connessioni dei clients una volta che si sono connessi al server)
def handle(client):
    while True:
        try:
            #prendo il messaggio del client con la funzione .recv() N.B non la receive()
            message = client.recv(1024)

            #controllo in quale index si trova il client passato per parametro
            #in modo da poter estrarre il suo nickname
            print(f"{nicknames[clients.index((client))]} says {message}")

            #broadcasto il messaggio a tutti i client connessi al server
            broadcast(message)
        except:
            #gestico l'eccezione rimuovendo il client e il suo nickname dalla lista dei clients
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index];
            nicknames.remove(nickname);
            break

#receive function (resta in attesa e accetta connessioni da parte dei clients)
def receive():
    while True:
        #creo il mio client. NB: accept() ritorna un client e un address
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024);
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")

        #faccio un broadcast a tutti i clients
        broadcast(f"{nickname} connected to the server! \n".encode('utf-8'))

        #invio il messaggio al client per dirgli che è connesso
        client.send("Connected to the server".encode('utf-8'))

        #la funzione target del thread è: Handle. Passo inoltre il parametro client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
receive()