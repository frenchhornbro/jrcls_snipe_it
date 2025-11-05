import json
import os
from pathlib import Path
from asset import Asset
from logger import Logger
from weekly_reporter import WeeklyReporter

class Comparer:
    def __init__(self, compPath: Path, weeklyReporterPath: Path):
        self.logger = Logger()
        self.weeklyReporter = WeeklyReporter(weeklyReporterPath)
        self.compPath = compPath
        self._createFile()

    def compareAsset(self, changeMade: bool, asset: Asset) -> bool:
        id, model, itemName, productNum, currQty, reorderAtQty, order = str(asset.id), asset.model, asset.itemName, asset.productNum, str(asset.currQty), str(asset.reorderAtQty), asset.order
        try:
            if os.path.getsize(self.compPath) == 0:
                # No compare file, need to create it
                with open(self.compPath, 'w') as compareFile:
                    compareFile.write("{}")

            with open(self.compPath, 'r') as compareFile:
                compStr: str = compareFile.read()
            compJSON: dict = json.loads(compStr)

            if id in compJSON:
                # Asset was not newly created, check for any changes to asset
                fieldList:list = ['Name', 'Category', 'Model No', 'Remaining', 'Min QTY', 'Order Number']
                inputtedList:list = [model, itemName, productNum, currQty, reorderAtQty, order]
                asset:dict = compJSON[id]
                for field, recordedValue in zip(fieldList, inputtedList):
                    if asset[field] != recordedValue:
                        self.weeklyReporter.logChange(changeMade, field, id, model, asset[field], recordedValue)
                        self._updateCompLogAsset(asset, field, recordedValue, id, compJSON)
                        changeMade = True
            else:
                # Asset was newly created
                self.weeklyReporter.logCreation(changeMade, id, model, currQty)
                self._createCompLogAsset(id, model, itemName, productNum, currQty, reorderAtQty, order, compJSON)
                changeMade = True
            return changeMade
        except Exception as ex:
            print(f"Compare Asset Error: {ex}")
            self.logger.log(f"ERROR:\tCompare Asset: {ex}")
            return True
        
        
    def logDeletedAssets(self, currIDs: set[str]) -> bool:
        compChangeMade: bool = False
        if os.path.getsize(self.compPath) != 0: # There will be no deleted assets if the compareFile is empty
            with open(self.compPath, 'r') as compareFile:
                compStr: str = compareFile.read()
            compJSON: dict = json.loads(compStr)
            delKeys: list[str] = []
            for oldID in compJSON.keys():
                if not oldID in currIDs:
                    asset = compJSON[oldID]
                    self.weeklyReporter.logDeletion(compChangeMade, oldID, asset['Name'], asset['Remaining'])
                    delKeys.append(oldID)
                    compChangeMade = True
            for key in delKeys:
                self._deleteCompLogAsset(compJSON, key)
        return compChangeMade

    def _createFile(self):
        if not self.compPath.exists():
            # Create comparison file
            os.makedirs(os.path.dirname(self.compPath), exist_ok=True)
            with open(self.compPath, 'w'):
                self.logger.log("FILE:\tComparison file created")
    
    def _createCompLogAsset(self, id: str, model: str, itemName: str, productNum: str, currQty: str, reorderAtQty: str, order: str, compJSON: dict) -> None:
        try:
            with open(self.compPath, 'w') as compareFile:
                # The IDs are the keys, all fields are the values
                fields: dict = {"id": id, "Name": model, "Category": itemName, "Model No": productNum, "Remaining": currQty, "Min QTY": reorderAtQty, "Order Number": order}
                compJSON[id] = fields
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error creating asset in comparison log: {ex}")
            self.logger.log(f"ERROR:\tError creating asset in comparison log: {ex}")

    def _updateCompLogAsset(self, values: dict, field: str, input: str, id: str, compJSON: dict) -> None:
        try:
            with open(self.compPath, 'w') as compareFile:
                values[field] = input
                compJSON[id] = values
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error updating asset in comparison log: {ex}")
            self.logger.log(f"ERROR:\tError updating asset in comparison log: {ex}")

    def _deleteCompLogAsset(self, compJSON: dict, removeKey: str) -> None:
        try:
            with open(self.compPath, 'w') as compareFile:
                compJSON.pop(removeKey)
                compareFile.write(json.dumps(compJSON))
        except Exception as ex:
            print(f"Error deleting asset in comparison log: {ex}")
            self.logger.log(f"ERROR:\tError deleting asset in comparison log: {ex}")