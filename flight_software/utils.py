import socket
import time
import logging

def wait_4_dns(max_retires):
    t = time.time()
    while (True):
        try:
            addr = socket.gethostbyname('www.googleapis.com')
            logging.info("Found DNS for www.googleapis.com. IP:%s",addr)
            return True
        except:
            logging.error("DNS not ready yet...")
            time.sleep(1)
        if time.time()-t >= max_retires:
            return False
    

