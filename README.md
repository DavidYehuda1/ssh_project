# SSH Brute Force Scanner

A Python script for scanning SSH ports and attempting brute-force logins.

## Features

- Pings target to check if it's alive.
- Scans ports to identify open SSH port (default: 22).
- Attempts SSH login using brute-force from specified username and password files.
- Provides an interactive shell upon successful login.

## Requirements

- Python 3.x
- `paramiko`
- `scapy`

## Installation

1. Clone the repository or download the ZIP file.
2. Install the required packages:
   ```bash
   pip install paramiko scapy
   
## Usage

1. Run the script:
   ```bash
   python sshbftcpscan.py
2. Enter the target IP address when prompted.
3. Specify the paths to your username and password files.
4. Follow the prompts to perform the scan and attempt brute-force logins.

## Example files
### Usernames File
    test
    kali
    admin
### Passwords File
    password123
    letmein
    kali
    
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Disclamer

This tool is intended for educational purposes and ethical hacking only. Ensure you have permission to test the target system. Unauthorized access to computer systems is illegal.

## Contact

For questions or support, please reach out to dujovne4@gmail.com
