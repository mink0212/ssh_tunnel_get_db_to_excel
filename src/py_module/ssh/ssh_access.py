from sshtunnel import SSHTunnelForwarder

class SshAccess:
    server = None

    def __init__(self, ssh_config) -> None:
        self.server = SSHTunnelForwarder((
                ssh_config.get_str('SSH_HOSTNAME'),
                22
            ),
            ssh_username=ssh_config.get_str('SSH_USER'),
            ssh_pkey=ssh_config.get_str('SSH_KEYFILE'),
            remote_bind_address=(
                ssh_config.get_str('REMOTE_BIND_ADDRESS'),
                ssh_config.get_int('REMOTE_BIND_PORT')
            ),
            local_bind_address=(
                ssh_config.get_str('LOCAL_BIND_ADDRESS'),
                ssh_config.get_int('LOCAL_BIND_PORT')
        ))

    def ssh_start(self):
        self.server.start()

    def ssh_close(self):
        self.server.stop()
