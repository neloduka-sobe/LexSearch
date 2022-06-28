use lexsearch;
DROP TABLE IF EXISTS `guests`;
CREATE TABLE `guests` (
	`guest_id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	PRIMARY KEY (`guest_id`)
);


DROP TABLE IF EXISTS `episodes`;
CREATE TABLE `episodes` (
	`episode_id` int(11) NOT NULL AUTO_INCREMENT,
	`number` int(11) NOT NULL,
	`title` varchar(128) NOT NULL COLLATE utf8mb4_unicode_ci,
	`yt_id` char(11) NOT NULL COLLATE utf8mb4_unicode_ci,
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
	`full_text` mediumtext NOT NULL COLLATE utf8mb4_unicode_ci,
	`timestamp` json,
	`last_edit_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`timestamp_id`)
); ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

