
from MCServerThread import MCServerThread

from queue import Queue

class MCManager:
    def __init__(self, bot):
        self.bot = bot
        self.thread = None
        self._is_running = False
        self._command_queue = []

    def start_server(self):
        if self.thread is None:
            self.thread = MCServerThread(self._command_queue)
            self.thread.start()
            self._is_running = True
            return "Server Starting..."

        return "Server already running"

    def stop_server(self):
        if self.thread and self.thread.is_alive():
            self._command_queue.append("STOP")
            self.thread.join()
            self.thread = None
            self._is_running = False # i dont think i use this
            return "Server Stop command sent"

        return "Server thread not running"

    # def send_command(self, msg):
    #     if self.thread:
    #         self._command_queue.append("SAY")
    #         return "SAY {} command sent".format(msg)
        
    #     return "Server thread not running"

