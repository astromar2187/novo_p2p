# server.py
import socket
import threading
import json

# Endereço e porta para o servidor P2P
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

# Dicionário de contatos disponíveis em cada peer
peers_books = {} # da forma {peer_id: [books]}

# Função para gerenciar mensagens dos peers conectados
def handle_peer_connection(peer_socket, address): #serve para receber mensagens de um peer, processar e responder
    while True: #enquanto estiver ativo
        try: #tenta receber a mensagem
            message = peer_socket.recv(1024).decode('utf-8') #recebe a mensagem
            if message: #se a mensagem for recebida
                print(f"Mensagem recebida de {address}: {message}") #mostra a mensagem recebida, de qual peer e o endereço
                process_peer_message(message, peer_socket) #processa a mensagem
        except Exception as e: #se der erro
            print(f"Peer {address} desconectado. Erro: {e}") #mostra que o peer foi desconectado
            peer_socket.close() #fecha o socket do peer
            break   #para o loop se o peer foi desconectado

# Função para processar as mensagens recebidas
def process_peer_message(message, peer_socket): #serve para processar a mensagem recebida
    try: #tenta processar a mensagem
        message = json.loads(message) #carrega a mensagem em json
        message_type = message["type"] #pega o tipo da mensagem, que pode ser register_peer ou search_contact
        peer_id = message["peer_id"] #pega o id do peer

        if message_type == "register_peer": #se o tipo da mensagem for register_peer
            books = message["books"] #pega os contatos do peer
            peers_books[peer_id] = books #adiciona o peer_id e os contatos no dicionário
            print(f"Peer '{peer_id}' registrado com livros: {books}") #mostra que o peer e os contatos foram registrados com sucesso
            # Envia resposta de confirmação ao cliente
            response = {"type": "register_response", "message": f"Peer '{peer_id}' registrado com sucesso!"} #cria a resposta, que é um json com o tipo e a mensagem de confirmação
            peer_socket.send(json.dumps(response).encode('utf-8')) #envia a resposta ao peer

        elif message_type == "search_book": #se o tipo da mensagem for search_book
            book_name = message["book_name"] #pega o nome do livro a ser buscado
            result = search_book(contact_name) #chama a função search_book para buscar o contato
            response = {"type": "search_response", "result": result} #cria a resposta, que é um json com o tipo e o resultado da busca
            peer_socket.send(json.dumps(response).encode('utf-8')) #envia a resposta ao peer

        elif message_type == "remove_peer": #se o tipo da mensagem for remove_peer
            if peer_id in peers_contacts: #se o peer_id estiver nos contatos
                del peers_contacts[peer_id] #remove o peer_id dos contatos
                print(f"Peer '{peer_id}' removido com sucesso!") #mostra que o peer foi removido com sucesso
                response = {"type": "remove_response", "message": f"Peer '{peer_id}' removido com sucesso!"} #cria a resposta, que é um json com o tipo e a mensagem de remoção
            else:
                print(f"Peer '{peer_id}' não encontrado.") #mostra que o peer não foi encontrado
                response = {"type": "remove_response", "message": f"Peer '{peer_id}' não encontrado."} #cria a resposta, que é um json com o tipo e a mensagem de não encontrado
            peer_socket.send(json.dumps(response).encode('utf-8')) #envia a resposta ao peer

    except Exception as e: #se der erro
        print(f"Erro ao processar mensagem: {e}") #mostra o erro

# Função para buscar um livro em todos os peers
def search_book(book_name): 
    for peer_id, books in peers_books.items(): #para cada peer e seus livros
        if book_name in books: #se o livro estiver nos livros do peer
            return f"Livro '{book_name}' encontrado no peer '{peer_id}'" #retorna que o contato foi encontrado e em qual peer (o primeiro que encontrar)
    return f"Livro '{book_name}' nao encontrado" #se não encontrar o contato, retorna que não foi encontrado

# Função principal para iniciar o servidor
def start_server(): #serve para iniciar o servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket do servidor
    server_socket.bind((SERVER_IP, SERVER_PORT)) #liga o socket ao endereço e porta do servidor
    server_socket.listen(5) #escuta até 5 conexões
    print(f"Servidor iniciado em {SERVER_IP}:{SERVER_PORT}") #mostra que o servidor foi iniciado

    while True: #enquanto estiver ativo
        peer_socket, address = server_socket.accept() #aceita a conexão do peer
        print(f"Nova conexão de {address}") #mostra que uma nova conexão foi feita
        thread = threading.Thread(target=handle_peer_connection, args=(peer_socket, address)) #cria uma thread para lidar com a conexão do peer
        thread.start() #inicia a thread

# Iniciar o servidor
start_server()
