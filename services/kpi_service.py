from collections import Counter


def calculate_kpis(rows):

    if not rows:
        return {
            "total": 0,
            "top_defect": "-",
            "top_camera": "-",
            "last_rejection": "-"
        }

    total = len(rows)

    defects = Counter()
    cameras = Counter()

    for r in rows:
        defects[r["defect"]] += 1
        cameras[r["camera"]] += 1

    top_defect = defects.most_common(1)[0][0]
    top_camera = cameras.most_common(1)[0][0]
    last_rejection = rows[0]["time"]

    return {
        "total": total,
        "top_defect": top_defect,
        "top_camera": top_camera,
        "last_rejection": last_rejection
    }