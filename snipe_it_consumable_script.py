import requests
import smtplib  # Simple Mail Transfer Protocol Library
import email.utils
from email.message import EmailMessage
from email.mime.text import MIMEText # Multipurpose Internet Mail Extensions
from asset_creator import AssetCreator
from asset import Asset
from emailer import Emailer

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
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzOTMiLCJqdGkiOiIyMWNmY2ExNzFjZjQ3OGQ1MzY0OTI4Mjk1MjRkY2JkOWQ1NTE4OGVjNTkzOGRlODRhN2YxYTM4Yjc4OGY4M2QwYzcyNmYwOTU1MmM3MWZmNyIsImlhdCI6MTcwOTIzNzAxOCwibmJmIjoxNzA5MjM3MDE4LCJleHAiOjIwMjQ4NTYyMTgsInN1YiI6IjY4MCIsInNjb3BlcyI6W119.gwtsjkWZ30kBVSIObK7fQBpoPdjJkxaxtMr2gBtqeWrQL5gi1u9ZsT4eZkZw0eiGqZkd2oQU4GxbV94bYcf01cSyY9r28gMufou7L1DEABM8fuv_pObsZ8SITKueEO5xF143BTTol-9JXbE3X--BSNYMsYgL6QWPs4q-NsHVPdiEE_nMaQZj5fCWZRYPspCfuvS6D6JG2IOIMZcs7ioueAHfvA_ekW8lj5JUAdiPuQi7hJ3bxVpEADF2RwvPf9gROxVCp2GY_XCLRye-9EIZvwYFJJmJM6906anJB0WooymM7sKC5RahZi43Md59pyi6VZHW71qwBeq9qJNQVV_lDYY64low4jlB7SL77CZcWQt46CANL3acVDSaKA5yndchM2Eir0tOcmWKLGo-EZev4KhUtyVPAWfNOHbZvD4xNqiSMqCaxX8IAA-yDykOXxlxNnUmED6VFxF_L9sj2uq2TKH8d2P3_6yj5XF2ySYDnkwvm2bgA-thy2gSkrXmrlxM8uIJdc_tQD_WRp8ojmyJe4fu6rnWbiM-jR_rOATJZYkwDrFAT6Ri-_mqKk6ms2zqmr4RN05K-uOh5GjNSeCiZWqZwC97DRLhPqLMPT42qLD_vxuKc8A8dhK0g1yn-RRrZzH_E8blpEQQbnjuR6RiJ0QFkPhQ5WmW9LoW37u_Pms"
    }

    response = requests.get(url, headers=headers)
    json_str_input = str(response.text)
    assetCreator:AssetCreator = AssetCreator(json_str_input)
    assets:list[Asset] = assetCreator.createAssets()
    asset: Asset
    for asset in assets:
        if asset.get_current_qty() <= asset.get_reorder_at_qty():
            # TODO: Make sure once an email is sent once for one asset, it isn't sent for the same thing again so long as the status is ordered
            # ^^^ May have to do a PUT request to set something as 1 or 0 (for an ordered status)

            emailer:Emailer = Emailer(asset.email_msg())
            print(asset.email_msg())
            emailer.run()
            # TODO: For some reason the body of the email is blank when the code is run from here, but when it's run from emailer it works just fine. Fix this