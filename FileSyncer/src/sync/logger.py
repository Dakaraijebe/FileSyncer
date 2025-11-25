import threading
from datetime import datetime

class Logger:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()

    def _write(self, level, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} [{level}] {msg}"

        with self.lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

        print(line)

    def info(self, msg):
        self._write("INFO", msg)

    def error(self, msg):
        self._write("ERROR", msg)
