# client.py
import socket
import json

# Definição do IP e Porta do Servidor P2P
SERVER_IP = "192.168.15.53"
SERVER_PORT = 5000

# Definição dos livros locais desse peer
peer_id = input("Digite o ID do peer: ")  # Exemplo: "peer_1"
livros = input("Digite os livros separados por vírgula: ").split(",")  # Exemplo: "ana, vini"
livros = [livro.strip() for livro in livros]  # Remove espaços extras

# Função para registrar o peer no servidor
def register_peer(): 
    print("[DEBUG] Registrando o peer no servidor...") #mostra que está registrando o peer no servidor
    message = { #cria a mensagem para registrar o peer, em json
        "type": "register_peer", #tipo da mensagem é register_peer, ou seja, serve para indicar que o peer quer ser registrado
        "peer_id": peer_id, #id do peer
        "livros": livros #livros do peer
    }
    send_message_to_server(message) #envia a mensagem para o servidor
    print("[DEBUG] Fim de register_peer") #mostra que o peer foi registrado com sucesso

# Função para buscar um livro no servidor
def search_livro(livro_name): 
    print(f"[DEBUG] Enviando solicitação para buscar livro: {livro_name}") #mostra que está buscando o livro
    message = { #cria a mensagem para buscar o livro, em json
        "type": "search_livro", #tipo da mensagem é search_livro, ou seja, serve para indicar que o peer quer buscar um livro
        "livro_name": livro_name #nome do livro a ser buscado
    }
    send_message_to_server(message) #envia a mensagem para o servidor

# Função para enviar mensagens ao servidor e receber resposta
def send_message_to_server(message):
    try: #tenta enviar a mensagem
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket do cliente
        client_socket.connect((SERVER_IP, SERVER_PORT)) #conecta o cliente ao servidor
        client_socket.send(json.dumps(message).encode('utf-8')) #envia a mensagem ao servidor

        # Receber resposta do servidor
        response = client_socket.recv(1024).decode('utf-8') #recebe a resposta do servidor
        print(f"Resposta do servidor: {response}") #mostra a resposta do servidor
    except Exception as e: #se der erro
        print(f"Erro ao enviar mensagem: {e}")  #mostra o erro
        
    print("fechando conexão...") #mostra que a conexão está sendo fechada
    client_socket.close() #fecha o socket do cliente

# Função principal do cliente para interagir com o servidor
def run_client(): 
    # Registrar o peer no servidor
    register_peer() #registra o peer no servidor

    # Loop de interação com o usuário
    while True: #enquanto estiver ativo
        print("\nComandos disponíveis: 1 para buscar um livro, 2 para sair")
        user_input = input("Digite um comando: ")

        if user_input.lower() == '1':
            livro_name = input("Digite o nome do livro para buscar: ").strip()
            search_livro(livro_name)
        elif user_input.lower() == '2':
            print("Saindo do cliente...")
            break
        else:
            print("Comando não reconhecido! Use 1 para buscar livros ou 2 para sair.")

# Executar o cliente
run_client()
