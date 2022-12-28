#!/usr/bin/env python3

### Imports
import scrapetube  # used to get playlist and videos data
import spacy  # used to find Guests names
from youtube_transcript_api import YouTubeTranscriptApi # used to get youtube transcripts
import mariadb  # used to connect to the mariadb database
import sys  # used to exit when exception occurs

### Constants
PODCAST_PLAYLIST = "PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4"  # Youtube id of playlist containing all podcast episodes
FALSE_POSITIVES_NAMES = ["Black Holes", "Email", "Oumuamua", "Deep Learning", "Carl Sagan", "Wu-Tang Clan", "Comedy"]  # False positive recognised guests
PROBLEMATIC_GUESTS = ["Luís and João Batalha", "Dmitry Korkin"]  # Guests that are not recognised correctly by spacy
BLOCKED_VIDEOS_IDS = ['6ePR2TWYVkI']  # Youtube id's of the videos that are not part of a podcast

### Setups
npl = spacy.load("en_core_web_sm")
videos = scrapetube.get_playlist(PODCAST_PLAYLIST)


for video in videos:
    if video['videoId'] in BLOCKED_VIDEOS_IDS:
        continue

    # getting yt_id and title form playlist
    yt_id = video['videoId']
    yt_title =  video['title']['runs'][0]['text']

    # indexes used for dividing the string
    colon_index = yt_title.find(":")
    pipe_index = yt_title.find("|")
    hash_index = yt_title.find("#")

    # dividing string
    first_part = yt_title[:colon_index].strip()
    second_part = yt_title[colon_index+1:pipe_index].strip()
    third_part = yt_title[pipe_index+1:].strip()
    video_number = yt_title[hash_index+1:].strip()


    '''
    Getting guests of the episode
    Links:
        Name extracting: https://towardsdatascience.com/superior-person-name-recognition-with-pre-built-google-bert-e6215186eae0
        Install: https://github.com/explosion/spaCy/issues/4577
    '''

    # Finding all entities in first_part

    doc = npl(first_part)
    guests = []  # array containing episode guests

    # if guest is known for being problematic for spacy then use first_part as guest name
    if first_part in PROBLEMATIC_GUESTS:
        guests.append(first_part.strip())
    else:

        # if not add all entities in first_part into guests array
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                guests.append(ent.text.replace('&', '').strip())

        # if not guests were found in first_part look for them in second_part
        if guests == []:
            doc = npl(second_part)
            for ent in doc.ents:
                if ent.label_ == "PERSON" and ent.text not in FALSE_POSITIVES_NAMES:
                    guests.append(ent.text.replace('&', '').strip())

        # if guest wasnt found in second_string, this means it is inside first string, but wasn's recognized properly
        if guests == []:
            guests.append(first_part.strip())


    # Creating data to be added into timestamps table
    parts_of_the_text = {}  # parts of the text to be added to the database
    timestamp_full_text = ''  # full text of the podcast to be added to the database
    is_transcript_enabled = 1  # states whether there is a transcript for the episode

    try:
        srt = YouTubeTranscriptApi.get_transcript(yt_id)

    except Exception as e:
        # When youtube_transcripts are disabled
        print(e)
        is_transcript_enabled = 0

    finally:

        # iterating through every verse of the transcript
        i = 0
        for part in srt:
            if i % 2 == 1:
                timestamp_full_text += (" " + part.get('text') + " " + last_text)  # adding new verse to the full text
                parts_of_the_text[last_time] = last_text + ' ' + part.get('text')
            else:
                last_time = part.get('start')
                last_text = part.get('text')
            i += 1




    # connect to MariaDB
    try:
        conn = mariadb.connect(
            user="root",
            password="mypass",
            host="database",
            port=3306,
            database="lexsearch"
        )
    except mariadb.Error as e:
        print(f"Error connecting to database: {e}")
        conn.close()
        sys.exit(1)

    # create database cursor
    cur = conn.cursor(buffered=True)

    # adding episode data to the database
    try:
        cur.execute(
        "INSERT INTO episodes (number,title,yt_id,transcript_enabled) VALUES (?,?,?,?)",
        (video_number, yt_title, yt_id,is_transcript_enabled)
        )
        episode_id = cur.lastrowid
        conn.commit()
        cur.close()

    except mariadb.Error as e:
        print(f"Error 1: {e}")
        conn.close()
        sys.exit(1)




    # checking whether guests are already in the database
    guests_ids = [None for i in guests]  # database ids of the guests
    guests_in_db = [False for i in guests]

    try:
        for index, guest in enumerate(guests):


            cur = conn.cursor(buffered=True)
            cur.execute(
            "SELECT * FROM guests WHERE name=?",
            (guest,)
            )
            conn.commit()

            for result in cur:
                if result:
                    guests_ids[index] = result[0]
                    guests_in_db[index] = True

            cur.fetchall()
            tmp = cur.nextset()
            cur.close()

    except mariadb.Error as e:
        print(f"Error 2: {e}")
        conn.close()
        sys.exit(1)

    # adding guests

    try:
        for index, value in enumerate(guests):
            cur = conn.cursor(buffered=True)

            if not guests_in_db[index]:
                cur.execute(
                "INSERT INTO guests (name) VALUES (?);",
                (value,)
                ) 
                conn.commit()

            # get id of an added guest
            cur.execute(
            "SELECT guest_id FROM guests WHERE name=?;",
            (value,)
            )
            conn.commit()

            for i in cur:
                guests_ids[index] = i[0]

            cur.close()
    except mariadb.Error as e:
        print(f"Error 3: {e}")
        conn.close()
        sys.exit(1)



    print(f"{guests_ids=}")
    print(f"{guests_in_db=}")
    print(f"{timestamp_full_text=}")

    # adding appearances

    try:
        for guest_id in guests_ids:
            cur = conn.cursor(buffered=True)
            cur.execute(
            "INSERT INTO appearances (episode_id, guest_id) VALUES (?,?)",
            (episode_id,guest_id,)
            )
            conn.commit()
            cur.close()

    except mariadb.Error as e:
        print(f"Error 4: {e}")
        conn.close()
        sys.exit(1)

    # adding timestamps

    try:
        if bool(is_transcript_enabled):
            cur = conn.cursor(buffered=True)
            cur.execute(
            "INSERT INTO timestamps (episode_id, full_text) VALUES (?,?)",
            (episode_id, timestamp_full_text,)
            )
            conn.commit()

            # get id of an added timestamp
            cur.execute(
            "SELECT timestamp_id FROM timestamps WHERE episode_id=?;",
            (episode_id,)
            )
            conn.commit()

            for i in cur:
                timestamp_id = i[0]
            cur.close()

    except mariadb.Error as e:
        print(f"Error 5: {e}")
        conn.close()
        sys.exit(1)


    # Adding parts to the parts table

    try:
        if bool(is_transcript_enabled):
            for key, value in parts_of_the_text.items():
                cur = conn.cursor(buffered=True)
                cur.execute(
                "INSERT INTO parts (episode_id, time, words) VALUES (?,?,?)",
                (episode_id, key, value )
                )
                conn.commit()
            cur.close()
    except mariadb.Error as e:
        print(f"Error 6: {e}")
        conn.close()
        sys.exit()

# closing connection with the database
conn.close()
