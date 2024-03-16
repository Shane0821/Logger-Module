import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname( __file__ ), '..', 'component'))

from ILog import LogComponent

logger = LogComponent()
print("Logger Created.")
logger.write("This is a test message.")
time.sleep(5)
logger.write("This is a test message+5.")
logger.stop()
print("Logger stopped.")
logger.write("This is a test message.")
