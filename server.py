import socket
import threading
import json

# Endereço e porta para o servidor P2P
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

# Dicionário de contatos disponíveis em cada peer
peers_books = {}  # da forma {peer_id: [books]}
id = 1

# Função para gerenciar mensagens dos peers conectados
def handle_peer_connection(peer_socket, address):
    while True:
        try:
            message = peer_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Mensagem recebida de {address}: {message}")
                process_peer_message(message, peer_socket)
        except Exception as e:
            print(f"Peer {address} desconectado. Erro: {e}")
            peer_socket.close()
            break

# Função para processar as mensagens recebidas
def process_peer_message(message, peer_socket):
    global id
    try:
        message = json.loads(message)
        message_type = message["type"]

# Dentro da função process_peer_message, logo após processar a mensagem
        if message_type == "register_peer":
            try:
                peer_id = "peer_" + str(id)
                id += 1

                books = message["books"]
                peers_books[peer_id] = books

                print(f"Peer '{peer_id}' registrado com livros: {books}")
                response = {
                    "type": "register_response",
                    "peer_id": peer_id,
                    "message": f"Peer '{peer_id}' registrado com sucesso!"
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"Erro ao registrar peer: {e}")
                response = {
                    "type": "register_response",
                    "message": "Erro ao registrar o peer."
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))


        elif message_type == "search_book":
            book_name = message["book_name"]
            result = search_book(book_name)
            response = {"type": "search_response", "result": result}
            peer_socket.send(json.dumps(response).encode('utf-8'))

        elif message_type == "exit":
            peer_id = message["peer_id"]
            if peer_id in peers_books:
                del peers_books[peer_id]
                print(f"Peer '{peer_id}' desconectado com sucesso!")
                response = {
                    "type": "remove_response",
                    "message": f"Peer '{peer_id}' removido com sucesso!"
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        if peer_socket:
            peer_socket.close()

# Função para buscar um livro em todos os peers
def search_book(book_name):
    for peer_id, books in peers_books.items():
        if book_name in books:
            return f"Livro '{book_name}' encontrado no peer '{peer_id}'"
    return f"Livro '{book_name}' não encontrado"

# Função principal para iniciar o servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}")

    while True:
        peer_socket, address = server_socket.accept()
        print(f"Nova conexão de {address}")
        thread = threading.Thread(target=handle_peer_connection, args=(peer_socket, address))
        thread.start()

# Iniciar o servidor
start_server()
