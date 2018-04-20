import os
import shutil

data_folder = "DBS/"


class fileWorker():

    # Crea folders en el path que estemos especificand
    def create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(data_folder + path)
        except OSError:
            print('Error: Creating directory. ' + path)

    # Crea archivos .txt y escribe el contenido que queremos en el archivo
    def createWrite_file(self, path, content):
        file = open(data_folder + path, "w")
        file.write(content)
        file.close()
        return True

    # lista los objetos que se encuentren en en path especificado
    def list_files(self, path):
        files = []
        for name in os.listdir(data_folder + path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
        return (files)

    # Agrega datos al archivo que se esta especificado
    def append_file(self, path, content):
        file = open(data_folder + path, "a+")
        file.write(content)
        file.close()

    # Lee datos que se esten especificando en el path
    def read_file(self, path):
        file = open(data_folder + path, "r")
        if file.mode == "r":
            contenido = file.read()
            return (contenido)

    def remove_folder(self, path):

        if os.path.exists(data_folder + path):
            shutil.rmtree(data_folder + path)
            return True
        return False
