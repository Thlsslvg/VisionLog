import asyncio
import os
from parser.parser_logs import parse_log
from database.db import (
    connect_database,
    disconnect_database,
    create_table,
    insert_rejection,
    get_all_filenames
)

from observer.file_watcher import start_watcher


LOG_FOLDER = "logs/log"


async def process_existing_logs():

    await connect_database()
    await create_table()

    existing_files = await get_all_filenames()

    for file in os.listdir(LOG_FOLDER):

        if not file.endswith(".txt"):
            continue

        if file in existing_files:
            continue

        path = os.path.join(LOG_FOLDER, file)

        try:
            rejection = parse_log(path)

            await insert_rejection(rejection)

            print(f"[INIT] Inserido: {file}")

        except Exception as e:
            print(f"[INIT ERRO] {file}: {e}")

    await disconnect_database()


async def main():

    await process_existing_logs()

    start_watcher(LOG_FOLDER)


asyncio.run(main())

