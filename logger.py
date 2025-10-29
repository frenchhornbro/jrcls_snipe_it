import json
from datetime import datetime
import os
from pathlib import Path

class Logger:
    def __init__(self) -> None:
        self.fileName = ""
        logFolder:Path = Path("./log")
        os.makedirs(logFolder, exist_ok=True)
        self.logFile:Path = Path("./log/log.txt")       #need to cd to this directory in the bat file for this to work

    def log(self, input, title:bool=False, newline:bool=False) -> None:
        input = str(input)
        with open(self.logFile, 'a') as fileWriter:     #this is in append mode
            if (not newline):
                fileWriter.write('{:%Y-%b-%d %H:%M:%S}'.format(datetime.now()))
                fileWriter.write("\t")
            if (not title): fileWriter.write("\t")
            fileWriter.write(input)
            fileWriter.write("\n")

    def compareAsset(self, weeklyLogFile:Path, compFile:Path, changeMade:bool, id:str, model:str, itemName:str, productNum:str, currQty:str, reorderAtQty:str, qtyToOrder:str, order:str) -> bool:
        try:
            if os.path.getsize(compFile) == 0:
                # No compare file, need to create it
                with open(compFile, 'w') as compareFile:
                    compareFile.write("{}")

            compStr:str = ""
            with open(compFile, 'r') as compareFile:
                compStr = compareFile.read()
            compJSON:dict = json.loads(compStr)

            if id in compJSON:
                # Asset was not newly created, check for any changes to asset
                fieldList:list = ['Name', 'Category', 'Model No', 'Remaining', 'Min QTY', 'Order Number']
                inputtedList:list = [model, itemName, productNum, currQty, reorderAtQty, order]
                asset:dict = compJSON[id]
                for field, recordedValue in zip(fieldList, inputtedList):
                    if asset[field] != recordedValue:
                        self.logChange(weeklyLogFile, changeMade, field, id, model, asset[field], recordedValue)
                        self.updateCompLogAsset(compFile, asset, field, recordedValue, id, compJSON)
                        changeMade = True
            else:
                # Asset was newly created
                self.logCreation(weeklyLogFile, changeMade, id, model, currQty)
                self.createCompLogAsset(compFile, id, model, itemName, productNum, currQty, reorderAtQty, order, compJSON)
                changeMade = True
            return changeMade
        except Exception as ex:
            print(f"Compare Asset Error: {ex}")
            self.log(f"ERROR:\tCompare Asset: {ex}")
            return True

    def createCompLogAsset(self, compFile:Path, id:str, model:str, itemName:str, productNum:str, currQty:str, reorderAtQty:str, order:str, compJSON:dict) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                # The IDs are the keys, all fields are the values
                fields:dict = {"id": id, "Name": model, "Category": itemName, "Model No": productNum, "Remaining": currQty, "Min QTY": reorderAtQty, "Order Number": order}
                compJSON[id] = fields
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error creating asset in comparison log: {ex}")
            self.log(f"ERROR:\tError creating asset in comparison log: {ex}")

    def updateCompLogAsset(self, compFile:Path, values:dict, field:str, input:str, id:str, compJSON:dict) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                values[field] = input
                compJSON[id] = values
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error updating asset in comparison log: {ex}")
            self.log(f"ERROR:\tError updating asset in comparison log: {ex}")

    def deleteCompLogAsset(self, compFile:Path, compJSON:dict, removeKey:str) -> None:
        try:
            with open(compFile, 'w') as compareFile:
                compJSON.pop(removeKey)
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error deleting asset in comparison log: {ex}")
            self.log(f"ERROR:\tError deleting asset in comparison log: {ex}")

    def logCreation(self, weeklyLogPath:Path, changeMade:bool, id:str, model:str, qty:str) -> None:
        try:
            logMsg:str = f"\tCREATION: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset creation for {model}: {ex}")
            self.log(f"ERROR:\tError logging asset creation for {model}: {ex}")

    def logChange(self, weeklyLogPath:Path, changeMade:bool, fieldName:str, id:str, model:str, prev:str, curr:str) -> None:
        try:
            msgSpecification:str =  "CHANGE"
            if fieldName == "Order Number":
                msgSpecification = "ORDER"
            logMsg:str = f"\t{msgSpecification}: ID: {id}, Name: {model}\n\t\t"
            if fieldName == "Order Number":
                if prev == "ORDERED":
                    logMsg += "Shipment received, ORDERED tag cleared"
                else:
                    logMsg += "Order requested, ORDERED tag added"
            else:
                logMsg += f"{fieldName} changed from {prev} to {curr}\n"
            print(logMsg)
            with open (weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset change ({fieldName}) for {model}: {ex}")
            self.log(f"ERROR:\tError logging asset change ({fieldName}) for {model}: {ex}")

    def logDeletion(self, weeklyLogPath:Path, changeMade:bool, id:str, model:str, qty:str) -> None:
        try :
            logMsg:str = f"\tDELETION: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(weeklyLogPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)
        except Exception as ex:
            print(f"Error logging asset deletion for {model}: {ex}")
            self.log(f"ERROR:\tError logging asset deletion for {model}: {ex}")

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("TEST:\tManually testing out logger", True)