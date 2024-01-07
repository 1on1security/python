#!/usr/bin/env python3

import os
import paramiko
from concurrent.futures import ThreadPoolExecutor

agents_ile='agents.config'
def ssh_transfer(hostname):
    # SSH parameters
    ssh_user = 'yourSSHusername'
    ssh_port = yourSSHport
    private_key_path = 'yourSSHusernameKey.pem'

    # Local and remote directory paths
    local_directory = f'pathToLocalDirectory/{hostname}'
    remote_directory = '/pathToRemoteDirectory'

    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Adjust the ServerAliveInterval and ServerAliveCountMax
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=ssh_port, username=ssh_user, pkey=paramiko.RSAKey(filename=private_key_path),
                    look_for_keys=False, timeout=10, allow_agent=False, compress=True)

        # Change ownership of /remote directory and contents to ssh user
        stdin, stdout, stderr = ssh.exec_command(f'sudo chown -R {ssh_user}:{ssh_user} {remote_directory}')

        # Wait for the command to complete
        stdout.channel.recv_exit_status()

        # Create local directory if it doesn't exist
        os.makedirs(local_directory, exist_ok=True)

        # Transfer files from remote to local
        with ssh.open_sftp() as sftp:
            files = sftp.listdir(remote_directory)
            for file in files:
                remote_file_path = f'{remote_directory}/{file}'
                local_file_path = f'{local_directory}/{file}'

                # Allocate a pseudo-terminal to prevent disconnects for large files
                with ssh.get_transport().open_channel(kind='session') as channel:
                    channel.get_pty()
                    sftp.getfo(remote_file_path, open(local_file_path, 'wb'), bufsize=32768)

        print(f"Transfer completed for {hostname}")

    except Exception as e:
        print(f"Error transferring files for {hostname}: {e}")

    finally:
        ssh.close()

def main():
    # Read hostnames from file
    with open('agents_file', 'r') as file:
        hostnames = [line.strip() for line in file.readlines()]

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=len(hostnames)) as executor:
        executor.map(ssh_transfer, hostnames)

if __name__ == "__main__":
    main()
