import datetime

class Logger:
    def __init__(self) -> None:
        self.fileName = ""

    def log(self, input) -> None:
        input = str(input)
        fileName = "./log/log.txt"
        with open(fileName, 'a') as fileWriter:     #this is in append mode
            fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
            fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("Manually testing out logger")