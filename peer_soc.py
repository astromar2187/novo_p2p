import socket
import json

class PeerClient:
    def __init__(self, ip_trk, porta_trk = 5000, livros = []):
        self.ip_trk = ip_trk
        self.porta_trk = porta_trk
        self.peer_id = None
        self.livros = livros

    def register_peer(self):
        print("[DEBUG] Registrando o Peer no servidor...")

        #garantindo que o user ta colocando o input certo
        #while not self.livros:  
            #entrada = input("Digite os livros separados por vírgula: ")
            #livros = [livro.strip() for livro in entrada.split(",") if livro.strip()]  #remove espaços em branco e entradas vazias
            
            #if not livros:  # se a lista ainda estiver vazia, exibe a mensagem de erro
                #print("Erro: Nenhum livro válido foi digitado. Tente novamente.")

        message = {
            "type": "register_peer",
            "livros": self.livros
        }
        
        print(f"[DEBUG] Enviando mensagem para o servidor: {message}")
        response = self.send_message_to_server(message)

        # Verifica se o peer_id está presente e exibe a mensagem correspondente
        self.peer_id = response.get("peer_id")

        if self.peer_id is not None:
            print(f"[DEBUG] Peer registrado com ID: {self.peer_id}")
            print("[DEBUG] Fim do Registro do Peer")
            return self.peer_id
        else:
            print("Erro ao registrar o Peer.")
            print("[DEBUG] Fim do Registro do Peer")
            return None

    def unregister_peer(self):
        print("[DEBUG] Desregistrando o Peer no servidor...")

        message = {
            "type": "unregister_peer",
            "peer_id": self.peer_id
        }

        response = self.send_message_to_server(message)

        if response is not None and "message" in response:
            print(f"Resposta do servidor: {response['message']}")
        else:
            print("Erro: Resposta do servidor inválida.")

    def get_peer_info(self):
        message = {
            "type": "get_peer_info",
            "peer_id": self.peer_id
        }

        response = self.send_message_to_server(message)

        if response is not None and "message" in response:
            print(f"Resposta do servidor: {response['message']}")
        else:
            print("Erro: Resposta do servidor inválida.")

    # Função para atualizar a lista de livros
    def refresh_books(self):
        print("[DEBUG] Atualizando lista de livros...")
        
        '''if not self.livros:  #se a lista estiver vazia, exibe a mensagem de erro
                print("Erro: Nenhum livro válido foi digitado. Tente novamente.")'''
        
        message = {
            "type": "refresh_books",
            "peer_id": self.peer_id,
            "livros": self.livros
        }

        response = self.send_message_to_server(message)
        
        if response is not None and response["success"]:
            print(f"Livros atualizados com sucesso!")
        else:
            print("Erro ao adicionar livros.")
        

    def search_livro(self, livro_name):
        print(f"[DEBUG] Enviando solicitação para buscar livro: {livro_name}")

        message = {
            "type": "search_livro",
            "livro_name": livro_name,
            "peer_id": self.peer_id  # Envia o peer_id para o servidor
        }

        response = self.send_message_to_server(message)  # Armazena a resposta

        # Verifica se a resposta é válida
        if response is not None and "result" in response:
            print(f"Resultado da busca: {response['result']}")
        else:
            print("Erro: Resposta do servidor inválida.")


    def send_message_to_server(self, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip_trk, self.porta_trk))
            client_socket.send(json.dumps(message).encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')
            client_socket.close()

            response_data = json.loads(response)
            return response_data
            
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return None


    def download_livro(self, livro_name):
        print(f"[DEBUG] Enviando solicitação para baixar livro: {livro_name}")

        message = {
            "type": "download_book",
            "book_name": livro_name,
            "peer_id": self.peer_id  # Envia o peer_id que está baixando o livro
        }

        response = self.send_message_to_server(message)

        if response is not None and "success" in response:
            if response["success"]:
                print(f"Livro baixado com sucesso: {response['message']}")
            else:
                print(f"Erro ao baixar livro: {response['message']}")
        else:
            print("Erro: Resposta do servidor inválida.")


    '''def mostrar_livros(self):
        print(f"[DEBUG] Enviando solicitação para mostrar livros do Peer atual ({self.peer_id})")

        message = {
            "type": "mostrar_livros",
            "peer_id": self.peer_id  # Envia o peer_id atual para o server
        }

        response = self.send_message_to_server(message)  # Armazena a resposta

        # Verifica se a resposta é válida
        if response is not None and "books" in response:
            print(f"Livros do Peer atual ({self.peer_id}): {response['books']}")
        else:
            print("Erro: Resposta do servidor inválida.")'''


    '''def run_client(self): 
        self.register_peer()

        while True:
            print("\nComandos disponíveis:")
            print("1: Buscar um livro")
            print("2: Baixar um livro")
            #print("3: Adicionar mais livros")
            print(f"4: Mostrar livros do Peer atual({self.peer_id})")
            print("5: Sair")
            
            user_input = input("Digite um comando: ")

            if user_input == '1':
                livro_name = input("Digite o nome do livro para buscar: ").strip()
                self.search_livro(livro_name)


            elif user_input == '2':
                livro_name = input("Digite o nome do livro para baixar: ").strip()
                self.download_livro(livro_name)


            elif user_input == '3':
                self.adicionar_livros()

            elif user_input == '4':
                self.mostrar_livros()

            elif user_input == '5':
                print("Saindo do cliente...")
                message = {
                    "type": "exit",
                    "peer_id": self.peer_id  # Envia o peer_id para o servidor
                }
                response = self.send_message_to_server(message)  # Recebe a resposta do servidor
                if response is not None and "message" in response:
                    print(f"Resposta do servidor: {response['message']}")
                break  # Encerra o loop após sair
            else:
                print("Comando não reconhecido! Use 1 para buscar livros, 2 para baixar livros ou 3 para sair.")'''

    




