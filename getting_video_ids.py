#!/usr/bin/env python3

### Imports
import scrapetube # used to get playlist and videos data
import spacy # used to find Guests names
from youtube_transcript_api import YouTubeTranscriptApi # used to get youtube transcripts
import json # used to create json in order to add it into the database

### Constants
PODCAST_PLAYLIST = "PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4" # Youtube id of playlist containing all podcast episodes
FALSE_POSITIVES_NAMES = ["Black Holes", "Email", "Oumuamua", "Deep Learning", "Carl Sagan", "Wu-Tang Clan", "Comedy"] # False positive recognised guests
PROBLEMATIC_GUESTS = ["Luís and João Batalha", "Dmitry Korkin"] # Guests that are not recognised correctly by spacy

### Setups
npl = spacy.load("en_core_web_sm")
videos = scrapetube.get_playlist(PODCAST_PLAYLIST)


for video in videos:

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
    guests = [] # array containing episode guests

    # if guest is known for being problematic for spacy then use first_part as guest name
    if first_part in PROBLEMATIC_GUESTS:
        guests.append(first_part)
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
            guests.append(first_part)


    # Creating data to be added into timestamps table
    json_text_index = 0 # used to track the id of the character in the timestamp_full_text
    timestamp_json = [] # timestamp jeson to be added to the database
    timestamp_full_text = '' # full text of the podcast to be added to the database

    srt = YouTubeTranscriptApi.get_transcript(yt_id)
    # iterating through every verse of the transcript
    for part in srt:
        timestamp_full_text += (part.get('text') + ' ') # adding new verse to the full text
        dlength= (len(part.get('text')) + 1) # getting the length of the added text

        timestamp_json.append({
            "first_index": json_text_index,
            "last_index": (json_text_index + dlength),
            "start_time": part.get('start')
            })

        json_text_index += dlength


    # ADD DATA TO THE DATABASE TODO

    # printing created vars
    print(f"{yt_id=}")
    print(f"{first_part=}")
    print(f"{second_part=}")
    print(f"{third_part=}")
    print(f"{video_number=}")
    print(f"{yt_title=}")
    print(f"{guests=}")
    print(f"{timestamp_json=}")
    print()

