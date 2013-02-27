DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (`channel` varchar(255) not null, `sender` varchar(255) not null, `action` varchar(25) not null, `message` varchar(1024));