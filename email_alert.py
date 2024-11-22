import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import EMAIL_FROM, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_email_alert(to_emails):
    subject = "Security Scan Results"
    body = "The scan has completed. Please find the attached scan report."

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF report
    try:
        with open("zap_scan_report.pdf", "rb") as report_file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(report_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename="zap_scan_report.pdf")
        msg.attach(attachment)
    except FileNotFoundError:
        print("PDF scan report not found. Email will be sent without the report.")

    try:
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
