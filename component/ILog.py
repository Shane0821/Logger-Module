import threading
import queue
import datetime
import os
from typing import Optional

class LogComponent:
    """
    This class is responsible for asynchronously logging messages to files.
    It creates a queue to store log messages, a listener thread to write messages to files,
    and provides methods to write messages, stop logging, and finish writing outstanding logs.
    """

    def __init__(self):
        """
        Initializes an instance of AsyncLogger.
        """

        # Queue to store log messages
        self.queue = queue.Queue()

        # Thread to listen to the queue and write to file
        self.listener = threading.Thread(target=self._log)

        self.lock = threading.Lock()
        self.condition = threading.Condition(lock=self.lock)

        # Flag to stop the log
        self.stop_log = False

        # Path to store log files
        self.path = os.path.join(os.path.dirname(__file__), "../logs")

        # Start the listener thread
        self.listener.start()

    def clear_logs(self):
        """
        Clears all the log files.
        """

        for file in os.listdir(self.path):
            file_path = os.path.join(self.path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def write(self, message: str) -> datetime.datetime:
        """
        Writes a log message to the queue.

        Args:
            message (str): The log message to be written.

        Returns:
            datetime.datetime: The timestamp of the log message.
        """
        # Get the current timestamp
        timestamp = datetime.datetime.now()

        # If the log is stopped, do nothing
        if (self.stop_log):
            return timestamp
        
        self.lock.acquire()

        # Put the message in the queue
        self.queue.put((timestamp, message))

        self.condition.notify()

        self.lock.release()

        return timestamp

    def stop(self, finish_writing: Optional[bool] = True):
        """
        Stops the logging process.

        Args:
            finish_writing (bool, optional): Whether to finish writing outstanding logs before stopping.
                Defaults to True.
        """

        self.stop_log = True

        self.queue.put((None, None))

        # Wait for the listener thread to finish
        self.listener.join() 

        # If finish_writing is True, write all the messages in the queue to the file
        if finish_writing:
            self._finish_outstanding_logs()

    def _write_to_file(self, timestamp: datetime.datetime, message: str): 
        """
        Writes a log message to a file.

        Args:
            timestamp (datetime.datetime): The timestamp of the log message.
            message (str): The log message to be written.
        """

        filename_with_timestamp = f"{self.path}/log_{timestamp.strftime('%Y_%m_%d')}.txt"

        # If the file does not exist, create it and write the message   
        if not os.path.exists(filename_with_timestamp):
            with open(filename_with_timestamp, 'w') as file:
                file.write(f"{timestamp.strftime('%H:%M:%S')}: {message}\n")
            return
        
        # If the file exists, append the message
        with open(filename_with_timestamp, 'a') as file:
            file.write(f"{timestamp.strftime('%H:%M:%S')}: {message}\n")

    def _finish_outstanding_logs(self):
        """
        Writes all the outstanding log messages in the queue to files.
        """

        # Write all the messages in the queue to the file
        while not self.queue.empty():
            timestamp, message = self.queue.get()

            if (timestamp == None or message == None):
                continue

            self._write_to_file(timestamp, message)

    def _log(self):
        """
        Listens to the queue and writes log messages to files.
        """

        while True:
            if self.stop_log:
                break

            self.lock.acquire()
        
            if self.queue.empty():
                self.condition.wait()
            
            timestamp, message = self.queue.get()

            self.lock.release()

            if (timestamp == None or message == None):
                continue

            self._write_to_file(timestamp, message)
