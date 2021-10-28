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

def test():
    print(1)
    try:
        print(2)
        n=90/0
    except:
        pass
    finally:
        print(3)
    print(4)


if __name__ == "__main__":
    test()
    # if is_running():
    #     quit()
    # print("running...")
    # time.sleep(600)
