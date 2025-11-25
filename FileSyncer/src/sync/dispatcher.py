import os

class Dispatcher:
    def __init__(self, logger, config, worker_pool):
        self.logger = logger
        self.config = config
        self.worker_pool = worker_pool
        self.source = config["source_folder"]
        self.target = config["target_folder"]


    def _map_target_path(self, src_path):
        rel = os.path.relpath(src_path, self.source)
        return os.path.join(self.target, rel)

    def on_created(self, path):
        dst = self._map_target_path(path)
        self.logger.info(f"[CREATE] {path}")
        self._copy_task(path, dst)

    def on_modified(self, path):
        dst = self._map_target_path(path)
        self.logger.info(f"[MODIFY] {path}")
        self._copy_task(path, dst)

    def on_deleted(self, path):
        dst = self._map_target_path(path)
        self.logger.info(f"[DELETE] {path}")
        self._delete_task(dst)

    def _copy_task(self, src, dst):
        self.worker_pool.add_task({
            "type": "copy",
            "src": src,
            "dst": dst
        })

    def _delete_task(self, dst):
        service.worker_pool.add_task({
            "type": "delete",
            "dst": dst
        })