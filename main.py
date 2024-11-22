from config import ZAP_URL, TARGET_URL, EMAIL_TO
from login import perform_login
from scan import start_scan
from email_alert import send_email_alert

def main():
    # Perform login
    perform_login()

    # Start ZAP scan
    start_scan(ZAP_URL, TARGET_URL)

    # Send email alert with scan report to multiple recipients
    send_email_alert(["raktim.kakati@vantagecircle.com", "kongkona.das@vantagecircle.com", "subhendu.gogoi@vantagecircle.com", "adin.saikia@vantagecircle.com"])

if __name__ == "__main__":
    main()
