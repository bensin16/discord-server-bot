import asyncio
import threading

class MCServerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.process = None
        self.loop = None

    def run(self):
        self.execute(
            ['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar', 'nogui'],
            lambda x: self._stdout_callback(x),
            lambda x: print("STDERR: %s" % x),
        )

    def _stdout_callback(self, x):
        print("STDOUT: %s" % x)
        if "Done" in x.decode():
            print("Done! found lmaooo")
            print("Sending 'help'")
            self.loop.create_task(self._write_to_stream(self.process.stdin, f'help\n'))
            print("help sent")

    def _parse_message(self, val):
        if val == "STOP":
            self._write_to_stream(self.process.stdin, f"help")

    async def _check_message_queue(self):
        while True:
            val = None
            if self.queue.not_empty:
                print("Waiting for message...")
                val = await self.queue.get()
                print("Message recieved: {}".format(val))

            self._parse_message(val)

            if val == "STOP":
                print("stop called")
                self.queue.task_done()
                break

    async def _read_stream(self, stream, cb):
        while True:
            line = await stream.readline()
            if line:
                cb(line)
            else:
                break

    async def _write_to_stream(self, stream, message):
        buf = message.encode()
        
        stream.write(buf)
        await stream.drain()    
        await asyncio.sleep(0.5)

    async def _stream_subprocess(self, cmd, stdout_cb, stderr_cb):  
        self.process = await asyncio.create_subprocess_exec(*cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        await asyncio.wait([
            self._read_stream(self.process.stdout, stdout_cb),
            self._read_stream(self.process.stderr, stderr_cb),
            # self._check_message_queue(),
        ])
        return await self.process.wait()

    def execute(self, cmd, stdout_cb, stderr_cb):  
        self.loop = asyncio.new_event_loop()
        rc = loop.run_until_complete(
            self._stream_subprocess(
                cmd,
                stdout_cb,
                stderr_cb,
        ))
        loop.close()
        return rc