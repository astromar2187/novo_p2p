from peer_soc import PeerClient
import os
import threading
from estilos import Estilos
from file_manager import FileManager


if __name__ == "__main__":
    # Inicialização de estilos e gerenciador de arquivos
    estilos = Estilos()
    files = FileManager()
    files.create_dir() # Cria o diretório de arquivos, se não existir

    # Configurações do tracker
    ip_trk = '192.168.0.65'  # IP do tracker
    porta_trk = 5000
    
    # Exibição do título do programa
    estilos.exibir_titulo()

    # Inicialização do peer
    livros = files.get_files() # Obtém todos os arquivos .txt no diretório book_files
    soc = PeerClient(ip_trk, porta_trk, livros)
    soc.register_peer()  # Registra o cliente

    # Inicia o servidor do peer
    threading.Thread(target=soc.start_server, daemon=True).start()
    # Loop principal do programa
    while True:
        flag = True
        estilos.exibir_menu()
        choice = input("Escolha uma opção: ")

        # Diagnóstico do registro na rede
        if choice == '1':  
            print("Diagnóstico do registro na rede...")
            soc.get_peer_info()

        # Atualizar registro na rede
        elif choice == '2': 
            print("Atualizando registro na rede...")
            livros = files.get_files()
            soc.livros(livros)
            soc.update_tracker_books()

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
                    if op == '0':
                        flag = False
                        break
                
                if flag:
                    book_name = livros[int(op) - 1]
                    conteudo = files.get_file_content(book_name)
                    estilos.exibir_cont_livro(book_name, conteudo)

        # Remover livro baixado
        elif choice == '4': 
            print("Livros baixados:")
            livros = files.get_files()
            count = 1
            for livro in livros:
                print(f" {count} - {livro}")
                count += 1
            op = input("Digite o número correspondente ao livro: ")
            while not op.isdigit() or int(op) < 1 or int(op) > len(livros):
                op = input("Opção inválida. Digite 0 para cancelar ou Digite o número do livro: ")
                if op == '0':
                    flag = False
                    break
            if flag:
                book_name = livros[int(op) - 1]

                res = input("Tem certeza que deseja remover o livro? (s/n) ")
                while res not in ['s', 'n']:
                    res = input("Opção inválida. Tem certeza que deseja remover o livro? (s/n) ")
                if res == 's':
                    print("Removendo livro...")
                    files.remove_file(book_name)
                    livros_atual = files.get_files()
                    soc.livros(livros_atual)
                    soc.update_tracker_books()
                    print("Livro removido com sucesso.")

        # Baixar livro
        elif choice == '5':
            print("Lista de livros disponíveis:")
            livros_disponiveis = soc.get_list_books()
            count = 1
            livros = []

            for id in livros_disponiveis:
                print(f"Peer ID: {id} | IP: {livros_disponiveis[id][0]}")
                livros.extend(livros_disponiveis[id][1])
                for j in livros_disponiveis[id][1]:
                    print(f" {count} - {j}")
                    count += 1

               
            op = input("Digite o número correspondente ao livro que deseja baixar (ou 0 para cancelar): ")
            while not op.isdigit() or int(op) < 0 or int(op) > len(livros):
                op = input("Opção inválida. Digite o número correspondente ao livro que deseja baixar (ou 0 para cancelar): ")
                
            if int(op) != 0:
                book_name = livros[int(op) - 1]
                if book_name in files.get_files():
                    print("[Main] Livro já está baixado.")
                else:
                    download_choice = input("Gostaria de proceder com o download do livro? (s/n): ")
                    while download_choice not in ['s', 'n']:
                        download_choice = input("Opção inválida. Gostaria de proceder com o download do livro? (s/n): ")
                    if download_choice == 's':
                        print("[Main] Fazendo download do livro...")
                        conteudo = soc.download_book(book_name)
                        if conteudo:
                            files.save_file(book_name, conteudo)
                            print("[Main] Download concluído. Livro salvo com sucesso.")

        elif choice == '6':
            soc.unregister_peer()
            break


