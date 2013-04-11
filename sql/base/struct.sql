-- chiruclan.de IRC services
-- Copyright (C) 2012-2013  Chiruclan
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` bigint(20) not null auto_increment key,
	`name` varchar(255) not null,
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
	`name` varchar(255) not null key,
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
	`uid` varchar(9) not null key,
	`opertype` varchar(255) NOT NULL DEFAULT 'GlobalOp'
);

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
	`user` varchar(255),
	`text` varchar(2048)
);

DROP TABLE IF EXISTS `online`;
CREATE TABLE IF NOT EXISTS `online` (
	`uid` varchar(9) not null key,
	`nick` varchar(255) not null,
	`address` varchar(255),
	`host` varchar(255),
	`username` varchar(255),
    `account` varchar(255)
);

DROP TABLE IF EXISTS `metadata`;
CREATE TABLE IF NOT EXISTS `metadata` (
	`uid` VARCHAR(0) NOT NULL,
	`key` VARCHAR(255) NOT NULL,
	`value` VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `trust`;
CREATE TABLE IF NOT EXISTS `trust` (
	`id` bigint(20) not null auto_increment key,
	`address` varchar(255) not null key,
	`limit` varchar(255),
	`timestamp` bigint(20) not null
);

DROP TABLE IF EXISTS `chanlist`;
CREATE TABLE IF NOT EXISTS `chanlist` (
	`uid` varchar(9),
	`channel` varchar(255),
	`flag` enum('', 'v', 'h', 'o', 'a', 'q') NOT NULL DEFAULT ''
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
	`uid` varchar(9) not null key
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
	`help` varchar(255),
	`bot` varchar(6) not null default '0'
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
	`hostname` varchar(255) NOT NULL DEFAULT 'root@localhost',
	`type` varchar(255) NOT NULL DEFAULT 'GlobalOp',
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS `statistics`;
CREATE TABLE IF NOT EXISTS `statistics` (
	`attribute` varchar(255) not null key,
	`value` varchar(255)
);

INSERT INTO `statistics` (`attribute`, `value`) VALUES ('kicks', '0'),('kills', '0');
