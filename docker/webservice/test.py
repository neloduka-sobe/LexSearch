#!/usr/bin/env python3
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="mypass",
        host="database",
        port=3306,
        database="lexsearch"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
video_number = 1
yt_title = 'abcd'
yt_id = '5qap5aO4i9A'
cur.execute(
        "INSERT INTO episodes (number,title,yt_id) VALUES (?,?,?)",
        (video_number, yt_title, yt_id)
                )
conn.close()
