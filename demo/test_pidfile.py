import pidfile
import time
print('Starting process')
try:
    with pidfile.PIDFile():
        print('Process started')
        time.sleep(30)
except pidfile.AlreadyRunningError:
    print('Already running.')

print('Exiting')