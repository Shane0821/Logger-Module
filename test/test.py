import unittest
 
import os
import sys
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..', 'component'))
from ILog import LogComponent

import time

class TestLogComponent(unittest.TestCase):
    def test_write(self):
        logger = LogComponent()
        logger.clear_logs()

        ts1 = logger.write("This is test message 1.")
        time.sleep(5)
        ts2 = logger.write("This is test message 2.")
        logger.stop()

        expected = f"{ts1.strftime('%H:%M:%S')}: This is test message 1.\n{ts2.strftime('%H:%M:%S')}: This is test message 2.\n"

        with open(f"{logger.path}/log_{ts1.strftime('%Y_%m_%d')}.txt", 'r') as file:
            actual = file.read()
        self.assertEqual(expected, actual)

    def test_stop_with_delay(self):
        logger = LogComponent()
        logger.clear_logs()

        ts1 = logger.write("This is test message 1.")
        time.sleep(5)
        ts2 = logger.write("This is test message 2.")
        logger.stop()
        logger.write("This is test message 3.")
        logger.write("This is test message 4.")

        expected = f"{ts1.strftime('%H:%M:%S')}: This is test message 1.\n{ts2.strftime('%H:%M:%S')}: This is test message 2.\n"

        with open(f"{logger.path}/log_{ts1.strftime('%Y_%m_%d')}.txt", 'r') as file:
            actual = file.read()
        self.assertEqual(expected, actual)
    
    def test_stop_without_delay(self):
        logger = LogComponent()
        logger.clear_logs()

        ts1 = logger.write("This is test message 1.")
        time.sleep(5)
        ts2 = logger.write("This is test message 2.")
        logger.stop(False)
        logger.write("This is test message 3.")
        logger.write("This is test message 4.")

        expected = f"{ts1.strftime('%H:%M:%S')}: This is test message 1.\n{ts2.strftime('%H:%M:%S')}: This is test message 2.\n"

        with open(f"{logger.path}/log_{ts1.strftime('%Y_%m_%d')}.txt", 'r') as file:
            actual = file.read()
        self.assertEqual(expected, actual)

    def test_stop_without_delay_empty(self):
        logger = LogComponent()
        logger.clear_logs()

        for i in range(10000):
            logger.write(f"This is test message {i}.")
        logger.stop(False)

        self.assertTrue(not logger.queue.empty())

    def test_cross_date(self):
        logger = LogComponent()
        logger.clear_logs()

        ts = logger.write("This is test message 1.")

        logger.stop()

        self.assertTrue(os.path.exists(f"{logger.path}/log_{ts.strftime('%Y_%m_%d')}.txt"))

 
if __name__ == '__main__':
    unittest.main()