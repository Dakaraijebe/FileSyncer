import sys
import os

# pridani src do PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, ROOT)

from sync.worker import WorkerPool
from sync.logger import Logger
import time

config = {
    "num_workers": 2, 
    "hash_verify": False
}

logger = Logger("test_worker.log")
pool = WorkerPool(config, logger)

os.makedirs("test_src", exist_ok=True)
os.makedirs("test_dst", exist_ok=True)

with open("test_src/example.txt", "w", encoding="utf-8") as f:
    f.write("Hello world from Plichtic.\n")

pool.start_workers()

pool.add_task({
    "type": "copy",
    "src": "test_src/example.txt",
    "dst": "test_dst/example.txt"
})

pool.add_task({
    "type": "delete",
    "dst": "test_dst/delete_me.txt"
})

time.sleep(2)

pool.stop_workers()

print("=== TEST COMPLETE ===")
