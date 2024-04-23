import json
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self) -> None:
        self.fileName = ""

    def log(self, input, title:bool=False, newline:bool=False) -> None:
        logFolder:Path = Path("./log")
        logFile:Path = Path("./log/log.txt")       #need to cd to this directory in the bat file for this to work
        input = str(input)
        if (not logFolder.exists()):
            logFolder.mkdir(parents=True)
        with open(logFile, 'a') as fileWriter:     #this is in append mode
            if (not newline):
                fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.now()))
                fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

    def compareAsset(self, weeklyLogFile:Path, compFile:Path, changeMade:bool, id:str, model:str, itemName:str, productNum:str, currQty:str, reorderAtQty:str, qtyToOrder:str, order:str) -> bool:
        try:
            compFileSize:int = compFile.stat().st_size
            if compFileSize == 0:
                # No compare file, need to create it
                with open(compFile, 'w') as compareFile:
                    compareFile.write("{}")

            compStr:str = ""
            with open(compFile, 'r') as compareFile:
                compStr = compareFile.read()
            compJSON:dict = json.loads(compStr)

            found:bool = False
            for asset in compJSON.items():
                if asset[0] == id:
                    found = True
                    fieldList:list = ['Name', 'Category', 'Model No', 'Remaining', 'Min QTY', 'QTY To Order', 'Order Number']
                    inputtedList:list = [model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order]
                    values:dict = dict(asset[1])
                    # FIXME: Values contain what existed before. But what if this is a new asset and nothing existed before? Then it should bypass asset[0] == id, right?
                    # Maybe the error is that when the asset is created in the comparison log, there's a flaw
                    
                    for field, input in zip(fieldList, inputtedList):
                        if values[field] != input:
                            self.logChange(weeklyLogFile, changeMade, field, id, model, values[field], input)
                            self.updateCompLogAsset(compFile, values, field, input, id, compJSON)
                            changeMade = True
                    break
            if not found:
                # This was created
                self.logCreation(weeklyLogFile, changeMade, id, model, currQty)
                self.createCompLogAsset(compFile, id, model, itemName, productNum, currQty, reorderAtQty, qtyToOrder, order, compJSON)
                changeMade = True
            return changeMade
        except Exception as ex:
            print(f"Compare Asset Error: {ex}")
            self.log(f"Compare Asset Error: {ex}")
            return True

    def createCompLogAsset(self, compFile:Path, id:str, model:str, itemName:str, productNum:str, currQty:str, reorderAtQty:str, qtyToOrder:str, order:str, compJSON:dict) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                # The IDs are the keys, all fields are the values
                fields:dict = {"id": id, "Name": model, "Category": itemName, "Model No": productNum, "Remaining": currQty, "Min QTY": reorderAtQty, "QTY To Order": qtyToOrder, "Order Number": order}
                compJSON[id] = fields
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error creating asset in comparison log: {ex}")
            self.log(f"Error creating asset in comparison log: {ex}")

    def updateCompLogAsset(self, compFile:Path, values:dict, field:str, input:str, id:str, compJSON:dict) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                values[field] = input
                compJSON[id] = values
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error updating asset in comparison log: {ex}")
            self.log(f"Error updating asset in comparison log: {ex}")

    def deleteCompLogAsset(self, compFile:Path, compJSON:dict, removeKey:str) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                compJSON.pop(removeKey)
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error deleting asset in comparison log: {ex}")
            self.log(f"Error deleting asset in comparison log: {ex}")

    def logCreation(self, weeklyLogPath:Path, changeMade:bool, id:str, model:str, qty:str) -> None:
        try:
            logMsg:str = f"\tAsset creation: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset creation for {model}: {ex}")
            self.log(f"Error logging asset creation for {model}: {ex}")

    def logChange(self, weeklyLogPath:Path, changeMade:bool, fieldName:str, id:str, model:str, prev:str, curr:str) -> None:
        try:
            logMsg:str = f"\tAsset change: ID: {id}, Name: {model}\n\t\tPrevious {fieldName}: {prev}, Current {fieldName}: {curr}\n"
            print(logMsg)
            with open (weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset change ({fieldName}) for {model}: {ex}")
            self.log(f"Error logging asset change ({fieldName}) for {model}: {ex}")

    def logDeletion(self, weeklyLogPath:Path, changeMade:bool, id:str, model:str, qty:str) -> None:
        try :
            logMsg:str = f"\tAsset deletion: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)
        except Exception as ex:
            print(f"Error logging asset deletion for {model}: {ex}")
            self.log(f"Error logging asset deletion for {model}: {ex}")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("Manually testing out logger")