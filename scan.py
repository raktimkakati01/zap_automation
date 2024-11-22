import requests
import pdfkit
from config import ZAP_API_KEY, ZAP_URL, TARGET_URL

def start_scan(zap_url, target_url):
    session = requests.Session()
    session.params = {"apikey": ZAP_API_KEY}

    try:
        # Start spidering
        print(f"Starting spider for {target_url}...")
        spider_response = session.get(f"{zap_url}/JSON/spider/action/scan/", params={"url": target_url})
        spider_response.raise_for_status()
        spider_id = spider_response.json().get("scan")

        # Wait for spidering to complete
        while True:
            spider_status = session.get(f"{zap_url}/JSON/spider/view/status/", params={"scanId": spider_id}).json()
            progress = spider_status.get("status")
            print(f"Spider Progress: {progress}%")
            if progress == "100":
                break

        print("Spider completed successfully.")

        # Start active scan
        print(f"Starting active scan for {target_url}...")
        ascan_response = session.get(f"{zap_url}/JSON/ascan/action/scan/", params={"url": target_url, "recurse": "true"})
        ascan_response.raise_for_status()
        scan_id = ascan_response.json().get("scan")

        # Wait for active scan to complete
        while True:
            ascan_status = session.get(f"{zap_url}/JSON/ascan/view/status/", params={"scanId": scan_id}).json()
            progress = ascan_status.get("status")
            print(f"Active Scan Progress: {progress}%")
            if progress == "100":
                break

        print("Active scan completed successfully.")

        # Retrieve scan results as HTML
        html_report = session.get(f"{zap_url}/OTHER/core/other/htmlreport/").text
        html_file_path = "zap_scan_report.html"
        pdf_file_path = "zap_scan_report.pdf"

        # Save HTML report
        with open(html_file_path, "w", encoding="utf-8") as report_file:
            report_file.write(html_report)

        # Convert HTML report to PDF
        pdfkit.from_file(html_file_path, pdf_file_path)
        print(f"Scan report saved as {pdf_file_path}.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the scan: {e}")
