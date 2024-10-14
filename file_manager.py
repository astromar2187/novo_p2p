import os

class FileManager:
    def __init__(self, dir='book_files'):
        self.dir = dir

    def create_dir(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def get_files(self):
        return os.listdir(self.dir)

    def search_file(self, file_name):
        files = self.get_files()
        if file_name in files:
            return f"Arquivo '{file_name}' encontrado"
        else:
            return f"Arquivo '{file_name}' não encontrado"

    def remove_file(self, file_name):
        files = self.get_files()
        if file_name in files:
            os.remove(f"{self.dir}/{file_name}")
            return f"Arquivo '{file_name}' removido com sucesso!"
        else:
            return f"Arquivo '{file_name}' não encontrado"

    def add_file(self, file_name, file_content):
        with open(f"{self.dir}/{file_name}", 'w') as file:
            file.write(file_content)
        return f"Arquivo '{file_name}' adicionado com sucesso!"
    
    def get_file_content(self, file_name):
        with open(f"{self.dir}/{file_name}", 'r') as file:
            return file.read()

    