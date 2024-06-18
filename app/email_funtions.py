import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Function to send an email
def send_email(to_email, subject, body):
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")  # Get password from .env
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def send_sms(to_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=to_number
        )
    except Exception as e:
        print(f"Failed to send SMS to {to_number}: {e}")
        raise HTTPException(status_code=500, detail=str(e))