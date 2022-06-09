import subprocess
import os

def kill_process(process_name):
    _subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = _subprocess.communicate()
    for line in output.splitlines():
        if process_name in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)