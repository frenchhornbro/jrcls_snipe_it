import smtplib
import ssl
from credential_handler import CredentialHandler

class Emailer:
    def __init__(self, msg:str = "Sending a test email") -> None:
        self.body:str = msg

    def run(self) -> None:
        port = 465
        smtp_server = 'smtp.gmail.com'

        sender_email:str = "epicsuperbob123@gmail.com"
        receiver_email:str = "epicsuperbob123@gmail.com"
        cred:CredentialHandler = CredentialHandler()
        password = cred.run()
        subject:str = "Test Subject"

        context = ssl.create_default_context()

        try :
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, [receiver_email], self.body)
                print("Email sent")
        except Exception as e:
            print(f'DARN! Doing this throws an error: "{e}"')

if __name__ == '__main__':
    emailer:Emailer = Emailer("Trying to send a message via Python")
    emailer.run()