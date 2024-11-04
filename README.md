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
