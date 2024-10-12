#from peer.client import PeerClient
from file_manager import FileManager
from estilos import Estilos

def menu():
    #peer_client = PeerClient()

    while True:
        estilos.exibir_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1': #MUDAR ISSO PARA CONFERIR REGISTRO NA REDE   
            print("[DEBUG] Registrando o peer no servidor...") #mostra que está registrando o peer no servidor
            #peer_client.register_to_tracker()

        elif choice == '2':
            print("Livros baixados:")
            livros = files.get_files()
            for livro in livros:
                print(f"  - {livro}")
            res = input("Deseja abrir algum livro? (s/n) ")
            while res not in ['s', 'n']:
                res = input("Opção inválida. Deseja abrir algum livro? (s/n) ")
            if res == 's':
                book_name = input("Nome do livro: ")
                files.open_file(book_name)

        elif choice == '3':
            book_name = input("Nome do livro: ")
            res = input("Tem certeza que deseja remover o livro? (s/n) ")
            while res not in ['s', 'n']:
                res = input("Opção inválida. Tem certeza que deseja remover o livro? (s/n) ")
            if res == 's':
                print("Removendo livro...")
                files.remove_file(book_name)

        elif choice == '4':
            book_name = input("Nome do livro: ")
            #peer_client.search_book_in_network(book_name)
            
            download_choice = input("Gostaria de proceder com o download do livro? (s/n) ")
            while download_choice not in ['s', 'n']:
                download_choice = input("Opção inválida. Gostaria de proceder com o download do livro? (s/n) ")
            
            if download_choice == 's':
                print("[DEBUG] Fazendo download do livro...")
                #peer_client.download_book(book_name)

        elif choice == '5':
            print("Deixando servidor...")
            #peer_client.unregister_from_tracker()
            break

        else:
            print("Opção inválida.")

def register_peer():
    peer_id = input("Digite o ID do peer: ")  # Exemplo: "peer_1"
    livros = input("Digite os livros separados por vírgula: ").split(",")  # Exemplo: "ana, vini"
    livros = [livro.strip() for livro in livros]  # Remove espaços extras

if __name__ == "__main__":
    estilos = Estilos()
    files = FileManager()

    estilos.exibir_título()
    


    menu()

