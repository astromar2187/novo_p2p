# Códigos ANSI para cores
MAGENTA = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Reseta para a cor padrão do terminal

class Estilos:
    def __init__(self):
        pass

    def exibir_título(self):
        # Título colorido
        print(f"{MAGENTA}______________________________________________________________ ")
        print(f"{MAGENTA}______________________________________________________________ ")
        print(f"{CYAN}                                                            ")
        print(f"{CYAN} {GREEN}                     Bem-vindo ao BookTorrent              {CYAN}")
        print(f"{CYAN} {YELLOW}            Uma rede de compartilhamento de livros         {CYAN}")
        print(f"{CYAN} {MAGENTA}                        peer-to-peer                       {CYAN}")
        print(f"{CYAN}                                                            ")
        print(f"{CYAN} {BLUE}              Registre-se para começar a ler!              {CYAN}")
        print(f"{CYAN}                                                            ")
        print(f"{MAGENTA}-------------------------------------------------------------- ")
        print(f"{MAGENTA}-------------------------------------------------------------- ")
        print(RESET)  # Reseta a cor após o texto

    def exibir_menu(self):
        # Menu colorido
     # Menu centralizado e estilizado
        print(f"{MAGENTA}\n____________________________________________________________ ")
        print(f"                                                            ")
        print(f"                              {CYAN}Menu:                         ")
        print(f"{MAGENTA}____________________________________________________________")
        print(f" {BLUE}1.{CYAN} Conferir registro na rede                               ")
        print(f" {BLUE}2.{CYAN} Ver livros baixados                                     ")
        print(f" {BLUE}3.{CYAN} Remover livro baixado                                   ")
        print(f" {BLUE}4.{CYAN} Buscar novo livro na rede                               ")
        print(f" {BLUE}5.{CYAN} Sair                                                    ")
        print(f"{MAGENTA}____________________________________________________________")
        print(RESET)  # Reseta a cor após o texto



