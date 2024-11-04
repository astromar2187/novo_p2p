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

    def livros(self, livros):
        self.books =livros

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
        peer_ip, books = response["info"]
        print(f"Dados armazenados no tracker atualmente: ")
        print(f"Peer ID: {self.peer_id} | IP: {peer_ip} | Livros: {books}")
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
                print("[Socket]Erro: resposta vazia do servidor tracker.")
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

                # Receber o arquivo
                data = peer_socket.recv(1024).decode('utf-8')
                if data:
                    print(f"[Socket]Livro '{book_name}' recebido com sucesso!")
                    # Adicionar o livro baixado à lista de livros locais
                    self.books.append(book_name)
                    print(f"[Socket]O livro '{book_name}' foi adicionado à sua lista de livros.")

                    # Notificar o tracker sobre a atualização da lista de livros
                    self.update_tracker_books()
                    return data
                else:
                    print(f"[Socket]Arquivo vazio.")
                peer_socket.close()

            else:
                print(response["message"])

            soc.close()

        except json.JSONDecodeError:
            print("[Socket]Erro: resposta inválida recebida, não é JSON.")
        except Exception as e:
            print(f"[Socket]Erro ao tentar baixar o livro: {e}")

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

    def get_list_books(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.tracker_ip, self.tracker_port))
        message = {
            "type": "get_list_books"
        }
        soc.send(json.dumps(message).encode('utf-8'))
        response = soc.recv(1024).decode('utf-8')
        response = json.loads(response)
        info = response["info"]
        soc.close()
        return info

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            request = json.loads(request)

            if request["type"] == "download_request":
                book_name = request["book_name"]
                if book_name in self.books:
                    # Envie o conteúdo do livro
                    try:
                        book_path = os.path.join('book_files', book_name)
                        with open(book_path, 'rb') as f:
                            while (chunk := f.read(1024)):
                                client_socket.send(chunk)
                        print(f"Livro '{book_name}' enviado com sucesso!")
                    except FileNotFoundError:
                        response = {
                            "type": "download_response",
                            "success": False,
                            "message": f"Livro '{book_name}' não encontrado no servidor."
                        }
                        client_socket.send(json.dumps(response).encode('utf-8'))
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




