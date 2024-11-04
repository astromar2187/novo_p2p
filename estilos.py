# Códigos ANSI para cores
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Reseta para a cor padrão do terminal

class Estilos:
    def __init__(self):
        self.dimensao_tela = 65  # Largura da tela

    '''Exibe o conteúdo centralizado com a cor escolhida'''
    def center(self, conteudo, cor):
        # Calcula o espaço vazio para centralizar o texto
        espaco_vazio = (self.dimensao_tela - len(conteudo)) // 2
        print(f"{cor}{' ' * espaco_vazio}{conteudo}{' ' * espaco_vazio}{RESET}")
    
    def left(self, conteudo, cor):
        print(f"{cor}{conteudo}{RESET}")

    def repetir_caractere(self, caractere, vezes):
        return caractere * vezes

    def exibir_titulo(self):
        # Título colorido
        print(f"{MAGENTA}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        print(f"{MAGENTA}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        self.center("Bem-vindo ao BookTorrent", GREEN)
        self.center("Uma rede de compartilhamento de livros peer-to-peer", YELLOW)
        self.center("Registre-se para começar a ler!", MAGENTA)
        print(f"{MAGENTA}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        print(f"{MAGENTA}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        print(RESET)


    '''def exibir_menu(self):
        # Menu colorido
     # Menu centralizado e estilizado
        print(f"{MAGENTA}\n____________________________________________________________ ")
        print(f"                                                            ")
        print(f"                              {CYAN}Menu:                         ")
        print(f"{MAGENTA}____________________________________________________________")
        print(f" {BLUE}1.{CYAN} Conferir registro na rede                               ")
        print(f" {BLUE}2.{CYAN} Atualizar registro na rede                              ")
        print(f" {BLUE}3.{CYAN} Ver livros baixados                                     ")
        print(f" {BLUE}4.{CYAN} Remover livro baixado                                   ")
        print(f" {BLUE}5.{CYAN} Buscar novo livro na rede                               ")
        print(f" {BLUE}6.{CYAN} Sair                                                    ")
        print(f"{MAGENTA}____________________________________________________________")
        print(RESET)  # Reseta a cor após o texto'''

    def exibir_menu(self):
        count = 1
        print(f"{CYAN}{self.repetir_caractere('_', self.dimensao_tela)}")
        self.center("Menu:", MAGENTA)
        print(f"{CYAN}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        
        opcoes = ["Conferir registro na rede", 
            "Atualizar registro na rede", 
            "Ver livros baixados", 
            "Remover livro baixado", 
            "Buscar novo livro na rede", 
            "Sair"]

        for opcao in opcoes:
            self.left(f"{count}. {opcao}", RESET)
            count += 1

        print(f"{CYAN}{self.repetir_caractere('_', self.dimensao_tela)}")
        print(RESET)
        #print("\n")
        
    def exibir_cont_livro(self, book_name, book_content):
        print(f"{RED}{self.repetir_caractere('_', self.dimensao_tela)}")
        print("\n")
        self.center(f"Livro: {book_name}", CYAN)
        print("\n")
        
        # Quebra o conteúdo do livro em linhas de acordo com a largura da tela
        #book_content = [book_content[i:i+self.dimensao_tela] for i in range(0, len(book_content), self.dimensao_tela)]

        # Exibe o conteúdo do livro
        print(f"{RESET}{book_content}")

        print(f"{RED}{self.repetir_caractere('_', self.dimensao_tela)}")
        #print("\n")
        print(RESET)



