import os
import time
 
FILE_NAME = "uart_test.py"
MAX_WD_TIME = 600

# check last modify date of a file
# return true if passed the time limit
def last_modified (file_name, time_limit):
    time_last_modified = os.path.getmtime(file_name)
    print(time_last_modified)
    current_time = time.time()
    print(current_time)
    since_last_modified_sec = current_time - time_last_modified
    print(since_last_modified_sec)
    time.sleep(1)
    if since_last_modified_sec < time_limit:
        return False
    else:
        return True


rr = last_modified(FILE_NAME, MAX_WD_TIME)

if rr:
    print("the file reached the time limit. restarting.")
    os.system("sudo reboot")
else:
    print("the file didn't reach the time limit.")

