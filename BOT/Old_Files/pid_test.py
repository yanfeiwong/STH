import os,time
import subprocess
argument = '...'
proc = subprocess.Popen(['python3', 'U_Power.py', argument], shell=True)
time.sleep(3) # <-- There's no time.wait, but time.sleep.
pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.
#pid=os.system('echo "wangyan840" |sudo python U_Power.py&')
print(pid)
#os.system("kill "+str(proc.pid))
proc.terminate()
exit(0)

