#from peer.client import PeerClient
from file_manager import FileManager
from estilos import Estilos
from peer_soc import PeerClient

if __name__ == "__main__":
    # Inicialização de classes de estilos e de manipulação de arquivos
    estilos = Estilos()
    files = FileManager()
    files.create_dir()
    
    # Exibição do título do programa
    estilos.exibir_titulo()

    # Inicialização do cliente peer
    ip_trk = '192.168.15.53'
    porta_trk = 5000
    livros = files.get_files()
    soc = PeerClient(ip_trk, porta_trk, livros)
    soc.register_peer() #registro do cliente

    # Loop principal do programa
    while True:
        estilos.exibir_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1': #MUDAR ISSO PARA CONFERIR REGISTRO NA REDE   
            print("Diagnóstico do registro na rede...")
            soc.get_peer_info()

        elif choice == '2': 
            print("Atualizando registro na rede...")
            livros = files.get_files()
            soc.livros = livros
            soc.refresh_books()

        # Exibir livros baixados
        elif choice == '3':
            print("Livros baixados:")
            livros = files.get_files()
            count = 1
            for livro in livros:
                print(f" {count} - {livro}")
                count += 1
            res = input("Deseja abrir algum livro? (s/n) ")
            while res not in ['s', 'n']:
                res = input("Opção inválida. Deseja abrir algum livro? (s/n) ")
            if res == 's':
                op = input("Digite o número correspondente ao livro: ")
                while not op.isdigit() or int(op) < 1 or int(op) > len(livros):
                    op = input("Opção inválida. Digite 0 para cancelar ou Digite o número do livro: ")
                book_name = livros[int(op) - 1]
                conteudo = files.get_file_content(book_name)
                estilos.exibir_cont_livro(book_name, conteudo)

        # Remover livro baixado
        elif choice == '4': #MELHORAR ISSO AQUI PELO AMOR DE DEUS
            print("Livros baixados:")
            livros = files.get_files()
            count = 1
            for livro in livros:
                print(f" {count} - {livro}")
                count += 1
            op = input("Digite o número correspondente ao livro: ")
            while not op.isdigit() or int(op) < 1 or int(op) > len(livros):
                op = input("Opção inválida. Digite 0 para cancelar ou Digite o número do livro: ")
            book_name = livros[int(op) - 1]

            res = input("Tem certeza que deseja remover o livro? (s/n) ")
            while res not in ['s', 'n']:
                res = input("Opção inválida. Tem certeza que deseja remover o livro? (s/n) ")
            if res == 's':
                print("Removendo livro...")
                files.remove_file(book_name)
                livros_atual = files.get_files()
                soc.livros = livros_atual
                soc.refresh_books()
                print("Livro removido com sucesso.")

        # Buscar novo livro na rede
        elif choice == '5':
            book_name = input("Nome do livro: ")
            soc.search_book(book_name)
            
            download_choice = input("Gostaria de proceder com o download do livro? (s/n) ")
            while download_choice not in ['s', 'n']:
                download_choice = input("Opção inválida. Gostaria de proceder com o download do livro? (s/n) ")
            
            if download_choice == 's':
                print("[DEBUG] Fazendo download do livro...")
                #peer_client.download_book(book_name)
   
        elif choice == '6':
            print("Deixando servidor...")
            soc.unregister_peer()
            break

        else:
            print("Opção inválida.")

