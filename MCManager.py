from MCServerThread import MCServerThread

server_jar_location = 'server.jar'
mc_server_args = ['java', '-Xmx1024M', '-Xms1024M', '-jar', server_jar_location, 'nogui'],

class MCManager:
    def __init__(self):
        self.thread = None
        self._is_running = False

    def StartServer(self):
        if self.thread is None:
            self.thread = MCServerThread('mcserver', '1000')
            self.thread.start()
            return "Server Starting..."

        return "Server already running"