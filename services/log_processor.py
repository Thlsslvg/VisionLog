from pathlib import Path

from parser.parser_logs import parse_log
from database.db import (
    create_table,
    get_all_filenames,
    insert_rejection
)


async def process_existing_logs(log_folder):
    log_folder = Path(log_folder)

    await create_table()

    if not log_folder.exists():
        print(f"[ERROR] Log folder not found: {log_folder}")
        return

    existing_files = await get_all_filenames()

    for file in log_folder.glob("*.txt"):
        if file.name in existing_files:
            continue

        try:
            rejection = parse_log(file)
            await insert_rejection(rejection)

            print(f"[INIT] Processed: {file.name}")

        except Exception as error:
            print(f"[INIT ERROR] {file.name}: {error}")


async def process_single_log(path):
    await create_table()

    rejection = parse_log(path)

    await insert_rejection(rejection)

    print(f"[WATCHDOG] Processed: {Path(path).name}")