import os
from models.rejection import Rejection


def parse_log(path):

    with open(path, "r", encoding="utf-8") as file:
        lines = [
            line.strip()
            for line in file.readlines()
            if line.strip()
        ]

    if len(lines) < 4:
        raise ValueError("Log inválido: menos de 4 linhas")

    camera = lines[0].split(":", 1)[1].strip()
    status = lines[1].split(":", 1)[1].strip()
    defect = lines[2].split(":", 1)[1].strip()
    time = lines[3].split(":", 1)[1].strip()

    filename = os.path.basename(path)

    return Rejection(
        camera,
        status,
        defect,
        time,
        filename
    )