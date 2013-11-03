

def ssh_call(machine, cmd, user, pword=None):
    '''Using paramiko to avoid giving same password 15 times.
    >>> ssh_call('fs09', 'ls -lh /', 'root', gp('root'))
    '''
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machine, username=user, password=pword)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read()


