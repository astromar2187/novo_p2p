import socket
import threading
import json

# Endereço e porta para o servidor P2P
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

# Dicionário de contatos disponíveis em cada peer
peers_books = {}  
id = 1

# Função para gerenciar mensagens dos peers conectados
def handle_peer_connection(peer_socket, address):
    while True:
        try:
            message = peer_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Mensagem recebida de {address}: {message}")
                process_peer_message(message, peer_socket)
            else:
                break  # Se não houver mensagem, desconecta
        except Exception as e:
            print(f"Peer {address} desconectado. Erro: {e}")
            break

    peer_socket.close()


# Função para processar as mensagens recebidas
def process_peer_message(message, peer_socket):
    global id
    try:
        message = json.loads(message)
        message_type = message["type"]

        if message_type == "register_peer": 
            peer_id = "peer_" + str(id)
            id += 1
            books = message["livros"]
            peers_books[peer_id] = books
            print(f"Peer '{peer_id}' registrado com livros: {books}")
            response = {
                "type": "register_response", 
                "message": f"Peer '{peer_id}' registrado com sucesso!",
                "peer_id": peer_id  # Enviando o peer_id na resposta
            }
            peer_socket.send(json.dumps(response).encode('utf-8'))

        elif message_type == "search_livro":
            book_name = message["livro_name"]
            peer_id = message["peer_id"]
            result = search_book(book_name, peer_id)
            response = {"type": "search_response", "result": result}
            peer_socket.send(json.dumps(response).encode('utf-8'))

        elif message_type == "download_book":
            book_name = message["book_name"]
            peer_id = message["peer_id"]  # ID do peer que está baixando o livro
            result = download_book(book_name, peer_id)  # Passa o peer que está baixando
            peer_socket.send(json.dumps(result).encode('utf-8'))

        elif message_type == "exit":
            peer_id = message["peer_id"]
            if peer_id in peers_books:
                del peers_books[peer_id]  # Remove o peer e seus livros
                print(f"Peer '{peer_id}' desconectado com sucesso!")
                response = {
                    "type": "exit_response",
                    "message": f"Peer '{peer_id}' removido com sucesso!"
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))
            else:
                response = {
                    "type": "exit_response",
                    "message": f"Peer '{peer_id}' já removido!"
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))


        elif message_type == "add_books":
            peer_id = message["peer_id"]
            books = message["livros"]
            peers_books[peer_id].extend(books)
            print(f"Peer '{peer_id}' adicionou livros: {books}")
            response = {
                "type": "adicionar_livros_response",
                "success": True,
                "message": f"Peer '{peer_id}' adicionou livros com sucesso!"
            }
            peer_socket.send(json.dumps(response).encode('utf-8'))


        elif message_type == "mostrar_livros":
            peer_id = message["peer_id"]
            if peer_id in peers_books:
                books = peers_books[peer_id]
                response = {
                    "type": "mostrar_livros_response",
                    "books": books
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))


        else:
            response = {
                "type": "error",
                "message": "Tipo de Mensagem inválida"
            }
            peer_socket.send(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        if peer_socket:
            peer_socket.close()

# Função para processar o download do livro e adicionar ao peer que baixou
def download_book(book_name, pid):
    for peer_id, books in peers_books.items():
        if book_name in books:
            # Se o livro foi encontrado, adicione ao peer que fez o download
            if peer_id == pid:
                return {
                    "type": "download_response",
                    "success": False,
                    "message": f"Livro '{book_name}' já está presente no próprio peer '{pid}'"
                }
            
            else:
                peers_books[pid].append(book_name)
                print(f"Livro '{book_name}' adicionado ao peer '{pid}'")
            
            book_content = f"Conteúdo do livro '{book_name}' do peer '{peer_id}'"
            return {
                "type": "download_response",
                "success": True,
                "message": book_content
            }
        
    return {
        "type": "download_response",
        "success": False,
        "message": f"Livro '{book_name}' não disponível em nenhum peer"
    }


def search_book(book_name, pid):
    for peer_id, books in peers_books.items():
        if book_name in books:
            if peer_id == pid:
                return f"Livro '{book_name}' já está presente no próprio peer '{peer_id}'"
            return f"Livro '{book_name}' encontrado no peer '{peer_id}'"
    return f"Livro '{book_name}' não encontrado em nenhum peer"


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
