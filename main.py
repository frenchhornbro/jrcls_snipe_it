import time
import json
from datetime import datetime
from pathlib import Path
from comparer import Comparer
from weekly_reporter import WeeklyReporter
from logger import Logger
from http_handler import HTTPHandler
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer

compLogPath: Path = Path("./comparison/comparison.json")
weeklyReportPath: Path = Path("./log/weekly-report.txt")
logger: Logger = Logger()
comparer: Comparer = Comparer(compLogPath, weeklyReportPath)
weeklyReporter: WeeklyReporter = WeeklyReporter(weeklyReportPath)
emailer: Emailer = Emailer()

with open("./config.json") as config:
    c = json.load(config)
    weeklyReportEmail: str = c["weekly-report-email"]
    suppliesReorderEmail: str = c["supplies-reorder-email"]

def getAssets() -> list[Asset]:
    handler: HTTPHandler = HTTPHandler()
    currAssetJSON = handler.getAssets()
    assetCreator: AssetCreator = AssetCreator(currAssetJSON)
    return assetCreator.createAssets()

def checkMinQuantity(assets: list[Asset]) -> None:
    for asset in assets:
        if asset.currQty <= asset.reorderAtQty:
            if asset.order == "":
                if (asset.set_order("ORDERED")):
                    logger.log(f"ORDER:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order was placed")
                    emailer.run("Supplies Reorder", asset.email_msg(), suppliesReorderEmail)
                    time.sleep(5) # Without this Jira freaks out and can take up to 30 minutes to actually receive the email and run its end of the script
            elif asset.order != "ORDERED":
                if (asset.set_order("")):
                    logger.log(f'UPDATE:\tID: {asset.id}, Name: {asset.model}, Model No: {asset.productNum} - Order field was cleared of the following unnecessary text: "{asset.order}"')
        elif asset.order != "":
            if (asset.set_order("")):
                logger.log(f"UPDATE:\tQuantity now acceptable for asset {asset.productNum}, ORDERED tag was removed")

def runComparisons(assets: list[Asset]) -> tuple[set[str], bool]:
    compChangeMade: bool = False
    currIDs: set = set()
    for asset in assets:
        compChangeMade = comparer.compareAsset(compChangeMade, asset) or compChangeMade
        currIDs.add(str(asset.id))
    return currIDs, compChangeMade

def sendWeeklyReport() -> None:
    weeklyReportText = weeklyReporter.getReport()
    emailer.run("Weekly Consumable Report", weeklyReportText, weeklyReportEmail)
    weeklyReporter.deleteReport()

if __name__ == '__main__':
    logger.log("\n", isTitle=True, addNewline=True)
    logger.log("START", isTitle=True)
    assets: list[Asset] = getAssets()
    # Send an email for each asset under minimum quantity
    checkMinQuantity(assets)
    # Update the weekly report with changes or deletions to assets
    currIDs, compChangeMade = runComparisons(assets)
    compChangeMade = comparer.logDeletedAssets(currIDs) or compChangeMade
    if compChangeMade:
        weeklyReporter.addNewline()
    try:
        # If the deadline has passed, compile the weekly report and email it to helpdesk@law.byu.edu
        if datetime.now() > weeklyReporter.getEmailDeadline():
            sendWeeklyReport()
    except Exception as ex:
        print(f"Error checking the deadline to send the weekly report: {ex}")
        logger.log(f"ERROR:\tError checking the deadline to send the weekly report: {ex}")
    logger.log("END", isTitle=True)