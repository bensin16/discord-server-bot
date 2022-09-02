
from MCServerThread import MCServerThread

from queue import Queue

server_jar_location = 'server.jar'
mc_server_args = ['java', '-Xmx1024M', '-Xms1024M', '-jar', server_jar_location, 'nogui'],

class MCManager:
    def __init__(self):
        self.thread = None
        self._is_running = False
        self._command_queue = Queue()

    def StartServer(self):
        if self.thread is None:
            self.thread = MCServerThread(self._command_queue)
            self.thread.start()
            return "Server Starting..."

        return "Server already running"

    def StopServer(self):
        if self.thread and self.thread.is_alive():
            self._command_queue.put("STOP")
            return "Server Stop command sent"

        return "Server thread not running"

