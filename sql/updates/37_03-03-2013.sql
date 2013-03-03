DROP TABLE IF EXISTS `ircd_opers`;
CREATE TABLE `ircd_opers` (`id` bigint(20) NOT NULL auto_increment, `username` varchar(255) NOT NULL, `password` varchar(255) NOT NULL, `hostname` varchar(255) NOT NULL DEFAULT '*@*', `type` varchar(255) NOT NULL DEFAULT 'GlobalOp', PRIMARY KEY (id));
ALTER TABLE `opers` ADD COLUMN `opertype` varchar(255) not null default 'GlobalOp';