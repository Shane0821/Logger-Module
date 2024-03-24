import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname( __file__ ), '..', 'component'))

from ILog import LogComponent

logger = LogComponent()
print("Logger Created.")

for i in range(10000):
    logger.write(f"This is a test message. {i}")

logger.stop()
print("Logger stopped.")
logger.write("This is a test message.")
