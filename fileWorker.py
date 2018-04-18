import os

class fileWorker():
    def  __init__(self):
        current_dataBase = ""
        print ("File Worker")

    #Crea folders en el path que estemos especificand
    def create_folder(path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print ('Error: Creating directory. ' + path)

    #Crea archivos .txt y escribe el contenido que queremos en el archivo
    def createWrite_file(path, content):
        file = open(path, "w")
        file.write(content)
        file.close()

    #lista los objetos que se encuentren en en path especificado
    def list_files(path):
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
        return(files)

    #Agrega datos al archivo que se esta especificado
    def append_file(path, content):
        file = open(path, "a+")
        file.write(content)
        file.close()

    #Lee datos que se esten especificando en el path
    def read_file(path):
        file = open(path,"r")
        if file.mode == "r":
            contenido = file.read()
            return(contenido)
