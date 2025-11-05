from datetime import datetime
import os
from pathlib import Path

class Logger:
    def __init__(self) -> None:
        self.logFile: Path = Path("./log/log.txt")       #need to cd to this directory in the bat file for this to work
        os.makedirs(os.path.dirname(self.logFile), exist_ok=True)

    def log(self, input, title: bool=False, newline: bool=False) -> None:
        with open(self.logFile, 'a') as fileWriter:     #this is in append mode
            if (not newline):
                fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.now()))
                fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(str(input))
            fileWriter.write("\n")

if __name__ == '__main__':
    logger: Logger = Logger()
    logger.log("TEST:\tManually testing out logger", True)