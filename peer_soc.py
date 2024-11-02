import socket
import json
import threading
import os
class PeerClient:
    def __init__(self, tracker_ip, tracker_port, books, host='0.0.0.0', port=5001):
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port
        self.books = books
        self.peer_id = None
        self.host = host  # Adiciona o host do peer
        self.port = port  # Adiciona a porta do peer

    def register_peer(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.tracker_ip, self.tracker_port))
        message = {
            "type": "register_peer",
            "books": self.books
        }
        soc.send(json.dumps(message).encode('utf-8'))
        response = soc.recv(1024).decode('utf-8')
        response = json.loads(response)
        self.peer_id = response.get("peer_id")
        print(response["message"])
        soc.close()

    def get_peer_info(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.tracker_ip, self.tracker_port))
        message = {
            "type": "get_peer_info",
            "peer_id": self.peer_id
        }
        soc.send(json.dumps(message).encode('utf-8'))
        response = soc.recv(1024).decode('utf-8')
        response = json.loads(response)
        for peer_id, (peer_ip, books) in response["peers_books"].items():
            print(f"Peer ID: {peer_id}, IP: {peer_ip}, Livros: {books}")
        soc.close()

    def unregister_peer(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.tracker_ip, self.tracker_port))
        message = {
            "type": "unregister_peer",
            "peer_id": self.peer_id
        }
        soc.send(json.dumps(message).encode('utf-8'))
        soc.close()

    def download_book(self, book_name):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((self.tracker_ip, self.tracker_port))

            # Solicitar o IP do peer que possui o livro
            message = {
                "type": "getIp_pelo_livro",
                "peer_id": self.peer_id,
                "book_name": book_name
            }

            soc.send(json.dumps(message).encode('utf-8'))
            response = soc.recv(1024).decode('utf-8')

            if not response:
                print("Erro: resposta vazia do servidor tracker.")
                return
            response = json.loads(response)

            if response["type"] == "getIp_pelo_livro_response":
                ip = response["peer_ip"]

                # Conectar ao peer que possui o arquivo
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect((ip, 5001))  # Supondo que o peer ouça na porta 5001

                # Enviar solicitação para download do arquivo
                request = {
                    "type": "download_request",
                    "book_name": book_name
                }
                peer_socket.send(json.dumps(request).encode('utf-8'))

                # Receber o conteúdo do livro e salvar localmente
                with open(book_name, 'wb') as f:
                    while True:
                        data = peer_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"Livro '{book_name}' baixado com sucesso!")
                peer_socket.close()

                # Adicionar o livro baixado à lista de livros locais
                self.books.append(book_name)
                print(f"O livro '{book_name}' foi adicionado à sua lista de livros.")

                # Notificar o tracker sobre a atualização da lista de livros
                self.update_tracker_books()

            else:
                print(response["message"])

            soc.close()

        except json.JSONDecodeError:
            print("Erro: resposta inválida recebida, não é JSON.")
        except Exception as e:
            print(f"Erro ao tentar baixar o livro: {e}")

    def update_tracker_books(self):
        """Atualiza o tracker com a lista atualizada de livros do peer."""
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((self.tracker_ip, self.tracker_port))
            message = {
                "type": "update_books",
                "peer_id": self.peer_id,
                "books": self.books
            }
            soc.send(json.dumps(message).encode('utf-8'))
            response = soc.recv(1024).decode('utf-8')
            response = json.loads(response)
            if response["type"] == "update_books_response":
                print(response["message"])
            soc.close()
        except Exception as e:
            print(f"Erro ao atualizar o tracker: {e}")



    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            request = json.loads(request)

            if request["type"] == "download_request":
                book_name = request["book_name"]
                if book_name in self.books:
                    # Envie o conteúdo do livro
                    with open(book_name, 'rb') as f:
                        while (chunk := f.read(1024)):
                            client_socket.send(chunk)
                    print(f"Livro '{book_name}' enviado com sucesso!")
                else:
                    response = {
                        "type": "download_response",
                        "success": False,
                        "message": f"Livro '{book_name}' não encontrado."
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))
            else:
                print("Tipo de solicitação inválida.")

        except Exception as e:
            print(f"Erro ao manipular cliente: {e}")
        finally:
            client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor de Peer iniciado em {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexão recebida de {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()





