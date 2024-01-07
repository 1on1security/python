# threadPoolSCP

Tired of using that old "FOR" loop to sequentially download or rsync with a large number of remote hosts?<br>
Presumes you have PKI and/or trusted certificate or other automated means of authentication in place already.<br>

Edit "agents.config" to include a list of hosts, one per line.  Modify the following in threadPoolsSCP.py
- ssh_user = 'yourSSHusername'
- ssh_port = yourSSHport
- private_key_path = 'yourSSHusernameKey.pem'
- local_directory = f'pathToLocalDirectory/{hostname}'
- remote_directory = '/pathToRemoteDirectory'

