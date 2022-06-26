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
	`guests` set NOT NULL DEFAULT set(),
	/*`episode_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,*/
	`description` text COLLATE utf8mb4_unicode_ci,
	PRIMARY KEY (`episode_id`)
); ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

