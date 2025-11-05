import os
from datetime import datetime, timedelta
from pathlib import Path
from logger import Logger

class WeeklyReporter:
    def __init__(self, weeklyReportPath: Path):
        self.logger = Logger()
        self.weeklyReportPath = weeklyReportPath
        self._createFile()

    def logCreation(self, changeMade: bool, id: str, model: str, qty: str) -> None:
        try:
            logMsg: str = f"\tCREATION: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(self.weeklyReportPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset creation for {model}: {ex}")
            self.logger.log(f"ERROR:\tError logging asset creation for {model}: {ex}")

    def logChange(self, changeMade: bool, fieldName: str, id: str, model: str, prev: str, curr: str) -> None:
        try:
            msgSpecification: str =  "CHANGE"
            if fieldName == "Order Number":
                msgSpecification = "ORDER"
            logMsg: str = f"\t{msgSpecification}: ID: {id}, Name: {model}\n\t\t"
            if fieldName == "Order Number":
                if prev == "ORDERED":
                    logMsg += "Shipment received, ORDERED tag cleared"
                else:
                    logMsg += "Order requested, ORDERED tag added"
            else:
                logMsg += f"{fieldName} changed from {prev} to {curr}\n"
            print(logMsg)
            with open (self.weeklyReportPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)

        except Exception as ex:
            print(f"Error logging asset change ({fieldName}) for {model}: {ex}")
            self.logger.log(f"ERROR:\tError logging asset change ({fieldName}) for {model}: {ex}")

    def logDeletion(self, changeMade: bool, id: str, model: str, qty: str) -> None:
        try :
            logMsg: str = f"\tDELETION: ID: {id}, Name: {model}, Quantity: {qty}\n"
            print(logMsg)
            with open(self.weeklyReportPath, 'a') as weeklyLog:
                if not changeMade:
                    weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")
                weeklyLog.write(logMsg)
        except Exception as ex:
            print(f"Error logging asset deletion for {model}: {ex}")
            self.logger.log(f"ERROR:\tError logging asset deletion for {model}: {ex}")

    
    def getEmailDeadline(self) -> None:
        with open(self.weeklyReportPath, 'r') as weeklyLog:
            dateString: datetime = weeklyLog.readline().strip()
        return datetime.strptime(dateString, '%a, %b %d, %Y') + timedelta(days=7)
    
    def getReport(self) -> str:
        with open(self.weeklyReportPath, 'r') as weeklyLog:
            return f"Start Date: {weeklyLog.read()}"
        
    def deleteReport(self) -> None:
        self.weeklyReportPath.unlink()

    def addNewline(self) -> None:
        with open(self.weeklyReportPath, 'a') as weeklyLog:
            weeklyLog.write("\n")

    def _createFile(self) -> None:
        if not self.weeklyReportPath.exists():
            # Create weekly log file
            os.makedirs(os.path.dirname(self.weeklyReportPath), exist_ok=True)
            with open(self.weeklyReportPath, 'w'):
                pass
        if os.path.getsize(self.weeklyReportPath) == 0:
            # Write current date at head of weekly log file
            with open(self.weeklyReportPath, 'w') as weeklyLog:
                weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")