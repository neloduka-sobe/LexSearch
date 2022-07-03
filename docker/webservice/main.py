#!/usr/bin/env python3

# Imports
from flask import Flask, render_template, url_for, redirect, request
import mariadb # to connect to the database
import sys
import math


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
            SELECT number, title, name, time, yt_id
            FROM episodes, parts, guests, appearances
            WHERE episodes.episode_id in (select distinct episode_id from timestamps where MATCH(full_text) AGAINST(?) >= 0.9) AND episodes.episode_id = appearances.episode_id AND guests.guest_id = appearances.guest_id AND parts.episode_id = episodes.episode_id AND MATCH(words) AGAINST(?) >= 0.7
            ORDER BY MATCH(words) AGAINST(?) desc
            LIMIT 50;
            """,
            (text,text,text,)
            )
            ret = [list(i) for i in cur]
            cur.close()
            return ret

        except mariadb.Error as e:
            print(f"Error 2: {e}")
            cur.close()
            self.conn.close()
            sys.exit(1)

app = Flask(__name__)

database = Database(USER, PASSWORD, HOST, PORT, DATABASE)

@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(f"/{request.form['content']}")
    else:
        return render_template("index.html")

@app.route("/<text>", methods = ["POST", "GET"])
def search(text):
    if request.method == "POST":
        return  redirect(f"/{request.form['content']}")
    else:
        results = database.search(text)

        for result in results:
            result[3] = math.floor(result[3])

        return  render_template("results.html", results=results)



### Executing main function
try:

    if __name__ == "__main__":
        app.run(host="0.0.0.0")

except KeyboardInterrupt:
   database.conn.close()
   del database
