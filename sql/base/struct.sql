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

-- ----------------------------
-- Table structure for banlist
-- ----------------------------
DROP TABLE IF EXISTS "banlist";
CREATE TABLE "banlist" (
"id" bigserial NOT NULL PRIMARY KEY,
"channel" varchar(255) COLLATE "default" NOT NULL,
"ban" varchar(255) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for chanlist
-- ----------------------------
DROP TABLE IF EXISTS "chanlist";
CREATE TABLE "chanlist" (
"uid" varchar(9) COLLATE "default" NOT NULL,
"channel" varchar(255) COLLATE "default" NOT NULL,
"flag" varchar(255) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for channelinfo
-- ----------------------------
DROP TABLE IF EXISTS "channelinfo";
CREATE TABLE "channelinfo" (
"name" varchar(255) COLLATE "default" NOT NULL PRIMARY KEY,
"modes" varchar(255) COLLATE "default",
"flags" varchar(255) COLLATE "default",
"topic" varchar(2048) COLLATE "default",
"welcome" varchar(1024) COLLATE "default",
"spamscan" varchar(255) COLLATE "default",
"fantasy" varchar(255) COLLATE "default"
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for chanrequest
-- ----------------------------
DROP TABLE IF EXISTS "chanrequest";
CREATE TABLE "chanrequest" (
"channel" varchar(65) COLLATE "default" NOT NULL PRIMARY KEY,
"account" varchar(32) COLLATE "default" NOT NULL,
"succeed" int4 NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for channels
-- ----------------------------
DROP TABLE IF EXISTS "channels";
CREATE TABLE "channels" (
"channel" varchar(255) COLLATE "default" NOT NULL,
"user" varchar(255) COLLATE "default" NOT NULL,
"flag" varchar(255) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for feedback
-- ----------------------------
DROP TABLE IF EXISTS "feedback";
CREATE TABLE "feedback" (
"user" varchar(255) COLLATE "default" NOT NULL PRIMARY KEY,
"text" varchar(2048) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for glines
-- ----------------------------
DROP TABLE IF EXISTS "glines";
CREATE TABLE "glines" (
"id" serial NOT NULL PRIMARY KEY,
"mask" varchar(255) COLLATE "default" NOT NULL,
"reason" varchar(240) COLLATE "default" NOT NULL,
"timestamp" int4 NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for ircd_opers
-- ----------------------------
DROP TABLE IF EXISTS "ircd_opers";
CREATE TABLE "ircd_opers" (
"id" serial NOT NULL PRIMARY KEY,
"username" varchar(255) COLLATE "default" NOT NULL,
"password" varchar(255) COLLATE "default" NOT NULL,
"hostname" varchar(255) COLLATE "default" NOT NULL,
"type" varchar(255) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for memo
-- ----------------------------
DROP TABLE IF EXISTS "memo";
CREATE TABLE "memo" (
"id" bigserial NOT NULL PRIMARY KEY,
"recipient" varchar(32) COLLATE "default" NOT NULL,
"sender" varchar(32) COLLATE "default" NOT NULL,
"subject" varchar(64) COLLATE default NOT NULL,
"message" varchar(2048) COLLATE "default" NOT NULL,
"read_state" boolean NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for metadata
-- ----------------------------
DROP TABLE IF EXISTS "metadata";
CREATE TABLE "metadata" (
"uid" varchar(9) COLLATE "default" NOT NULL PRIMARY KEY,
"key" varchar(32) COLLATE "default" NOT NULL,
"value" varchar(128) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for modules
-- ----------------------------
DROP TABLE IF EXISTS "modules";
CREATE TABLE "modules" (
"id" serial NOT NULL PRIMARY KEY,
"name" varchar(255) COLLATE "default",
"class" varchar(255) COLLATE "default",
"command" varchar(255) COLLATE "default",
"help" varchar(255) COLLATE "default",
"bot" varchar(6) COLLATE "default" NOT NULL,
"oper" numeric(1) NOT NULL,
"auth" numeric(1) NOT NULL,
"fantasy" numeric(1) NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for online
-- ----------------------------
DROP TABLE IF EXISTS "online";
CREATE TABLE "online" (
"uid" varchar(9) COLLATE "default" NOT NULL PRIMARY KEY,
"nick" varchar(32) COLLATE "default" NOT NULL,
"address" varchar(38) COLLATE "default" NOT NULL,
"host" varchar(64) COLLATE "default" NOT NULL,
"username" varchar(16) COLLATE "default" NOT NULL,
"gateway" numeric(1) NOT NULL DEFAULT 0,
"account" varchar(32) COLLATE "default",
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for opers
-- ----------------------------
DROP TABLE IF EXISTS "opers";
CREATE TABLE "opers" (
"uid" varchar(9) COLLATE "default" NOT NULL PRIMARY KEY,
"opertype" varchar(255) COLLATE "default" NOT NULL
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for statistics
-- ----------------------------
DROP TABLE IF EXISTS "statistics";
CREATE TABLE "statistics" (
"attribute" varchar(255) COLLATE "default" NOT NULL PRIMARY KEY,
"value" varchar(255) COLLATE "default"
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for suspended
-- ----------------------------
DROP TABLE IF EXISTS "suspended";
CREATE TABLE "suspended" (
"id" serial NOT NULL PRIMARY KEY,
"channel" varchar(65) COLLATE "default" NOT NULL,
"reason" varchar(120) COLLATE "default"
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "users";
CREATE TABLE "users" (
"id" serial NOT NULL PRIMARY KEY,
"name" varchar(32) COLLATE "default" NOT NULL,
"pass" varchar(255) COLLATE "default" NOT NULL,
"email" varchar(64) COLLATE "default" NOT NULL,
"flags" varchar(32) COLLATE "default",
"modes" varchar(16) COLLATE "default",
"suspended" varchar(120) COLLATE "default"
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for vhosts
-- ----------------------------
DROP TABLE IF EXISTS "vhosts";
CREATE TABLE "vhosts" (
"user" varchar(255) COLLATE "default" NOT NULL PRIMARY KEY,
"vhost" varchar(255) COLLATE "default",
"active" numeric(1) NOT NULL DEFAULT 0
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for trust
-- ----------------------------
CREATE TABLE "trust" (
"id" serial NOT NULL PRIMARY KEY,
"address" varchar(255) COLLATE "default" NOT NULL,
"limit" varchar(16) COLLATE "default" NOT NULL,
"timestamp" int4 NOT NULL,
) WITH (OIDS=FALSE);

-- ----------------------------
-- Table structure for botchannel
-- ----------------------------
CREATE TABLE "botchannel" (
"bot" numeric(6) NOT NULL,
"channel" varchar(64) NOT NULL
) WITH (OIDS=FALSE);

INSERT INTO "statistics" ("attribute", "value") VALUES
  ('kicks', '0'),
  ('kills', '0');