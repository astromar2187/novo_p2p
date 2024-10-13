import socket
import json

# Definição do IP e Porta do Servidor P2P
SERVER_IP = "192.168.15.53"  # Substitua pelo IP do servidor
SERVER_PORT = 5000

peer_id = None


def register_peer():
    global peer_id
    print("[DEBUG] Registrando o Peer no servidor...")
    livros = []

    #garantindo que o user ta colocando o input certo
    while not livros:  
        entrada = input("Digite os livros separados por vírgula: ")
        livros = [livro.strip() for livro in entrada.split(",") if livro.strip()]  #remove espaços em branco e entradas vazias
        
        if not livros:  # se a lista ainda estiver vazia, exibe a mensagem de erro
            print("Erro: Nenhum livro válido foi digitado. Tente novamente.")

    message = {
        "type": "register_peer",
        "livros": livros
    }

    response = send_message_to_server(message)
    
    # Verifica se o peer_id está presente e exibe a mensagem correspondente
    peer_id = response.get("peer_id")

    if peer_id:
        print(f"[DEBUG] Peer registrado com ID: {peer_id}")

    print("[DEBUG] Fim do Registro do Peer")


# Função para adicionar mais livros
def adicionar_livros():
    global peer_id
    
    # garantindo que o user ta colocando o input certo
    livros = []
    while not livros:  
        entrada = input("Digite os livros separados por vírgula: ")
        livros = [livro.strip() for livro in entrada.split(",") if livro.strip()]  #remove espaços em branco e entradas vazias
        
        if not livros:  #se a lista ainda estiver vazia, exibe a mensagem de erro
            print("Erro: Nenhum livro válido foi digitado. Tente novamente.")
    
    message = {
        "type": "add_books",
        "peer_id": peer_id,
        "livros": livros
    }

    response = send_message_to_server(message)
    
    if response and response.get("success", False):
        print(f"Livros {livros} adicionados com sucesso!")
    else:
        print("Erro ao adicionar livros.")
       

def search_livro(livro_name, peer_id):
    print(f"[DEBUG] Enviando solicitação para buscar livro: {livro_name}")

    message = {
        "type": "search_livro",
        "livro_name": livro_name,
        "peer_id": peer_id  # Envia o peer_id para o servidor
    }

    response = send_message_to_server(message)  # Armazena a resposta

    # Verifica se a resposta é válida
    if response is not None and "result" in response:
        print(f"Resultado da busca: {response['result']}")
    else:
        print("Erro: Resposta do servidor inválida.")


def send_message_to_server(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.send(json.dumps(message).encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()

        response_data = json.loads(response)
        return response_data
        
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None


def download_livro(livro_name, peer_id):
    print(f"[DEBUG] Enviando solicitação para baixar livro: {livro_name}")

    message = {
        "type": "download_book",
        "book_name": livro_name,
        "peer_id": peer_id  # Envia o peer_id que está baixando o livro
    }

    response = send_message_to_server(message)

    if response is not None and "success" in response:
        if response["success"]:
            print(f"Livro baixado com sucesso: {response['message']}")
        else:
            print(f"Erro ao baixar livro: {response['message']}")
    else:
        print("Erro: Resposta do servidor inválida.")


def mostrar_livros():
    print(f"[DEBUG] Enviando solicitação para mostrar livros do Peer atual ({peer_id})")

    message = {
        "type": "mostrar_livros",
        "peer_id": peer_id  # Envia o peer_id atual para o server
    }

    response = send_message_to_server(message)  # Armazena a resposta

    # Verifica se a resposta é válida
    if response is not None and "books" in response:
        print(f"Livros do Peer atual ({peer_id}): {response['books']}")
    else:
        print("Erro: Resposta do servidor inválida.")


def run_client(): 
    register_peer()

    while True:
        print("\nComandos disponíveis:")
        print("1: Buscar um livro")
        print("2: Baixar um livro")
        print("3: Adicionar mais livros")
        print(f"4: Mostrar livros do Peer atual({peer_id})")
        print("5: Sair")
        
        user_input = input("Digite um comando: ")

        if user_input == '1':
            livro_name = input("Digite o nome do livro para buscar: ").strip()
            search_livro(livro_name, peer_id)


        elif user_input == '2':
            livro_name = input("Digite o nome do livro para baixar: ").strip()
            download_livro(livro_name, peer_id)


        elif user_input == '3':
            adicionar_livros()

        elif user_input == '4':
            mostrar_livros()

        elif user_input == '5':
            print("Saindo do cliente...")
            message = {
                "type": "exit",
                "peer_id": peer_id  # Envia o peer_id para o servidor
            }
            response = send_message_to_server(message)  # Recebe a resposta do servidor
            if response is not None and "message" in response:
                print(f"Resposta do servidor: {response['message']}")
            break  # Encerra o loop após sair
        else:
            print("Comando não reconhecido! Use 1 para buscar livros, 2 para baixar livros ou 3 para sair.")

# Executar o cliente
run_client()
