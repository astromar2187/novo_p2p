import socket
import threading
import json
import time

class tacker:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.porta = 5000
        self.peers_books = {} # Dicionário para armazenar os ips e os livros de cada peer. Exemplo: {"peer_1": (ip, ["livro1", "livro2"]), "peer_2": (ip, ["livro3", "livro4"])}
        self.id = 1

    def get_peer_books(self):
        print("\n")
        print("Lista de peers atualizada em", time.ctime())
        print("______________________________________________________________")
        for peer_id, books in self.peers_books.items():
            print(f"Peer ID: {peer_id}, IP: {books[0]}, Livros: {books[1]}")
            print("\n")
        print("\n")

    '''Função para gerenciar mensagens dos peers conectados'''
    def handle_peer_connection(self, peer_socket, address):
        while True:
            try:
                message = peer_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Mensagem recebida de {address}: {message}")
                    self.process_peer_message(message, peer_socket, address)
                else:
                    break  # Se não houver mensagem, desconecta
            except Exception as e:
                print(f"Peer {address} desconectado. Erro: {e}")
                break

        peer_socket.close()


    '''Função para processar as mensagens recebidas'''
    def process_peer_message(self, message, peer_socket, address):
        try:
            message = json.loads(message)
            message_type = message["type"]
            peer_ip = address[0]
            peer_id = message["peer_id"] if "peer_id" in message else None

            if message_type == "register_peer": 
                peer_id = "peer_" + str(self.id)
                self.id += 1
                books = message["livros"]
                self.peers_books[peer_id] = (peer_ip, books)
                print(f"Peer '{peer_id}' registrado com livros: {books}. IP: {peer_ip}")
                response = {
                    "type": "register_response", 
                    "message": f"Peer '{peer_id}' registrado com sucesso!",
                    "peer_id": peer_id  # Enviando o peer_id na resposta
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))
                self.get_peer_books()

            elif message_type == "get_peer_info":
                if peer_id in self.peers_books:
                    books = self.peers_books[peer_id]
                    response = {
                        "type": "get_peer_info_response",
                        "success": True,
                        "message": f"Informações do Peer '{peer_id}': IP: {books[0]}, Livros: {books[1]}"
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                else:
                    response = {
                        "type": "get_peer_info_response",
                        "success": False,
                        "message": f"Peer '{peer_id}' não encontrado"
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "refresh_books":
                #peer_id = message["peer_id"]
                books = message["livros"]
                self.peers_books[peer_id] = (peer_ip, books)
                print(f"Peer '{peer_id}' atualizou seus livros: {books}")
                response = {
                    "type": "refresh_books_response",
                    "success": True,
                    "message": f"Peer '{peer_id}' atualizou seus livros com sucesso!"
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))
                self.get_peer_books()

            elif message_type == "search_livro":
                book_name = message["livro_name"]
                #peer_id = message["peer_id"]
                result = self.search_book(book_name, peer_id)
                response = {"type": "search_response", "result": result}
                peer_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "download_book":
                book_name = message["book_name"]
                peer_id = message["peer_id"]  # ID do peer que está baixando o livro
                result = self.download_book(book_name, peer_id)  # Passa o peer que está baixando
                peer_socket.send(json.dumps(result).encode('utf-8'))
                self.get_peer_books()

            elif message_type == "unregister_peer":
                if peer_id in self.peers_books:
                    del self.peers_books[peer_id]  # Remove o peer e seus livros
                    print(f"Peer '{peer_id}' desconectado com sucesso!")
                    response = {
                        "type": "unregister_response",
                        "message": f"Peer '{peer_id}' removido com sucesso!"
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                else:
                    response = {
                        "type": "unregister_response",
                        "message": f"Peer '{peer_id}' não encontrado"
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                self.get_peer_books()
                
            elif message_type == "mostrar_livros": #Não precisa perguntar isso ao servidor, pois a main pode fazer isso
                if peer_id in self.peers_books:
                    books = self.peers_books[peer_id]
                    response = {
                        "type": "mostrar_livros_response",
                        "books": books
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "test_connection":
                '''response = {
                    "type": "test_response",
                    "message": "Conexão com o Tracker estabelecida com sucesso!",
                    "peer_id": peer_id,
                    "peer_ip": self.peers_books[peer_id][0], # comprovando que o ip registrado é o mesmo
                    "books": self.peers_books[peer_id][1] # comprovando que os livros registrados são os mesmos
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))'''

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

    '''Função para processar o download do livro e adicionar ao peer que baixou'''
    def download_book(self, book_name, pid):
        for peer_id, books in self.peers_books.items():
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


    def search_book(self, book_name, pid):
        for peer_id, books in self.peers_books.items():
            if book_name in books:
                if peer_id == pid:
                    return f"Livro '{book_name}' já está presente no próprio peer '{peer_id}'"
                return f"Livro '{book_name}' encontrado no peer '{peer_id}'"
        return f"Livro '{book_name}' não encontrado em nenhum peer"


    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.porta))
        server_socket.listen(5)
        print(f"Servidor iniciado em {self.ip}:{self.porta}")

        while True:
            peer_socket, address = server_socket.accept()
            print(f"Nova conexão de {address}")
            thread = threading.Thread(target=self.handle_peer_connection, args=(peer_socket, address))
            thread.start()

# Iniciar o servidor
servidor = tacker()
servidor.start_server()
