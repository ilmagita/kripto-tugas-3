import threading
import socket
from config import host, port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()     # server is now on listening method

clients = []
nicknames = []

# broadcast method
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('ascii'))
        except Exception as e:
            print('There was an error in broadcasting a message.')
            print(e)

# handle method
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message.decode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat.')
            nicknames.remove(nickname)
            break

# receive method
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        if client:
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}')
            broadcast(f'{nickname} joined the chat.'.encode('ascii'))
            client.send('You have connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            print('Failed to accept connection.')

print("Server is listening...")
receive()