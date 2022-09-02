import asyncio
import threading

class MCServerThread(threading.Thread):
    def __init__(self, queue, manager):
        threading.Thread.__init__(self)
        self.queue = queue
        self.manager = manager
        self.loop = None
        self.process = None

    def run(self):
        print(self.execute(
            ['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar', 'nogui'],
            lambda x: self._stdout_callback(x),
            lambda x: print("STDERR: %s" % x),
        ))

    def _stdout_callback(self, x):
        print("STDOUT: %s" % x)
        if "Done" in x.decode():
            self.loop.create_task(self._check_message_queue()) #start up message processing after server has started

    async def _check_message_queue(self):
        while True:
            val = None
            if len(self.queue):
                val = self.queue.pop(0)

            if val == "SAY":
                await self._write_to_stream(self.process.stdin, f'say joe\n')
            elif val == "STOP":
                await self._write_to_stream(self.process.stdin, f'stop\n')
                return

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
        ])
        return await self.process.wait()

    def execute(self, cmd, stdout_cb, stderr_cb):  
        self.loop = asyncio.new_event_loop()
        rc = self.loop.run_until_complete(
            self._stream_subprocess(cmd, stdout_cb, stderr_cb)
        )
        self.loop.close()
        return rc