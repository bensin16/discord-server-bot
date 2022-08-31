import asyncio
import threading

class MCServerThread(threading.Thread):
    def __init__(self, thread_name, thread_id):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id

    def run(self):
        print(self.execute(
            ['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar', 'nogui'],
            lambda x: print("STDOUT: %s" % x), # use this to define how we will process stdout from server
            lambda x: print("STDERR: %s" % x),
        ))

    async def _read_stream(self, stream, cb):  
        while True:
            line = await stream.readline()
            if line:
                cb(line)
            else:
                break

    async def _stream_subprocess(self, cmd, stdout_cb, stderr_cb):  
        process = await asyncio.create_subprocess_exec(*cmd,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        await asyncio.wait([
            self._read_stream(process.stdout, stdout_cb),
            self._read_stream(process.stderr, stderr_cb)
        ])
        return await process.wait()


    def execute(self, cmd, stdout_cb, stderr_cb):  
        loop = asyncio.new_event_loop()
        rc = loop.run_until_complete(
            self._stream_subprocess(
                cmd,
                stdout_cb,
                stderr_cb,
        ))
        loop.close()
        return rc