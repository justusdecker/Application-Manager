import smtplib
from email.mime.text import MIMEText
def send_email(subject = "test", 
               body: str = "This is the content", 
               sender: str = "sender@gmail.com", 
               recipients: list[str] = ["first@gmail.com"], 
               password: str = "pw"):
    msg = MIMEText(body)
    msg |= {'Subject': subject, 'From': sender, 'To': ', '.join(recipients)}
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())

send_email()