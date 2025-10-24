import smtplib # Simple Mail Transfer Protocol Library
import ssl
import json
from logger import Logger

class Emailer:
    def __init__(self, body = "Sending a test email", subject = "Supplies Reorder") -> None:
        self.header = subject
        self.msg = "Subject: {}\n\n{}".format(subject, body)
        self.logger:Logger = Logger()
        with open("./config.json") as config:
            self.password = json.load(config)["app-password"]

    def run(self, sender_email:str="printersupply@law.byu.edu", receiver_email:str = "helpdesk@byu-law.atlassian.net") -> None:
        port = 465
        smtp_server = 'smtp.gmail.com'
        context = ssl.create_default_context()

        try :
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, self.password)
                server.sendmail(sender_email, [receiver_email], self.msg)
                server.quit()
                self.logger.log(f'EMAIL: Email "{self.header}" sent to {receiver_email}')
        except Exception as e:
            self.logger.log(f'ERROR:\t"{e}"')

if __name__ == '__main__':
    emailer:Emailer = Emailer("Sending a test message via Python")
    emailer.run()