#!/usr/bin/env python3

# Imports
from flask import Flask, render_template, url_for, redirect, request, flash
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


    def search_video_id(self, text):
        cur = self.conn.cursor(buffered=True) 
        #text =  '+' + "+".join(text.split())

        try:
            cur.execute(
            """
            SELECT number, title, name, yt_id 
            FROM episodes, guests, appearances, timestamps
            WHERE episodes.episode_id = appearances.episode_id AND guests.guest_id = appearances.guest_id AND timestamps.episode_id = episodes.episode_id AND MATCH(full_text) AGAINST(?) >= 0.5
            ORDER BY MATCH(full_text) AGAINST(?) desc
            LIMIT 25;
            """,
            (text, text,)
            )
            ret = [list(i) for i in cur]
            cur.close()
            return ret

        except mariadb.Error as e:
            print(f"Error 2: {e}")
            cur.close()
            self.conn.close()
            sys.exit(1)
    
    def search_specific_time(self, text, video_number):
        cur = self.conn.cursor(buffered=True) 
        #text =  '+' + "+".join(text.split())

        try:
            cur.execute(
            """
            SELECT number, title, name, yt_id, time
            FROM parts, episodes, guests, appearances
            WHERE parts.episode_id = episodes.episode_id AND episodes.number = ? AND appearances.episode_id = episodes.episode_id AND appearances.guest_id = guests.guest_id
            ORDER BY MATCH(words) AGAINST(?) desc
            LIMIT 15;
            """,
            (video_number, text, text,)
            )
            ret = [list(i) for i in cur]
            cur.close()
            return ret

        except mariadb.Error as e:
            print(f"Error 3: {e}")
            cur.close()
            self.conn.close()
            sys.exit(1)

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
database = Database(USER, PASSWORD, HOST, PORT, DATABASE)

@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == 'POST' and request.form['content'] != '':
        return redirect(f"/{request.form['content']}/")
    else:
        return render_template("index.html")

@app.route("/<text>/", methods = ["POST", "GET"])
def search(text):
    if request.method == "POST" and request.form['content'] != '':
        return  redirect(f"/{request.form['content']}/")
    else:
        results = database.search_video_id(text)
        
        if len(results) == 0:
            flash("No results were found")
            return redirect('/')

        return  render_template("results.html", results=results, text=text, leng=len(results[0]))

@app.route("/<text>/<video_id>/", methods = ["POST", "GET"])
def find_time(text, video_id):
    if request.method == "POST":
        return redirect(f"/{request.form['content']}/")
    else:
        results = database.search_specific_time(text, video_id)
        for i in range(len(results)):
            results[i][4] = math.floor(results[i][4])

        if len(results) == 0:
            flash("No results were found")
            return redirect('/')

        return  render_template("results.html", results=results, text=text, leng=len(results[0]))



### Executing main function
try:

    if __name__ == "__main__":
        app.run(host="0.0.0.0")

except KeyboardInterrupt:
   database.conn.close()
   del database
