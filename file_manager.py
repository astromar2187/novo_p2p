import os

class FileManager:
    def __init__(self, directory='book_files'):
        self.directory = directory

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def get_files(self):
        return os.listdir(self.directory)

    def search_file(self, file_name):
        files = self.get_files()
        if file_name in files:
            return f"Arquivo '{file_name}' encontrado"
        else:
            return f"Arquivo '{file_name}' não encontrado"

    def remove_file(self, file_name):
        files = self.get_files()
        if file_name in files:
            os.remove(f"{self.directory}/{file_name}")
            return f"Arquivo '{file_name}' removido com sucesso!"
        else:
            return f"Arquivo '{file_name}' não encontrado"

    def add_file(self, file_name, file_content):
        with open(f"{self.directory}/{file_name}", 'w') as file:
            file.write(file_content)
        return f"Arquivo '{file_name}' adicionado com sucesso!"
    
    def get_file_content(self, file_name):
        with open(f"{self.directory}/{file_name}", 'r') as file:
            return file.read()

if __name__ == "__main__":
    files = FileManager()
    files.create_directory()
    print(files.get_files())
    