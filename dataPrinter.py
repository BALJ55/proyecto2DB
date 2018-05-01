class dbDataPrinter():

    def print_table(self, data, header):

        data = list(data)
        MaxLength = 0
        data.insert(0, header)

        for i in range(0, len(data)):
            for x in data[i]:
                MaxLength = len(str(x)) if MaxLength < len(str(x)) else MaxLength

        print("-" * MaxLength * len(data[i]) + "----------")

        for i in range(0, len(data)):

            for x in range(0, len(data[i])):
                Length = MaxLength - len(str(data[i][x]))
                print("| " + str(data[i][x]) + (" " * Length), end=" ")
            print("|")

            if (not i):
                print("-" * MaxLength * len(data[i]) + "----------")

        print("-" * MaxLength * len(data[i]) + "----------")
