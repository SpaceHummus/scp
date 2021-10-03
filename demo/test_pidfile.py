import pidfile
import time

def is_running():
    try:
        with pidfile.PIDFile():
            print('Process NOT  running.')
            time.sleep(600)
            return False
    except pidfile.AlreadyRunningError:
        print('Process already running.')
        return True

if __name__ == "__main__":
    if is_running():
        quit()
    print("running...")
    time.sleep(600)
