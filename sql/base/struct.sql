DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` bigint(20) not null auto_increment key,
	`name` varchar(255),
	`pass` varchar(255),
	`email` varchar(255),
	`flags` varchar(255),
	`modes` varchar(255),
	`suspended` varchar(255)
);

DROP TABLE IF EXISTS `channels`;
CREATE TABLE IF NOT EXISTS `channels` (
	`channel` varchar(255),
	`user` varchar(255),
	`flag` enum('n', 'q', 'a', 'o', 'h', 'v', 'b')
);

DROP TABLE IF EXISTS `channelinfo`;
CREATE TABLE IF NOT EXISTS `channelinfo` (
	`name` varchar(255),
	`modes` varchar(255),
	`flags` varchar(255),
	`topic` varchar(2048),
	`welcome` varchar(1024),
	`spamscan` varchar(255),
	`fantasy` varchar(255)
);

DROP TABLE IF EXISTS `vhosts`;
CREATE TABLE IF NOT EXISTS `vhosts` (
	`user` varchar(255),
	`vhost` varchar(255),
	`active` varchar(255)
);

DROP TABLE IF EXISTS `opers`;
CREATE TABLE IF NOT EXISTS `opers` (
	`uid` varchar(9),
	`opertype` varchar(255) NOT NULL DEFAULT 'GlobalOp'
);

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
	`user` varchar(255),
	`text` varchar(2048)
);

DROP TABLE IF EXISTS `online`;
CREATE TABLE IF NOT EXISTS `online` (
	`uid` varchar(9),
	`nick` varchar(255),
	`address` varchar(255),
	`host` varchar(255),
	`username` varchar(255),
    `account` varchar(255)
);

DROP TABLE IF EXISTS `trust`;
CREATE TABLE IF NOT EXISTS `trust` (
	`id` bigint(20) not null auto_increment key,
	`address` varchar(255),
	`limit` varchar(255),
	`timestamp` bigint(20) not null
);

DROP TABLE IF EXISTS `chanlist`;
CREATE TABLE IF NOT EXISTS `chanlist` (
	`uid` varchar(9),
	`channel` varchar(255)
);

DROP TABLE IF EXISTS `memo`;
CREATE TABLE IF NOT EXISTS `memo` (
	`id` bigint(20) not null auto_increment key,
	`user` varchar(255),
	`source` varchar(255),
	`message` varchar(2048)
);

DROP TABLE IF EXISTS `banlist`;
CREATE TABLE IF NOT EXISTS `banlist` (
	`id` bigint(20) not null auto_increment key,
	`channel` varchar(255),
	`ban` varchar(255)
);

DROP TABLE IF EXISTS `suspended`;
CREATE TABLE IF NOT EXISTS `suspended` (
	`id` bigint(20) not null auto_increment key,
	`channel` varchar(255),
	`reason` varchar(255)
);

DROP TABLE IF EXISTS `gateway`;
CREATE TABLE IF NOT EXISTS `gateway` (
	`uid` varchar(9)
);

DROP TABLE IF EXISTS `glines`;
CREATE TABLE IF NOT EXISTS `glines` (
	`id` bigint(20) not null auto_increment key,
	`mask` varchar(255),
	`reason` varchar(255) NOT NULL DEFAULT 'You have been violating network rules',
	`timestamp` bigint(20) not null
);

DROP TABLE IF EXISTS `modules`;
CREATE TABLE IF NOT EXISTS `modules` (
	`id` bigint(20) not null auto_increment key,
	`name` varchar(255),
	`class` varchar(255),
	`oper` int(1) not null default 0,
	`auth` int(1) not null default 0,
	`command` varchar(255),
	`help` varchar(255)
);

DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
	`id` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`channel` varchar(255) not null,
	`sender` varchar(255) not null,
	`action` varchar(25) not null,
	`message` varchar(1024)
);

DROP TABLE IF EXISTS `ircd_opers`;
CREATE TABLE `ircd_opers` (
	`id` bigint(20) NOT NULL auto_increment,
	`username` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
	`hostname` varchar(255) NOT NULL DEFAULT '*@*',
	`type` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS `statistics`;
CREATE TABLE IF NOT EXISTS `statistics` (
	`attribute` varchar(255) not null key,
	`value` varchar(255)
);

INSERT INTO `statistics` (`attribute`, `value`) VALUES ('kicks', '0'),('kills', '0');
