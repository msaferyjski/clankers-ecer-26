import time, sys, keyboard, os

from paramiko import SSHClient
from scp import SCPClient
from dotenv import load_dotenv

load_dotenv()

ssh = SSHClient()
ssh.load_system_host_keys()

ip = os.getenv("IP")
port = os.getenv("PORT")
username = os.getenv("USER")
password = os.getenv("PASSWORD")
remote_path = os.getenv("REMOTE_PATH")
execute_path = os.getenv("EXECUTE_PATH")

ssh.connect(ip, port=int(port), username=username, password=password, timeout=3)

scp = SCPClient(ssh.get_transport())
scp.put("src", recursive=True, remote_path=remote_path)
scp.close()

ssh.exec_command(f"python3 {execute_pathc} &")

while True:
    if keyboard.is_pressed('c'):
        ssh.exec_command("pkill python3")
        break

ssh.close()