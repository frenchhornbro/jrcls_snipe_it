import time
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from http_handler import HTTPHandler
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer
from logger import Logger

logger: Logger = Logger()
compLogPath: Path = Path("./comparison/comparison.json")
weeklyLogPath:Path = Path("./log/weekly-asset-log.txt")

def getAssets() -> list[Asset]:
    handler: HTTPHandler = HTTPHandler()
    currAssetJSON = handler.getAssets()
    assetCreator: AssetCreator = AssetCreator(currAssetJSON)
    return assetCreator.createAssets()

def initCompFile() -> None:
    if not compLogPath.exists():
        # Create comparison file
        os.makedirs(os.path.dirname(compLogPath), exist_ok=True)
        with open(compLogPath, 'w'):
            logger.log("FILE:\tComparison file created")

def initWeeklyLogFile() -> None:
    if not weeklyLogPath.exists():
        # Create weekly log file
        os.makedirs(os.path.dirname(weeklyLogPath), exist_ok=True)
        with open(weeklyLogPath, 'w'):
            pass
    if os.path.getsize(weeklyLogPath) == 0:
        # Write current date at head of weekly log file
        with open(weeklyLogPath, 'w') as weeklyLog:
            weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")

def checkMinQuantity(assets: list[Asset]) -> None:
    for asset in assets:
        if asset.currQty <= asset.reorderAtQty:
            if asset.order == "":
                if (asset.set_order("ORDERED")):
                    logger.log(f"ORDER:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order was placed")
                    emailer: Emailer = Emailer(asset.email_msg())
                    emailer.run()
                    time.sleep(5) # Without this Jira freaks out and can take up to 30 minutes to actually receive the email and run its end of the script
            elif asset.order != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f'UPDATE:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order field was cleared of the following unnecessary text: "{asset.order}"')
        elif asset.order != "":
            if (asset.set_order("")):
                logger.log(f"UPDATE:\tQuantity now acceptable for asset {asset.productNum}, ORDERED tag was removed")

def getCurrIDs(assets: list[Asset]) -> tuple[set[str], bool]:
    compChangeMade: bool = False
    currIDs: set = set()
    for asset in assets:
        compChangeMade = compChangeMade or logger.compareAsset(weeklyLogPath, compLogPath, compChangeMade, str(asset.id), asset.model, asset.itemName, asset.productNum, str(asset.currQty), str(asset.reorderAtQty), str(asset.qtyToOrder), asset.order)
        currIDs.add(str(asset.id))
    return currIDs, compChangeMade

def logDeletedAssets(currIDs: set[str]) -> bool:
    compChangeMade: bool = False
    if os.path.getsize(compLogPath) != 0: # There will be no deleted assets if the compareFile is empty
        with open(compLogPath, 'r') as compareFile:
            compStr: str = compareFile.read()
        compJSON: dict = json.loads(compStr)
        delKeys: list[str] = []
        for oldID in compJSON.keys():
            if not oldID in currIDs:
                asset = compJSON[oldID]
                logger.logDeletion(weeklyLogPath, compChangeMade, oldID, asset['Name'], asset['Remaining'])
                delKeys.append(oldID)
                compChangeMade = True
        for key in delKeys:
            logger.deleteCompLogAsset(compLogPath, compJSON, key)
    return compChangeMade

def getEmailDeadline() -> None:
    with open(weeklyLogPath, 'r') as weeklyLog:
        dateString: datetime = weeklyLog.readline().strip()
    return datetime.strptime(dateString, '%a, %b %d, %Y') + timedelta(days=7)

def emailWeeklyLog() -> None:
    # If the deadline has passed, compile the weekly asset log and email it to helpdesk@law.byu.edu
    with open(weeklyLogPath, 'r') as weeklyLog:
        weeklyLogText: list[str] = f"Start Date: {weeklyLog.read()}"
    emailer: Emailer = Emailer(weeklyLogText, "Weekly Consumable Report")
    emailer.run("printersupply@law.byu.edu","helpdesk@law.byu.edu")
    # Delete the weekly asset log
    weeklyLogPath.unlink()

if __name__ == '__main__':
    logger.log("\n", True, True)
    logger.log("START", True)
    assets: list[Asset] = getAssets()
    # Create comparison and weekly log files
    initCompFile()
    initWeeklyLogFile()
    # Send an email for each asset under minimum quantity
    checkMinQuantity(assets)
    # Update the weekly log with changes or deletions to assets
    currIDs, compChangeMade = getCurrIDs(assets)
    compChangeMade = logDeletedAssets(currIDs) or compChangeMade
    # Add whitespace to log
    if compChangeMade:
        with open(weeklyLogPath, 'a') as weeklyLog:
            weeklyLog.write("\n")
    # Send weekly email
    try:
        if datetime.now() > getEmailDeadline():
            emailWeeklyLog()
    except Exception as ex:
        print(f"Error checking the deadline to send the weekly log: {ex}")
        logger.log(f"ERROR:\tError checking the deadline to send the weekly log: {ex}")
    logger.log("END", True)