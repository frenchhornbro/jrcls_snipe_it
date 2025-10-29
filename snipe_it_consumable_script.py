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

if __name__ == '__main__':
    logger:Logger = Logger()
    logger.log("\n", True, True)
    logger.log("START", True)
    
    # Get assets
    handler:HTTPHandler = HTTPHandler()
    currAssetJSON = handler.getAssets()
    assetCreator:AssetCreator = AssetCreator(currAssetJSON)
    assets:list[Asset] = assetCreator.createAssets()

    # Create comparison and weekly log files
    compChangeMade:bool = False
    compLogPath:Path = Path("./comparison/comparison.json")
    if not compLogPath.exists():
        os.makedirs(os.path.dirname(compLogPath), exist_ok=True)
        with open(compLogPath, 'w') as compareFile:
            logger.log("FILE:\tComparison file created")

    weeklyLogPath:Path = Path("./log/weekly-asset-log.txt")
    if not weeklyLogPath.exists():
        os.makedirs(os.path.dirname(weeklyLogPath), exist_ok=True)
        with open(weeklyLogPath, 'w') as compareFile:
            pass

    # Check if any existing assets are under minimum quantity
    for asset in assets:
        if asset.currQty <= asset.reorderAtQty:
            if asset.order == "":
                if (asset.set_order("ORDERED")):
                    logger.log(f"ORDER:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order was placed")
                    emailer:Emailer = Emailer(asset.email_msg())
                    emailer.run()
                    time.sleep(5) # Without this Jira freaks out and can take up to 30 minutes to actually receive the email and run its end of the script
            elif asset.order != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f'UPDATE:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order field was cleared of the following unnecessary text: "{asset.order}"')
        elif asset.order != "":
            if (asset.set_order("")):
                logger.log(f"UPDATE:\tQuantity now acceptable for asset {asset.productNum}, ORDERED tag was removed")

    # Update the weekly log
    currIDs:set = set()
    for asset in assets:
        compChangeMade = compChangeMade or logger.compareAsset(weeklyLogPath, compLogPath, compChangeMade, str(asset.id), asset.model, asset.itemName, asset.productNum, str(asset.currQty), str(asset.reorderAtQty), str(asset.qtyToOrder), asset.order)
        currIDs.add(str(asset.id))

    # Log deleted assets
    if os.path.getsize(compLogPath) != 0: # There will be no deleted assets if the compareFile is empty
        compStr:str = ""
        with open(compLogPath, 'r') as compareFile:
            compStr = compareFile.read()
        compJSON:dict = json.loads(compStr)
        delKeys:list[str] = []
        for oldID in compJSON.keys():
            if not oldID in currIDs:
                asset = compJSON[oldID]
                logger.logDeletion(weeklyLogPath, compChangeMade, oldID, asset['Name'], asset['Remaining'])
                delKeys.append(oldID)
                compChangeMade = True
        for key in delKeys:
            logger.deleteCompLogAsset(compLogPath, compJSON, key)

    if os.path.getsize(weeklyLogPath) == 0:
        with open(weeklyLogPath, 'w') as weeklyLog:
            weeklyLog.write(f"{'{:%a, %b %d, %Y}'.format(datetime.now())}\n")

    if compChangeMade:
        with open(weeklyLogPath, 'a') as weeklyLog:
            weeklyLog.write("\n")

    try:
        # Check the deadline
        dateString:datetime
        with open(weeklyLogPath, 'r') as weeklyLog:
            dateString = weeklyLog.readline().strip()
        weeklyEmailDeadline = datetime.strptime(dateString, '%a, %b %d, %Y') + timedelta(days=7)
        if datetime.now() > weeklyEmailDeadline:
            # If the deadline has passed, compile the weekly asset log and email it to helpdesk@law.byu.edu
            weeklyLogText:list[str] = "Start Date: "
            with open(weeklyLogPath, 'r') as weeklyLog:
                weeklyLogText += weeklyLog.read()
            emailer:Emailer = Emailer(weeklyLogText, "Weekly Consumable Report")
            emailer.run("printersupply@law.byu.edu","helpdesk@law.byu.edu")
            # Delete the weekly asset log
            weeklyLogPath.unlink()
    except Exception as ex:
        print(f"Error checking the deadline to send the weekly log: {ex}")
        logger.log(f"ERROR:\tError checking the deadline to send the weekly log: {ex}")
    
    logger.log("END", True)