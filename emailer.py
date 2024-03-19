import smtplib # Simple Mail Transfer Protocol Library
import ssl
from credential_handler import CredentialHandler
from logger import Logger

class Emailer:
    def __init__(self, body = "Sending a test email") -> None:
        subject = "Supplies Reorder"
        self.msg = "Subject: {}\n\n{}".format(subject, body)
        self.logger:Logger = Logger()

    def run(self, sender_email:str="printersupply@law.byu.edu", receiver_email:str = "helpdesk@byu-law.atlassian.net") -> None:
        port = 465
        smtp_server = 'smtp.gmail.com'
        cred:CredentialHandler = CredentialHandler()
        password = cred.run()
        context = ssl.create_default_context()

        try :
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, [receiver_email], self.msg)
                self.logger.log("Email sent")
                server.quit()
        except Exception as e:
            self.logger.log(f'DARN! Doing this throws an error:\t"{e}"')

if __name__ == '__main__':
    emailer:Emailer = Emailer("Sending a test message via Python")
    emailer.run()