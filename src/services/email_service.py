# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.header import Header

# class EmailService:
#     def __init__(self):
#         self.smtp_server = "smtp.gmail.com"
#         self.smtp_port = 587
#         self.sender_email = "dibyanshu.chatterjee.27@gmail.com"
#         self.password = "zscu ztza rdka mvyu"

#     def send_email_support(self, contact):
#         try:
#             message = MIMEMultipart()
#             message["From"] = str(Header(self.sender_email , 'utf-8')) 
#             message["To"] = str(Header(contact.email, 'utf-8'))  
#             message["Subject"] = str(Header(contact.subject, 'utf-8'))

#             body = f"""
#             New message from: {contact.name}
#             Email: {contact.email}
            
#             Message:
#             {contact.message}
#             """

#             message.attach(MIMEText(body, "plain", 'utf-8'))

#             with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
#                 server.starttls()
#                 server.login(self.sender_email, self.password)
#                 server.send_message(message)

#             return True
#         except Exception as e:
#             print(f"Error sending email: {str(e)}")
#             return False


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "dibyanshu.chatterjee.27@gmail.com"
        self.password = "zscu ztza rdka mvyu"

    def send_email_support(self, contact):
        try:
            message = MIMEMultipart()
            message["From"] = str(Header(self.sender_email, 'utf-8'))
            message["To"] = str(Header(contact.email, 'utf-8'))
            message["Subject"] = str(Header(contact.subject, 'utf-8'))

            # Create body with explicit encoding
            body = f"""
            New message from: {contact.name}
            Email: {contact.email}
            
            Message:
            {contact.message}
            """.strip()  # Remove leading/trailing whitespace

            # Properly encode the body
            message.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                text = message.as_string().encode('utf-8')  # Ensure the entire message is UTF-8 encoded
                server.send_message(message)

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False