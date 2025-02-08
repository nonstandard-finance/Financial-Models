import boto3
import requests
import brevo_python
from brevo_python import SendSmtpEmail
from brevo_python.rest import ApiException
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from app.core.template import email_otp_template
from app.core.constants import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, EMAIL, BREVO_KEY


# --- AWS SES Configuration ---
# SES_CLIENT = boto3.client(
#     "ses",
#     region_name=REGION,
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY,
# )

# --- Brevo (Sendinblue) Configuration ---
# configuration = brevo_python.Configuration()
# configuration.api_key["api-key"] = BREVO_KEY
# BREVO_API_INSTANCE = brevo_python.TransactionalEmailsApi(
#     brevo_python.ApiClient(configuration)
# )


class EmailService:
    def __init__(self, otp_expiration: int, ses_client=None, sender_email=EMAIL):
        """
        Initializes the EmailService.

        Args:
            ses_client: AWS SES client.
            brevo_api_instance: Brevo API instance.
            sender_email: Sender's email address.
            otp_expiration: OTP expiration time in seconds.
        """
        self.ses_client = ses_client
        self.sender_email = sender_email
        self.otp_expiration = otp_expiration

    def send_email(self, to: str, subject: str, message: str, use_brevo: bool = True):
        """
        Sends an email using either AWS SES or Brevo.

        Args:
            to: Recipient email address.
            subject: Email subject.
            message: Email body (text or HTML).
            use_brevo: If True, use Brevo; otherwise, use AWS SES.
        """
        if use_brevo:
            self._send_email_brevo(to, subject, message)
        else:
            self._send_email_ses(to, subject, message)

    def _send_email_ses(self, to: str, subject: str, message: str):
        """Sends an email using AWS SES."""
        try:
            self.ses_client.send_email(
                Source=self.sender_email,
                Destination={"ToAddresses": [to]},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Html": {"Data": message, "Charset": "UTF-8"}},
                },
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error sending email via SES: {str(e)}")

    def _send_email_brevo(self, to: str, subject: str, message: str):
        """Sends an email using Brevo with a direct HTTP POST request."""
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": BREVO_KEY,  # Use your BREVO_KEY constant here
            "content-type": "application/json",
        }
        payload = {
            "sender": {
                "name": "PoeAI | Notifications",
                "email": self.sender_email,  # Use the sender email from the class
            },
            "to": [
                {"email": to, "name": "Recipient Name"}
            ],  # Customize recipient name as needed
            "subject": subject,
            "htmlContent": message,
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            print(f"Email sent successfully: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending email via Brevo: {e}")

    def send_otp_email(self, to: str, otp_code: str):
        """
        Sends an OTP email with a custom HTML template.

        Args:
            to: Recipient email address.
            otp_code: OTP code to include in the email.
        """
        subject = "Your OTP Code"
        expiration_minutes = self.otp_expiration // 60
        # html_content = f"""
        # <html>
        #     <body>
        #         <h1>Your OTP Code</h1>
        #         <p>Your OTP code is: <strong>{otp_code}</strong></p>
        #         <p>This code will expire in <strong>{expiration_minutes} minutes</strong>.</p>
        #     </body>
        # </html>
        # """
        html_content = email_otp_template(
            otp_code=otp_code, expiration_minutes=expiration_minutes
        )
        self.send_email(to, subject, html_content)
