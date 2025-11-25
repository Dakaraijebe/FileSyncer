import threading
from sync.config import load_config
from sync.logger import Logger
from sync.watcher import FileWatcher
from sync.dispatcher import Dispatcher
from sync.worker import WorkerPool

class SyncService:
    def __init__(self):
        self.config = load_config()
        self.logger = Logger(self.config["log_file"])
        self.worker_pool = WorkerPool(self.config, self.logger)
        self.dispatcher = Dispatcher(self.logger, self.config, self.worker_pool)
        self.dispatcher = Dispatcher(self.logger, self.config, self.worker_pool)
        self.watcher = FileWatcher(self.config["source_folder"], self.dispatcher)


    def start(self):
        self.logger.info("Starting FileSyncer...")
        self.worker_pool.start_workers()
        self.watcher.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.logger.info("Stopping FileSyncer...")
            self.watcher.stop()
            self.worker_pool.stop_workers()
            self.logger.info("Shutdown complete.")
