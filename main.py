from peer_soc import PeerClient
import os
import threading

def get_files():
    # Obtém todos os arquivos .txt no diretório atual
    return [f for f in os.listdir() if f.endswith('.txt')]

if __name__ == "__main__":
    ip_trk = '192.168.0.65'  # IP do tracker
    porta_trk = 5000
    livros = get_files()
    
    soc = PeerClient(ip_trk, porta_trk, livros)
    soc.register_peer()  # Registra o cliente

    # Iniciar o servidor do peer
    threading.Thread(target=soc.start_server, daemon=True).start()

    while True:
        print("\n1. Mostrar arquivos disponíveis")
        print("2. Baixar arquivo")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            soc.get_peer_info()

        elif choice == '2':
            book_name = input("Nome do livro que deseja baixar: ")
            soc.download_book(book_name)

        elif choice == '3':
            soc.unregister_peer()
            break

        else:
            print("Opção inválida.")
