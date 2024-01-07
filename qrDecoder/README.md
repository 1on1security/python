## qrDecoder.py
For a given QR code image, decode the URL and submit to VirusTotal for safety rating.<br>
Usage: python script.py path/to/your/qr_code.png<p>

Create .evn file with contents:<br>
VIRUSTOTAL_API_KEY=YOUR_API_KEY_GOES_HERE<p?>

Consult requirements.txt for a list of required Python libraries.
Sample QR codes included.<br>

```
├── dustindecker.png    Sample expected to be clean URL https://dustindecker.com
├── README.md           This file.
├── knownDirty.png      Sample with known malicious URL http://hackingloading157 dot ddns dot net
├── knownDirty2.png     Sample with known malicious URL http://xxfg118 dot ru
├── microsoft.png       Sample expected to be clean URL https://micorosoft.com
├── nist.png            Sample expected to be clean URL https://www.nist.gov/publications/introduction-information-security
├── qrDecode.py         The Python Script
└── sans.png            Sample expected to be clean URL https://sans.edu
```