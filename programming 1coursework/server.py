import socket
import threading

HOST = '0.0.0.0'
PORT = 8080
LISTENER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)
        except Exception as e:
            print(f"Error while receiving message from {username}: {e}")
            break

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = f'SERVER~{username} added to the chat'
            send_messages_to_all(prompt_message)
            break

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f'Running the server on {HOST} {PORT}')
    except:
        print(f'Unable to bind to host {HOST} and port {PORT}')

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]} {address[1]}')

        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
