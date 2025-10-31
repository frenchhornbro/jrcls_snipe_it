import smtplib # Simple Mail Transfer Protocol Library
import ssl
import json
from logger import Logger

class Emailer:
    def __init__(self) -> None:
        self.logger: Logger = Logger()
        with open("./config.json") as config:
            c = json.load(config)
            self.sender_email = c["sender-email"]
            self.password = c["sender-email-app-password"]

    def run(self, header: str, body: str, receiver_email: str) -> None:
        port = 465
        smtp_server = 'smtp.gmail.com'
        context = ssl.create_default_context()
        msg = "Subject: {}\n\n{}".format(header, body)

        try :
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, [receiver_email], msg)
                server.quit()
                self.logger.log(f'EMAIL: Email "{header}" sent to {receiver_email}')
        except Exception as e:
            self.logger.log(f'ERROR:\t"{e}"')

if __name__ == '__main__':
    emailer: Emailer = Emailer()
    emailer.run("Sending a test message via Python SMTP", "This is a test", "helpdesk@law.byu.edu")