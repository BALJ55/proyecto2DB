import os


class fileWorker():
    data_folder = ""

    def __init__(self):
        data_folder = "./DBS"
        print("File Worker")

    # Crea folders en el path que estemos especificand
    def create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(self.data_folder + path)
                return true
        except OSError:
            print('Error: Creating directory. ' + path)
            return false

    # Crea archivos .txt y escribe el contenido que queremos en el archivo
    def createWrite_file(self, path, content):
        file = open(self.data_folder + path, "w")
        file.write(content)
        file.close()
        return true

    # lista los objetos que se encuentren en en path especificado
    def list_files(self, path):
        files = []
        for name in os.listdir(self.data_folder + path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
        return (files)

    # Agrega datos al archivo que se esta especificado
    def append_file(self, path, content):
        file = open(self.data_folder + path, "a+")
        file.write(content)
        file.close()

    # Lee datos que se esten especificando en el path
    def read_file(self, path):
        file = open(self.data_folder + path, "r")
        if file.mode == "r":
            contenido = file.read()
            return (contenido)
        return false
