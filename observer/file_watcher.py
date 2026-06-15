import asyncio
import os
import threading
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from parser.parser_logs import parse_log

from database.db import (
    connect_database,
    disconnect_database,
    create_table,
    insert_rejection
)


def wait_file_complete(path):

    last_size = -1

    while True:

        try:
            current_size = os.path.getsize(path)

            if current_size == last_size:
                return

            last_size = current_size
            time.sleep(1)

        except FileNotFoundError:
            time.sleep(1)


async def save_new_log(path):

    await connect_database()
    await create_table()

    rejection = parse_log(path)

    await insert_rejection(rejection)

    await disconnect_database()


def process_file(path):

    try:
        wait_file_complete(path)

        asyncio.run(save_new_log(path))

        print(f"[WATCHDOG] Novo log processado: {os.path.basename(path)}")

    except Exception as e:
        print(f"[WATCHDOG ERRO] {os.path.basename(path)} -> {e}")


class Handler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return


        if not event.src_path.lower().endswith(".txt"):
            return

        threading.Thread(
            target=process_file,
            args=(event.src_path,),
            daemon=True
        ).start()


def start_watcher(path):

    if not os.path.exists(path):
        print(f"Pasta não encontrada: {path}")
        return

    observer = Observer()

    observer.schedule(
        Handler(),
        path,
        recursive=False
    )

    observer.start()

    print(f"Watchdog ativo monitorando: {path}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

