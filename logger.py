import datetime
import json
from pathlib import Path

class Logger:
    def __init__(self) -> None:
        self.fileName = ""

    def log(self, input, title:bool=False, newline:bool=False) -> None:
        input = str(input)
        fileName = "./log/log.txt"                  #need to create a "log" directory in the current directory (also need to cd to this directory for this to work)
        with open(fileName, 'a') as fileWriter:     #this is in append mode
            if (not newline):
                fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
                fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

    def compareAsset(self, weeklyLogPath:Path, compPath:Path, id, model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order) -> None:
        #TODO: The current system will only log for asset creations and updates. We need to store the IDs in a list and run it afterwards to see if any assets were deleted
        try:
            if compPath.stat().st_size == 0:
                self.logCreation(weeklyLogPath, id, model)
                with open(compPath, 'a') as compareFile:
                    # TODO: Write the asset to compPath
                    ...
            else:
                compStr = ""
                with open(compPath, 'r') as compFile:
                    compStr = compFile.read()
                print (compStr)
                compJSON = json.loads(compStr)
                print(compJSON)

            for asset in compJSON:
                if asset['id'] == id:
                    #TODO: Double check the field names are correct with what will actually be stored
                    fieldList:list = ['model', 'itemName', 'productNum', 'currQty', 'reorderAtQty', 'qtyToOrder', 'order']
                    inputtedList:list = [model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order]

                    for field, input in zip(fieldList, inputtedList):
                        if asset[field] != input:
                            self.logChange(weeklyLogPath, field, id, model, asset[field], input)
                            asset[field] = input
                            with open(compPath, 'w') as compareFile:
                                compareFile.write(compJSON)
                    break

        except Exception as ex:
            print(f"Compare Asset Error: {ex}")
            self.log(f"Compare Asset Error: {ex}")

    def logCreation(self, weeklyLogPath, id, model) -> None:
        try:
            logMsg:str = f"{'{:%a, %b-%d}'.format(datetime.datetime.now())}\tAsset creation: ID: {id}, Name: {model}\n"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset creation for {model}: {ex}")
            self.log(f"Error logging asset creation for {model}: {ex}")

    def logChange(self, weeklyLogPath, fieldName, id, model, prev, curr) -> None:
        try:
            logMsg:str = f"{'{:%a, %b-%d}'.format(datetime.datetime.now())}\tAsset change: ID: {id}, Name: {model}\n\tField: {fieldName}, Previous: {prev}, Current: {curr}\n"
            print(logMsg)
            with open (weeklyLogPath, 'a') as weeklyLog:
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset change ({fieldName}) for {model}: {ex}")
            self.log(f"Error logging asset change ({fieldName}) for {model}: {ex}")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("Manually testing out logger")