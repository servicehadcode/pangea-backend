import smtplib
import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv
from uuid import uuid4

# Load environment variables at the module level
load_dotenv()

class EmailService:
    def __init__(self):
        # Ensure environment variables are loaded
        if not os.getenv('SMTP_SERVER'):
            load_dotenv()  # Try loading again if not found
            
        self.smtp_server = os.getenv('SMTP_SERVER', '').strip()
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '').strip()
        self.password = os.getenv('EMAIL_PASSWORD', '').replace('\xa0', ' ').strip()
        self.use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
        self.use_ssl = os.getenv('SMTP_USE_SSL', 'False').lower() == 'true'
        self.session_log_file = 'email_sessions.json'
        
        # Get founders' emails and split into list
        founders_email_str = os.getenv('FOUNDERS_EMAIL', '').strip()
        self.founders_emails = [email.strip() for email in founders_email_str.split(',') if email.strip()]

        # Validate required settings
        if not all([self.smtp_server, self.smtp_port, self.sender_email, self.password]):
            raise ValueError("Missing required email configuration. Please check your .env file.")

    def send_confirmation_email(self, contact):
        try:
            if not all([self.smtp_server, self.smtp_port, self.sender_email, self.password]):
                raise ValueError("Email configuration is incomplete")

            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = contact.email
            message["Subject"] = "We've Received Your Message"

            body = (
                f"Dear {contact.name},\n\n"
                "Thank you for reaching out to us. This email confirms that we've received your message.\n\n"
                "We'll review your inquiry and get back to you within 24 hours.\n\n"
                f"For reference, here's a copy of your message:\n"
                f"Subject: {contact.subject}\n"
                f"Message:\n{contact.message}\n\n"
                "Best regards,\nThe Support Team"
            )

            message.attach(MIMEText(body, "plain", "utf-8"))

            print(f"Attempting to send confirmation email using SMTP server: {self.smtp_server}:{self.smtp_port}")
            
            smtp_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
            with smtp_class(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    print("Starting TLS...")
                    server.starttls()
                print(f"Logging in as {self.sender_email}...")
                server.login(self.sender_email, self.password)
                print(f"Sending confirmation email to {contact.email}...")
                server.send_message(message)
                print("Confirmation email sent successfully!")

            self.log_session(contact, success=True, recipient=contact.email, is_confirmation=True)
            return True

        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
            print(f"SMTP Server: {self.smtp_server}")
            print(f"SMTP Port: {self.smtp_port}")
            print(f"Sender Email: {self.sender_email}")
            print(f"Password set: {'Yes' if self.password else 'No'}")
            self.log_session(contact, success=False, recipient=contact.email, is_confirmation=True)
            return False

    def send_email_support(self, contact):
        try:
            if not all([self.smtp_server, self.smtp_port, self.sender_email, self.password]):
                raise ValueError("Email configuration is incomplete")

            print("Starting email send process...")
            print(f"SMTP Server: {self.smtp_server}")
            print(f"SMTP Port: {self.smtp_port}")
            print(f"TLS Enabled: {self.use_tls}")
            print(f"SSL Enabled: {self.use_ssl}")

            # First sanitize all input data
            name = contact.name.replace('\xa0', ' ').strip()
            email = contact.email.replace('\xa0', ' ').strip()
            msg = contact.message.replace('\xa0', ' ').strip()

            print(f"Sanitized inputs - Name: {name}, Email: {email}")

            # Send to founders
            all_founders_success = True
            for recipient_email in self.founders_emails:
                message = MIMEMultipart()
                message["From"] = self.sender_email
                message["To"] = recipient_email
                message["Subject"] = contact.subject

                body = (
                    f"New message from: {name}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{msg}"
                )

                print(f"Creating email body for {recipient_email}...")
                message.attach(MIMEText(body, "plain", "utf-8"))

                smtp_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
                try:
                    print(f"Connecting to SMTP server using {'SSL' if self.use_ssl else 'standard'} connection...")
                    with smtp_class(self.smtp_server, self.smtp_port) as server:
                        if self.use_tls:
                            print("Starting TLS...")
                            server.starttls()
                        
                        print("Attempting login...")
                        server.login(self.sender_email, self.password)
                        
                        print(f"Sending message to {recipient_email}...")
                        server.send_message(message)
                        print(f"Message sent successfully to {recipient_email}!")
                    
                    self.log_session(contact, success=True, recipient=recipient_email)
                except Exception as e:
                    print(f"Failed to send to {recipient_email}: {str(e)}")
                    print(f"SMTP Server: {self.smtp_server}")
                    print(f"SMTP Port: {self.smtp_port}")
                    print(f"Sender Email: {self.sender_email}")
                    print(f"Password set: {'Yes' if self.password else 'No'}")
                    self.log_session(contact, success=False, recipient=recipient_email)
                    all_founders_success = False

            # Send confirmation email to user
            confirmation_success = self.send_confirmation_email(contact)

            # Return True only if both operations succeeded
            return all_founders_success and confirmation_success

        except Exception as e:
            print(f"Detailed error information:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Stack trace: {traceback.format_exc()}")
            return False

    def log_session(self, contact, success=True, recipient=None, is_confirmation=False):
        session_data = {
            "id": str(uuid4()),
            "from_email": self.sender_email,
            "to_email": recipient or contact.email,
            "subject": contact.subject,
            "message": contact.message,
            "time_invoked": datetime.now().isoformat(),
            "status": "success" if success else "failed",
            "type": "confirmation" if is_confirmation else "notification"
        }

        try:
            if os.path.exists(self.session_log_file):
                with open(self.session_log_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"sessions": []}

            data["sessions"].append(session_data)

            with open(self.session_log_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error logging session: {str(e)}")