DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users`(name text, pass text, email text);
DROP TABLE IF EXISTS `channels`;
CREATE TABLE IF NOT EXISTS `channels`(channel text, user text, flag text);
DROP TABLE IF EXISTS `channelinfo`;
CREATE TABLE IF NOT EXISTS `channelinfo`(name text, modes text, flags text, topic text, welcome text);
DROP TABLE IF EXISTS `vhosts`;
CREATE TABLE IF NOT EXISTS `vhosts`(user text, vhost text, active text);
DROP TABLE IF EXISTS `temp_nick`;
CREATE TABLE IF NOT EXISTS `temp_nick`(nick text, user text);
DROP TABLE IF EXISTS `opers`;
CREATE TABLE IF NOT EXISTS `opers`(uid text);
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback`(user text, text text);
DROP TABLE IF EXISTS `online`;
CREATE TABLE IF NOT EXISTS `online` (uid text, nick text, address text, host text);
DROP TABLE IF EXISTS `trust`;
CREATE TABLE IF NOT EXISTS `trust` (address text, `limit` text);
DROP TABLE IF EXISTS `chanlist`;
CREATE TABLE IF NOT EXISTS `chanlist` (uid text, channel text);
DROP TABLE IF EXISTS `memo`;
CREATE TABLE IF NOT EXISTS `memo` (user text, source text, message text);
