import os
import smtplib
import imghdr
import json
from email.message import EmailMessage

class Email:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        # f = open(os.getcwd() + '/web_app/config/config.json')
        # jsonData = json.load(f)
        self.senderEmail = os.environ.get('EMAIL_ACCOUNT')
        self.senderPW = os.environ.get('EMAIL_PASSWORD')
        self.getterEmail = os.environ.get('EMAIL_ACCOUNT')

    def send_email(self, userName, subj, fromEmail, body):

        msg = EmailMessage()
        msg['Subject'] = subj
        msg['From'] = self.senderEmail
        msg['To'] = self.getterEmail
        msg.set_content(body)

        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>A message from: """ + userName + """</h1>
                <h1>Contact email: """ + fromEmail + """</h1>
                <p>""" + body + """</p>
                <p style="color:SlateGray;">This is an Email from the SITE!</p>
            </body>
        </html>
        """, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.senderEmail, self.senderPW)
            smtp.send_message(msg)


# if __name__ == '__main__':
#     e = Email()
#     e.send_email('test','test','test')