import os
import time
 
FILE_NAME = "scp_main.log"
MAX_WD_TIME = 300 #5 minutes

# check last modify date of a file
# return true if passed the time limit
def last_modified (file_name, time_limit):
    time_last_modified = os.path.getmtime(file_name)
    current_time = time.time()
    since_last_modified_sec = current_time - time_last_modified
    time.sleep(1)
    if since_last_modified_sec < time_limit:
        return True
    else:
        return False


is_modified = last_modified(FILE_NAME, MAX_WD_TIME)

if not is_modified:
    print("the file reached the time limit. restarting.")
    os.system("sudo reboot")
else:
    print("the file didn't reach the time limit.")

