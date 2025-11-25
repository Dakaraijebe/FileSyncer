import threading
import queue
import shutil
import os
import hashlib

class WorkerPool:
    def __init__(self, config, logger):
        self.num_workers = config["num_workers"]
        self.verify = config.get("hash_verify", False)
        self.logger = logger
        self.task_queue = queue.Queue()
        self.workers = []

    def start_workers(self):
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop)
            t.daemon = True #vlakno se ukonci pri ukonceni hlavniho procesu
            t.start()
            self.workers.append(t)

        self.logger.info(f"WorkerPool: started {self.num_workers} workers.")

    def stop_workers(self):
  
        for n in range(self.num_workers):
            self.task_queue.put(None)

        for t in self.workers:
            t.join()

        self.logger.info("WorkerPool: all workers stopped.")

    def add_task(self, task):
        self.task_queue.put(task)

    def _worker_loop(self):
        while True:
            task = self.task_queue.get()

            if task is None:
                break  # ukončení

            try:
                t = task["type"]

                if t == "copy":
                    self._do_copy(task)
                elif t == "delete":
                    self._do_delete(task)

            except Exception as e:
                self.logger.error(f"Worker error: {e}")

            finally:
                self.task_queue.task_done()


    def _do_copy(self, task):
        src = task["src"]
        dst = task["dst"]

        # zajisti ,ze slozka existuje
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        shutil.copy2(src, dst)
        self.logger.info(f"[COPY] {src} → {dst}")

        if self.verify:
            if not self._verify_hash(src, dst):
                self.logger.error(f"[HASH MISMATCH] {src} vs {dst}")
            else:
                self.logger.info(f"[VERIFY OK] {src}")

    def _verify_hash(self, a, b):
        return self._hash_file(a) == self._hash_file(b)

    def _hash_file(self, path):
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _do_delete(self, task):
        dst = task["dst"]
        if os.path.exists(dst):
            os.remove(dst)
            self.logger.info(f"[DELETE] {dst}")
