#!/usr/bin/env python3
#
# Usage: qrDecode.py path_to_QR_image

import sys
import requests
import cv2
from pyzbar.pyzbar import decode

VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"

def decode_qr_code(image_path):
    image = cv2.imread(image_path)
    barcodes = decode(image)

    if barcodes:
        decoded_data = barcodes[0].data.decode("utf-8")
        return decoded_data
    else:
        raise Exception("No QR code found in the image")

def check_safe_links(url):
    virustotal_api_url = "https://www.virustotal.com/vtapi/v2/url/scan"
    virustotal_report_url = "https://www.virustotal.com/vtapi/v2/url/report"

    params = {
        "apikey": VIRUSTOTAL_API_KEY,
        "url": url
    }

    # Submit the URL for scanning
    response = requests.post(virustotal_api_url, data=params)

    if response.status_code == 200:
        scan_result = response.json()
        resource = scan_result.get("resource")

        if resource:
            # Retrieve the scan report
            params = {
                "apikey": VIRUSTOTAL_API_KEY,
                "resource": resource
            }

            response = requests.get(virustotal_report_url, params=params)

            if response.status_code == 200:
                report = response.json()
                positive_engines = report.get("positives", 0)

                if positive_engines == 0:
                    return True  # URL is considered safe if no positive detections
                else:
                    print("VirusTotal detected the URL as unsafe.")
                    print("Scan report:", report)
                    return False
            else:
                print("Failed to retrieve VirusTotal report. Status code:", response.status_code)
    else:
        print("Failed to submit URL to VirusTotal. Status code:", response.status_code)

    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/qr_code.png")
        sys.exit(1)

    qr_code_image_path = sys.argv[1]

    try:
        decoded_data = decode_qr_code(qr_code_image_path)
        print("Decoded URL:", decoded_data)

        is_safe = check_safe_links(decoded_data)
        if is_safe:
            print("The URL is safe.")
        else:
            print("The URL is not safe.")
    except Exception as e:
        print("Error decoding or checking the URL:", str(e))
