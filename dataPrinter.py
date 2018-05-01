
class dataPrinter():

    def print_table(array, header):

        array = list(array)
        MaxLength = 0
        array.insert(0,header)

        for i in range(0, len(array)):
            for x in array[i]:
                MaxLength = len(str(x)) if MaxLength < len(str(x)) else MaxLength

        print("-" * MaxLength * len(array[i]) + "----------")

        for i in range(0, len(array)):

            for x in range(0, len(array[i])):

                Length = MaxLength - len(str(array[i][x]))
                print( "| "+str(array[i][x])+(" " * Length) , end=" " )
            print("|")

            if (not i):
                print("-" * MaxLength * len(array[i])+"----------")

        print("-" * MaxLength * len(array[i]) + "----------")





