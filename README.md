# Nmap Scan Automation

This Python script automates a daily security test using Nmap. It scans a specified target IP address, saves the results to a file named with the current date and time.

## Features

- Automated daily security scans using Nmap.
- Results saved to a file with the current date and time.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3

## Usage

1. Clone the repository:

> git clone https://github.com/abdullahguch/nmap-scan-automation.git
> cd nmap-scan-automation

### Schedule the Script

The script is set to run once in every hour. You can customize the schedule by modifying the `schedule.every(60).minutes.do(job)` line in the script.

### Put in the IP Address

You need to put in the IP address you want to run the scan on. You can do that by modifying the `target_ip = "78.142.210.15"` line in the script.

2. Run the script:

> python nmap-scan-automation.py

The script will run an Nmap scan, save the results to a file named with the current date and time.

## Disclaimer

Ensure that you have proper authorization before conducting any security tests. Unauthorized testing is illegal and unethical.

## Contributing

Feel free to use, modify, and extend the code as needed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.