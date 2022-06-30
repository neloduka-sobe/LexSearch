#!/usr/bin/env python3

# Imports
from flask import Flask
import mariadb # to connect to the database
import sys


# Constans
USER = "root"
PASSWORD = "mypass"
HOST = "database"
PORT = 3306
DATABASE = "lexsearch"

class Database:

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        
        # connect to MariaDB
        try:
            self.conn = mariadb.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                database = self.database
            )
        except mariadb.Error as e:
            print(f"Error 1: {e}")
            self.conn.close()
            sys.exit(1)


    def search(self, text):
        cur = self.conn.cursor(buffered=True) 

        try:
            cur.execute(
            """
            SELECT number, title, timestamp
            FROM episodes, timestamps
            WHERE episodes.episode_id = timestamps.episode_id AND MATCH(full_text) AGAINST(?) >= 0.5
            """,
            (text,)
            )
            ret = [i for i in cur]
            cur.close()
            return ret

        except mariadb.Error as e:
            print(f"Error 2: {e}")
            cur.close()
            self.conn.close()
            sys.exit(1)

app = Flask(__name__)

database = Database(USER, PASSWORD, HOST, PORT, DATABASE)

@app.route("/")
def index():
    return "<p>Index site</p>"

@app.route("/search/<text>")
def search(text):
    result = database.search(text)
    return f"<p>Text: {result}</p>"


try:
    if __name__ == "__main__":
        app.run(host="0.0.0.0")
except KeyboardInterrupt:
   conn.close()
