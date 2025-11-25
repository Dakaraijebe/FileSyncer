# FileSyncer

Jednoduchý Python nástroj pro automatickou synchronizaci dvou složek.  
Sleduje změny ve `source` a podle nich aktualizuje `backup`.  
Projekt vznikl jako školní práce na SPŠE Ječná (2025).

---

## Funkce
- detekce vytvoření, úpravy a smazání souborů
- paralelní zpracování pomocí worker threadů
- bezpečné logování
- podpora hash kontroly (SHA-256)
- konfigurovatelné chování přes `config.json`

---

## Struktura projektu
src/
main.py
  sync/
    sync_service.py
    worker.py
    watcher.py
    dispatcher.py
    logger.py
    config.py
bin/
  run.cmd
config.json

---

## Konfigurace (`config.json`)
{
  "source_folder": "source",
  "target_folder": "backup",
  "num_workers": 3,
  "log_file": "sync.log",
  "hash_verify": false,
  "ignore_patterns": []
}
Spuštění
Windows
  bin/run.cmd
Program vyžaduje Python 3.x.

Jak to funguje
Watcher skenuje složku.

Dispatcher vytváří úkoly podle změn.

WorkerPool paralelně provádí kopírování/mazání.

Logger zaznamenává průběh.
