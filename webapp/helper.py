from datetime import datetime


def parse_date_to_iso(date_str):
    date_str = date_str.replace("/", "-")
    datetime_format = (
        "%d-%m-%Y %H:%i:%s", "%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%S.%fZ")
    for item in datetime_format:
        try:
            dt = datetime.strptime(date_str, item)
            to_iso = dt.isoformat()
            return to_iso
        except (ValueError, TypeError):
            continue

    return ''
