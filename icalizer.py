import csv
import icalendar
from uuid import uuid4 as uuid
from datetime import datetime
from os import listdir, mkdir
from pathlib import Path
from shutil import rmtree


def time_conversion(date, time):
    try:
        day, month, year = date.split('.')
        hour, minute, second = time.split(':')
    except:
        raise

    return datetime(int(year), int(month), int(day), int(hour), int(minute))


def icalize(filepath):
    with open(filepath, newline='') as csv_file:
        r = csv.reader(csv_file)
        rows = list()
        for row in r:
            rows.append(row)

    cal = icalendar.Calendar()
    cal.add('prodid', '-//D&A Kalender//')
    cal.add('version', '2.0')

    header_row = rows.pop(0)
    rows_clean = [row for row in rows if len(row) == 10]
    rows_unclean = [row for row in rows if len(row) != 10]
    rows_cleanable = [row for row in rows_unclean if len(row) == 9]
    [row.append('') for row in rows_cleanable]
    rows_cleaned = rows_cleanable
    rows = rows_clean + rows_cleaned

    for row in rows:
        event = icalendar.Event()

        event.add('summary', row[0])
        event.add('description', row[8])
        event.add('uid', uuid())
        event.add('dtstamp', icalendar.vDatetime(time_conversion(row[1], row[2])))
        event.add('dtstart', icalendar.vDatetime(time_conversion(row[1], row[2])))
        event.add('dtend', icalendar.vDatetime(time_conversion(row[3], row[4])))

        cal.add_component(event)

    return cal.to_ical()


if __name__ == '__main__':
    in_files = listdir('in/')
    assert all([Path('in/' + file_name).is_file() for file_name in in_files]), 'Only in allowed as input'
    assert all([Path('in/' + file_name).suffix.lower() == '.csv' for file_name in in_files]), 'Only in with ".csv" suffix allowed as input'
    try:
        rmtree('out/')
        mkdir('out/')
    except:
        pass

    for fn in in_files:
        fp = f'in/{fn}'
        cal_string = icalize(fp)
        with open( Path('out') / (Path(fp).stem + '.ics'), 'wb') as file:
            file.write(cal_string)
