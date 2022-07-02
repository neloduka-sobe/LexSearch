SELECT number, title, name, time, yt_id
FROM episodes, timestamps, parts, guests, appearances
WHERE 	episodes.episode_id = timestamps.episode_id AND 
	timestamps.timestamp_id = parts.timestamp_id AND 
	guests.guest_id = appearances.guest_id AND 
	appearances.episode_id = episodes.episode_id AND
	episode_id in (select episode_id from parts where MATCH(words) AGAINST(?) >= 0.8)
ORDER BY MATCH(words) AGAINST(?) DESC
LIMIT 30;



select timestamp_id, time from parts where MATCH(words) AGAINST('in this video not only') >= 0.7 ORDER BY MATCH(words) AGAINST('in this video not only') desc limit 50;


SELECT number, title, name, time, yt_id
            FROM episodes, timestamps, parts, guests, appearances
            WHERE episodes.episode_id = timestamps.episode_id AND timestamps.timestamp_id = parts.timestamp_id AND guests.guest_id = appearances.guest_id AND appearances.episode_id = episodes.episode_id   AND MATCH(full_text) AGAINST(?) >= 0.8
            ORDER BY MATCH(words) AGAINST(?) DESC
            LIMIT 30
