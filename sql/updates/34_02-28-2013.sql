ALTER TABLE `glines` ADD COLUMN `reason` VARCHAR(255) NOT NULL DEFAULT 'You have been violation network rules' AFTER `mask`;