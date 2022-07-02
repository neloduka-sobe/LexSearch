use lexsearch;
DROP TABLE IF EXISTS `guests`;
CREATE TABLE `guests` (
	`guest_id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(64) DEFAULT NULL,
	PRIMARY KEY (`guest_id`)
);


DROP TABLE IF EXISTS `episodes`;
CREATE TABLE `episodes` (
	`episode_id` int(11) NOT NULL AUTO_INCREMENT,
	`number` int(11) NOT NULL,
	`title` varchar(128) NOT NULL,
	`yt_id` char(11) NOT NULL,
	`transcript_enabled` tinyint(1) DEFAULT '1',
	`edit_date` timestamp default CURRENT_TIMESTAMP,
	PRIMARY KEY (`episode_id`)
); 

DROP TABLE IF EXISTS `appearances`;
CREATE TABLE `appearances` (
	`appearance_id` int(11) NOT NULL AUTO_INCREMENT,
	`episode_id` int(11) NOT NULL,
	`guest_id` int(11) NOT NULL,	
	PRIMARY KEY (`appearance_id`)
);

DROP TABLE IF EXISTS `timestamps`;
CREATE TABLE `timestamps` (
	`timestamp_id` int(11) NOT NULL AUTO_INCREMENT,
	`episode_id` int(11) NOT NULL,
	`full_text` mediumtext NOT NULL,
	FULLTEXT(`full_text`),
	`last_edit_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`timestamp_id`)
);


DROP TABLE IF EXISTS `parts`;
CREATE TABLE `parts` (
	`part_id` int(11) NOT NULL AUTO_INCREMENT,
	`timestamp_id` int(11) NOT NULL,
	`time` double,
       	`words` text,
	FULLTEXT(`words`),
	PRIMARY KEY(`part_id`)	
)

; ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8;
