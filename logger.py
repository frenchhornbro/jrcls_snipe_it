import datetime
import json
from pathlib import Path

class Logger:
    def __init__(self) -> None:
        self.fileName = ""

    def log(self, input, title:bool=False, newline:bool=False) -> None:
        logFolder:Path = Path("./log")
        logFile:Path = Path("./log/log.txt")       #need to cd to this directory in the bat file for this to work
        input = str(input)
        if (not logFile.exists()):
            logFolder.mkdir(parents=True)
        with open(logFile, 'a') as fileWriter:     #this is in append mode
            if (not newline):
                fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
                fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

    def compareAsset(self, weeklyLogFile:Path, compFile:Path, id, model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order) -> None:
        try:
            if compFile.stat().st_size == 0:
                # No compare file, need to create it
                with open(weeklyLogFile, 'a') as weeklyLog:
                    weeklyLog.write(f"{'{:%a, %b-%d}'.format(datetime.datetime.now())}\tWeekly log created")

            compStr:str = ""
            with open(compFile, 'r') as compareFile:
                compStr = compareFile.read()
            print (compStr)
            compJSON:dict = json.loads(compStr)
            print(compJSON)

            found:bool = False
            for asset in compJSON:
                if asset['id'] == id:
                    found = True
                    fieldList:list = ['model', 'itemName', 'productNum', 'currQty', 'reorderAtQty', 'qtyToOrder', 'order']
                    inputtedList:list = [model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order]
                    
                    for field, input in zip(fieldList, inputtedList):
                        if asset[field] != input:
                            self.logChange(weeklyLogFile, field, id, model, asset[field], input)
                            asset[field] = input
                            compJSON[id] = asset
                            with open(compFile, 'w') as compareFile:
                                compareFile.write(compJSON)
                    break
            if not found:
                # This was created
                self.logCreation(weeklyLogFile, id, model, currQty)
                with open(compFile, 'w') as compareFile:
                    # The IDs are the keys, all fields are the values
                    fields:dict = {'id': id, 'model': model, 'itemName': itemName, 'productNum': productNum, 'currQty': productNum, 'reorderAtQty': reorderAtQty, 'qtyToOrder': qtyToOrder, 'order': order}
                    compJSON[id] = fields
        except Exception as ex:
            print(f"Compare Asset Error: {ex}")
            self.log(f"Compare Asset Error: {ex}")

    def logCreation(self, weeklyLogPath:Path, id, model, qty) -> None:
        try:
            logMsg:str = f"{'{:%a, %b-%d}'.format(datetime.datetime.now())}\tAsset creation: ID: {id}, Name: {model}, Quantity: {qty}\n"
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

    def logDeletion(self, weeklyLogPath:Path, id, model, qty) -> None:
        try :
            logMsg:str = f"{'{:%a, %b-%d}'.format(datetime.datetime.now())}\tAsset deletion: ID: {id}, Name: {model}, Quantity: {qty}"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                weeklyLog.write(logMsg)
        except Exception as ex:
            print(f"Error logging asset deletion for {model}: {ex}")
            self.log(f"Error logging asset deletion for {model}: {ex}")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("Manually testing out logger")