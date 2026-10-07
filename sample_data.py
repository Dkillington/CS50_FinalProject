"""Fictional demonstration data, never represented as YouTube observations."""
import sqlite3
from pathlib import Path


def prepare_database(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return  # A user's database must never be overwritten or mixed with samples.
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE videos (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, title TEXT, views INTEGER, comments INTEGER, dateDay INTEGER, dateMonth INTEGER, dateYear INTEGER, url TEXT)")
        db.execute("CREATE TABLE dataset_metadata (key TEXT PRIMARY KEY, value TEXT)")
        db.execute("INSERT INTO dataset_metadata VALUES ('sample_data', 'true')")
        topics = ['First steps', 'Planning a project', 'Building the interface', 'Working with data', 'Testing the app', 'Finishing touches', 'Behind the scenes', 'A new experiment']
        for channel_index, channel in enumerate(['Sample Dev Diary (demo)', 'Sample Curious Workshop (demo)', 'Sample Game Journal (demo)']):
            for index, topic in enumerate(topics):
                db.execute("INSERT INTO videos (author,title,views,comments,dateDay,dateMonth,dateYear,url) VALUES (?,?,?,?,?,?,?,?)", (channel, f'{topic} — sample video {index + 1}', 800 + (index * 1273) + (channel_index * 431), 12 + index * 17 + channel_index * 9, 1 + index * 3, 3 + channel_index, 2024, '#sample-data'))
