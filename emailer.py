import smtplib # Simple Mail Transfer Protocol Library
import ssl
from credential_handler import CredentialHandler

class Emailer:
    def __init__(self, body = "Sending a test email") -> None:
        subject = "Supplies Reorder"
        self.msg = "Subject: {}\n\n{}".format(subject, body)

    def run(self) -> None:
        port = 465
        smtp_server = 'smtp.gmail.com'

        # Change sender_email to helpdesk@law.byu.edu (or other email that we create for this)
        sender_email:str = "epicsuperbob123@gmail.com"

        # Change receiver_email to helpdesk@byu-law.atlassian.net
        receiver_email:str = "epicsuperbob123@gmail.com"
        cred:CredentialHandler = CredentialHandler()
        password = cred.run()

        context = ssl.create_default_context()

        try :
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, [receiver_email], self.msg)
                print("Email sent")
                server.quit()
        except Exception as e:
            print(f'DARN! Doing this throws an error:\n\t"{e}"')

if __name__ == '__main__':
    emailer:Emailer = Emailer("Sending a test message via Python")
    emailer.run()