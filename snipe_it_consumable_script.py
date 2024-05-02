import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from http_handler import HTTPHandler
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer
from logger import Logger

if __name__ == '__main__':
    logger:Logger = Logger()
    handler:HTTPHandler = HTTPHandler()
    assetCreator:AssetCreator = AssetCreator(handler.getAsset())
    assets:list[Asset] = assetCreator.createAssets()
    asset:Asset
    logger.log("\n", True, True)
    logger.log("START", True)

    compChangeMade:bool = False
    compFolderPath:Path = Path("./comparison")
    compLogPath:Path = Path("./comparison/comparison.txt")

    if not compFolderPath.exists():
        compFolderPath.mkdir(parents=True)

    if not compLogPath.exists():
        with open(compLogPath, 'w') as compareFile:
            logger.log("FILE:\tComparison file created")

    weeklyLogFolderPath:Path = Path("./log")
    weeklyLogPath:Path = Path("./log/weekly-asset-log.txt")

    if not weeklyLogFolderPath.exists():
        weeklyLogFolderPath.mkdir(parents=True)

    if not weeklyLogPath.exists():
        with open(weeklyLogPath, 'w') as compareFile:
            pass

    currIDs:dict = {}

    for asset in assets:
        if logger.compareAsset(weeklyLogPath, compLogPath, compChangeMade, str(asset.id), asset.model, asset.itemName, asset.productNum, str(asset.currQty), str(asset.reorderAtQty), str(asset.qtyToOrder), asset.order):
            compChangeMade = True
        currIDs[str(asset.id)] = str(asset.id)
        if asset.currQty <= asset.reorderAtQty:
            if asset.order == "":
                if (asset.set_order("ORDERED")):
                    logger.log(f"ORDER:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order was placed")
                    emailer:Emailer = Emailer(asset.email_msg())
                    emailer.run()
                    time.sleep(5) #Without this Jira freaks out and can take up to 30 minutes to actually receive the email and run its end of the script
            elif asset.order != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f'UPDATE:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order field was cleared of the following unnecessary text: "{asset.order}"')
        elif asset.order != "":
            if (asset.set_order("")):
                logger.log(f"UPDATE:\tQuantity now acceptable for asset {asset.productNum}, ORDERED tag was removed")


    #There will be no deleted assets if the compareFile is empty
    if compLogPath.stat().st_size != 0:
        compStr:str = ""
        with open(compLogPath, 'r') as compareFile:
            compStr = compareFile.read()
        compJSON:dict = json.loads(compStr)

        # Log deleted assets
        delKeys:list[str] = []
        for oldID in compJSON.items():
            if not currIDs.get(oldID[0]):
                logger.logDeletion(weeklyLogPath, compChangeMade, oldID[0], oldID[1]['Name'], oldID[1]['Remaining'])
                delKeys.append(oldID[0])
                compChangeMade = True
        for key in delKeys:
            logger.deleteCompLogAsset(compLogPath, compJSON, key)        

    if weeklyLogPath.stat().st_size == 0:
        with open(weeklyLogPath, 'w') as weeklyLog:
            weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")

    if compChangeMade:
        with open(weeklyLogPath, 'a') as weeklyLog:
            weeklyLog.write("\n")

    try:
        dateString:datetime
        with open(weeklyLogPath, 'r') as weeklyLog:
            dateString = weeklyLog.readline().strip()
        weeklyEmailDeadline = datetime.strptime(dateString, '%a, %b %d, %Y') + timedelta(days=7)

        if datetime.now() >= weeklyEmailDeadline:
            weeklyLogText:list[str] = "Start Date: "
            with open(weeklyLogPath, 'r') as weeklyLog:
                weeklyLogBody = weeklyLog.readline()
                while weeklyLogBody:
                    weeklyLogText += weeklyLogBody
                    weeklyLogBody = weeklyLog.readline()
            emailer:Emailer = Emailer(weeklyLogText, "Weekly Consumable Report")
            emailer.run("printersupply@law.byu.edu","helpdesk@law.byu.edu")
            weeklyLogPath.unlink() #This deletes the file
    except Exception as ex:
        print(f"Error checking the deadline to send the weekly log: {ex}")
        logger.log(f"ERROR:\tError checking the deadline to send the weekly log: {ex}")
    
    logger.log("END", True)