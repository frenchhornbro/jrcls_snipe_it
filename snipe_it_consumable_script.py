import requests
import smtplib  # Simple Mail Transfer Protocol Library
import email.utils
from email.message import EmailMessage
from email.mime.text import MIMEText
from asset_creator import AssetCreator
from asset import Asset

def sendEmail(email_msg:str) -> None:
    email:EmailMessage = EmailMessage()
    email.set_content(email_msg)

    email['Subject'] = "Supplies Reorder"
    email['From'] = "htdurfee@gmail.com"
    email['To'] = "htdurfee@gmail.com"
    print(email_msg)

    print("1")
    server:smtplib.SMTP = smtplib.SMTP()
    print("2")
    server.set_debuglevel(True)
    print("3")
    server.connect('mail.google.com', 25)
    print("4")
    server.send_message(email)
    print("5")
    server.quit()
    print("6")

def testSendEmail(email_msg:str) -> None:
    # Create our message. 
    msg = MIMEText(email_msg)
    msg['To'] = email.utils.formataddr(('Hyrum Law School Account', 'durfeeh@law.byu.edu'))
    msg['From'] = email.utils.formataddr(('Hyrum Personal Account', 'htdurfee@gmail.com'))
    msg['Subject'] = 'Test'

    # --- send the email ---

    # SMTP() is used with normal, unencrypted (non-SSL) email.
    # To send email via an SSL connection, use SMTP_SSL().
    server = smtplib.SMTP()

    # Dump communication with the receiving server straight to to the console.
    server.set_debuglevel(True)  
    
    # Specifying an empty server.connect() statement defaults to ('localhost', 25).
    # Therefore, we specify which mail server we wish to connect to.
    print("BEFORE------------------------------------------------------------------------------------------------------------------------------------")
    # server.connect ('smtp.gmail.com', 587)
    server.connect ('localhost', 25)
    print("AFTER------------------------------------------------------------------------------------------------------------------------------------")

    # Optional login for the receiving mail_server.
    # server.login ('login@example.com', 'Password')

    # 'yourname@yourdomain.com' is our envelope address and specifies the return
    # path for bounced emails.
    try:
        server.sendmail('helpdesk@law.byu.edu', ['durfeeh@law.byu.edu'], msg.as_string())
    finally:
        server.quit()



if __name__ == '__main__':
    url = "https://jrcb-snipe-it.byu.edu/api/v1/consumables"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzOTEiLCJqdGkiOiJjOGI1YTdkODJmZGI5OGI4NTU2NTlhOWRlYjQyZjY3Y2IzZDIxNTU5ZGUzMzIwZmUwM2ZiYjY4NDgzZjYyY2EzMmRjZDNlMzJhOWZmMTRmNyIsImlhdCI6MTcwNzQyNDMzMywibmJmIjoxNzA3NDI0MzMzLCJleHAiOjIwMjMwNDM1MzMsInN1YiI6IjY4MCIsInNjb3BlcyI6W119.iCb2hpoeSBZtbghrDCH6xgozW8LULatiQYWVm7iQWTlQwaQ0oMeyh3UkuUS4mHk1XTzWrwXSVl3-W8L_Dyw1AppNxohk3hh1S1SsLMBlRqKPB12Lx50PFitVB2DuSFGHztRWoA7eBne_7bQheE_dTUpQtOOUw2bOICSF1atJmIOXkuLsGJfMpp-mpbLHJGD_IrkWc9FEZqHkHC972U91cX4a6qhQhdk0J35tIhE-sq0LBcbDDDHJAHs0qZo3w0Hd_I6gB2-hp03XQ_5pNW6Hmu5KxAFrEMGFr2S4xFBfJmnhU6OlGBC7XdEARfocWql7UwJjj0WT8bli28xqYNwzhacXcEhTe6d1wFN4ZiknvS1Ovnfs2UGuaiNoqVpLMTpJdJlh6IabpGSMKZ0XZW2OixC0_lUjNBxh6QlrmatlN8pikAs9-n8s-SwpUOdAiyBBhSkqBCu_A77gpsHLgUE3-pMXVApLoR1uFVvY2Vc0pRxAO58xKDrLkiQzWbLOe2ioZkmIx03b_9PUji40EnWANMsIvHL6d16sXrezM9Pl7Owpiy4IvBr8R1JjVpbO69EnOMcH6z_FtbVuTLoW6dJ96oemDaVXqOzxtzsKNX_DUyQsLZ89197D2v6IozPzhSnCGXM6VunkaRCnUQVyFmI-wh6tmAZuGVS7EPXFM3DA2CM"
    }

    response = requests.get(url, headers=headers)
    json_str_input = str(response.text)
    assetCreator:AssetCreator = AssetCreator(json_str_input)
    assets:list[Asset] = assetCreator.createAssets()
    asset: Asset
    for asset in assets:
        if asset.get_current_qty() <= asset.get_reorder_at_qty():
            testSendEmail(asset.email_msg())



#   main {
#   for each inventory item:
#   	if: currentQty <= reorderAt
#   		email_msg from helpdesk@law.byu.edu to helpdesk@byulaw-atlassian.net
#   }
#   
#   email_msg {
#   	f'Our printer supply for the following model(s) is low:
#   		* Model: {model}, Item Type: {item_name}, Product Number: {product_number}, Quantity to order: {qty_to_order}, The current quantity is: {currenty_qty}'
#   }