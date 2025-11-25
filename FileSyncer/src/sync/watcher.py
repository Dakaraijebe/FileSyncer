import os
import time
import threading


class FileWatcher:
    def __init__(self, folder, dispatcher, interval=1.0):
        self.folder = folder
        self.dispatcher = dispatcher
        self.interval = interval
        self.stop_flag = False
        self.last_state = {}

    def start(self):
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_flag = True
        self.thread.join()

    def _loop(self):
        while not self.stop_flag:
            self._scan_folder()
            time.sleep(self.interval)

    def _scan_folder(self):
        current = {}
 
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(path)
                except FileNotFoundError:
                    continue

                current[path] = mtime

                if path not in self.last_state:
                    self.dispatcher.on_created(path)
                else:
                    if mtime != self.last_state[path]:
                        self.dispatcher.on_modified(path)

        for old_path in self.last_state:
            if old_path not in current:
                self.dispatcher.on_deleted(old_path)

        self.last_state = current
