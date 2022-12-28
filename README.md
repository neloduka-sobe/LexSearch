# LexSearch


### Introduction

Search engine created using Python3, Flask, MariaDB, Docker, YoutubeAPI, Scrapetube, and Spacy to search for occurrences of specific words in Lex Fridman Podcast, allowing both searches for the episode as well as a timestamp of the quote.

### The goal

This program was created to broaden my understanding of Docker, Flask, MariaDB (especially to determine whether Full-Index Search is adequate for such purpose), official API, and Machine Learning solutions like Spacy.

### Screenshots

![Index search page of the program](https://github.com/neloduka-sobe/LexSearch/blob/f073eb25b1628b7739385a6b0cd86ba32dfb8acd/photos/1.png?raw=true)
Index search page of the program

![Example search results](https://github.com/neloduka-sobe/LexSearch/blob/main/photos/2.png?raw=true)
Example search results

![Example search results with timestamps](https://github.com/neloduka-sobe/LexSearch/blob/main/photos/3.png?raw=true)
Example search results with timestamps

### Setup

Docker is required to setup.

```bash
docker-compose up -d --build
```

Wait for the script to download all data from API and add it to the database. You can track progress via ```bash docker logs webservice```. After the first script finishes, the website should be available on 0.0.0.0:5000.
