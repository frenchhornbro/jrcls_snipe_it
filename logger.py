import datetime

class Logger:
    def __init__(self) -> None:
        self.fileName = ""

    def log(self, input, title:bool=False) -> None:
        input = str(input)
        fileName = "./log/log.txt"                  #need to create a "log" directory in the current directory (also need to cd to this directory for this to work)
        with open(fileName, 'a') as fileWriter:     #this is in append mode
            fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
            fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("Manually testing out logger")