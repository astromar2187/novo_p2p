import socket
import threading
import json
import time

class Tracker:
    def __init__(self):
        self.ip = "192.168.15.53"
        self.port = 5000
        self.peers_active = {}  # {peer_id: (ip, activeness)}
        self.peers_books = {}  # {peer_id: (ip, [books])}
        self.id_counter = 1
        self.check_interval = 10 # 3 minutos
        self.check_attempts = 3

    
    def get_peer_books(self):
        print("\nLista de peers atualizada em", time.ctime())
        print("______________________________________________________________")
        for peer_id, (peer_ip, books) in self.peers_books.items():
            print(f"Peer ID: {peer_id}, IP: {peer_ip}, Livros: {books}")
            print("\n")

    def is_peer_active(self, peer_ip):
        active = False  # Inicialmente, o peer é considerado inativo
        for attempt in range(self.check_attempts):
            try:
                print(f"Verificando conectividade com {peer_ip}... Tentativa {attempt + 1}")
                with socket.create_connection((peer_ip, 5010), timeout=5):
                    active = True  # Se a conexão for bem-sucedida em qualquer uma das tentativas, o peer é considerado ativo
                    print(f"Peer {peer_ip} está ativo.")
                    break
            except (socket.timeout, ConnectionRefusedError, OSError):
                continue
        return active  # Retorna True se o peer estiver ativo, False caso contrário

    def check_peers_connectivity(self):
        while True:
            time.sleep(self.check_interval)  # Esperar 3 minutos
            print("\nVerificando conectividade dos peers...")
            for peer_id in list(self.peers_books.keys()):
                peer_ip, books = self.peers_books[peer_id]  # {peer_id: (ip, [books])}
                if not self.is_peer_active(peer_ip):  # Se o peer não estiver ativo
                    print(f"Peer {peer_id} ({peer_ip}) não respondeu. Removendo...")
                    self.peers_active[peer_id] = False  # Marcar o peer como inativo
                    del self.peers_books[peer_id]  # Remover o peer da lista de peers

            print("Verificação de conectividade concluída.")
            self.get_peer_books()  # Atualizar a lista de peers

    def handle_peer_connection(self, peer_socket, address):
        while True:
            try:
                message = peer_socket.recv(1024).decode('utf-8')
                if message:
                    self.process_peer_message(message, peer_socket, address)
                else:
                    break
            except Exception as e:
                print(f"Peer {address} desconectado. Erro: {e}")
                break

        peer_socket.close()

    def process_peer_message(self, message, peer_socket, address):
        try:
            message = json.loads(message)
            message_type = message["type"]
            peer_ip = address[0]
            peer_id = message.get("peer_id", None)

            if message_type == "register_peer":
                peer_id = f"peer_{self.id_counter}"
                self.id_counter += 1
                books = message["books"]
                self.peers_books[peer_id] = (peer_ip, books)
                print(f"Peer '{peer_id}' registrado com livros: {books}. IP: {peer_ip}")
                response = {
                    "type": "register_response",
                    "message": f"Peer '{peer_id}' registrado com sucesso!",
                    "peer_id": peer_id
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))
                self.get_peer_books()

            elif message_type == "get_peer_info":
                if peer_id and peer_id in self.peers_books:
                    peer_info = self.peers_books[peer_id] # {peer_id: (ip, [books])} / peer_info = (ip, [books])
                    response = {
                        "type": "get_peer_info_response",
                        "info": peer_info
                    }
                else:
                    response = {
                        "type": "error",
                        "message": "Peer ID não encontrado."
                    }
                peer_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "unregister_peer":
                if peer_id in self.peers_books:
                    del self.peers_books[peer_id]
                    print(f"Peer '{peer_id}' desconectado com sucesso!")
                self.get_peer_books()


            elif message_type == "getIp_pelo_livro":
                book_name = message["book_name"]
                peer_with_book = None

                # Procurar o peer que tem o livro
                print(f"[Socket]Procurando livro '{book_name}'...")
                for peer_id, (peer_ip, books) in self.peers_books.items():
                    if book_name in books:
                        peer_with_book = (peer_id, peer_ip)
                        print(f"[Socket]Livro '{book_name}' encontrado no peer '{peer_id}'")
                        break

                if peer_with_book:
                    response = {
                        "type": "getIp_pelo_livro_response",
                        "peer_ip": peer_with_book[1]
                    }
                else:
                    response = {
                        "type": "error",
                        "message": f"Livro '{book_name}' não encontrado."
                    }

                peer_socket.send(json.dumps(response).encode('utf-8'))


            elif message_type == "update_books":
                books = message["books"]
                if peer_id in self.peers_books:
                    self.peers_books[peer_id] = (peer_ip, books)
                    print(f"Livros do Peer '{peer_id}' atualizados: {books}")
                    response = {
                        "type": "update_books_response",
                        "message": "Lista de livros atualizada no tracker."
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))
                    self.get_peer_books()
                else:
                    response = {
                        "type": "error",
                        "message": "Peer ID não encontrado para atualização."
                    }
                    peer_socket.send(json.dumps(response).encode('utf-8'))

            elif message_type == "get_list_books":
                books = []
                for peer_id, (peer_ip, peer_books) in self.peers_books.items():
                    books.extend(peer_books)
                response = {
                    "type": "get_list_books_response",
                    "books": books
                }
                peer_socket.send(json.dumps(response).encode('utf-8'))


        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            if peer_socket:
                peer_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)
        print(f"Servidor iniciado em {self.ip}:{self.port}")

        # Iniciar thread para verificar a conectividade dos peers
        '''self.check_thread = threading.Thread(target=self.check_peers_connectivity)
        self.check_thread.daemon = True
        self.check_thread.start()'''

        while True:
            peer_socket, address = server_socket.accept()
            print(f"Nova conexão de {address}")
            thread = threading.Thread(target=self.handle_peer_connection, args=(peer_socket, address))
            thread.start()

# Iniciar o servidor
tracker = Tracker()
tracker.start_server()
