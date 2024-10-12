import socket
import json

# Definição do IP e Porta do Servidor P2P
SERVER_IP = "192.168.15.53"  # Substitua pelo IP do servidor
SERVER_PORT = 5000

# Definição dos livros locais desse peer
peer_id = None

# Função para registrar o peer no servidor
def register_peer():
    global peer_id
    print("[DEBUG] Registrando o peer no servidor...")

    livros = input("Digite os livros separados por vírgula: ").split(",")
    livros = [livro.strip() for livro in livros]

    message = {
        "type": "register_peer",  # Tipo da mensagem é register_peer
        "books": livros  # Corrigido para "books"
    }

    peer_id = send_message_to_server(message)  # Envia a mensagem para o servidor
    print("[DEBUG] Fim de register_peer")

# Função para buscar um livro no servidor
def search_livro(livro_name):
    print(f"[DEBUG] Enviando solicitação para buscar livro: {livro_name}")
    message = {
        "type": "search_book",  # Tipo da mensagem corrigido para "search_book"
        "book_name": livro_name  # Corrigido para "book_name"
    }
    send_message_to_server(message)

# Função para enviar mensagens ao servidor e receber resposta
# Função para enviar mensagens ao servidor e receber resposta
def send_message_to_server(message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.send(json.dumps(message).encode('utf-8'))

        # Receber resposta do servidor
        response = client_socket.recv(1024).decode('utf-8')

        if not response:
            print("Resposta do servidor está vazia.")
            return None

        print(f"Resposta do servidor: {response}")

        # Fechar conexão
        client_socket.close()

        response_data = json.loads(response)
        if "peer_id" in response_data:
            return response_data["peer_id"]
        return None
    
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None


# Função principal do cliente para interagir com o servidor
def run_client():
    # Registrar o peer no servidor
    register_peer()

    # Loop de interação com o usuário
    while True:
        print("\nComandos disponíveis: 1 para buscar um livro, 2 para sair")
        user_input = input("Digite um comando: ")

        if user_input.lower() == '1':
            livro_name = input("Digite o nome do livro para buscar: ").strip()
            search_livro(livro_name)
        elif user_input.lower() == '2':
            print("Saindo do cliente...")
            # Enviar mensagem de saída ao servidor com o peer_id
            message = {
                "type": "exit",
                "peer_id": peer_id  # Certifique-se de enviar o peer_id
            }
            send_message_to_server(message)
            break
        else:
            print("Comando não reconhecido! Use 1 para buscar livros ou 2 para sair.")

# Executar o cliente
run_client()
