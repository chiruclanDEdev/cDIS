#!/usr/bin/env python

# Copyright by chiruclan.de IRC services 2012-2013

import sys
import socket
import os
import ConfigParser
import time
import hashlib
import smtplib
import _mysql
import subprocess
import urllib2
import traceback
import thread
import fnmatch
import ssl
import threading
import modules
import __builtin__

def red(string):
	return("\033[91m" + string + "\033[0m")

def blue(string):
	return("\033[94m" + string + "\033[0m")

def green(string):
	return("\033[92m" + string + "\033[0m")

try:
	if not os.access("logs", os.F_OK):
		os.mkdir("logs")
	config = ConfigParser.RawConfigParser()
	if len(sys.argv) == 1:
		config.read("configs/config.cfg")
	else:
		config.read(sys.argv[1])
		
	bots = ConfigParser.RawConfigParser()
	bots.read("configs/" + config.get("INCLUDES", "bots"))
except Exception:
	et, ev, tb = sys.exc_info()
	print(red("*") + " <<ERROR>> {0}: {1} (Line #{2})".format(et, ev, traceback.tb_lineno(tb)))

def debug(text):
	if config.get("OTHER", "debug") == "1":
		print(str(text))

def shell(text):
	subprocess.Popen(text+" >> /dev/null", shell=True).wait()

def perror(text):
	try:
		debug(red("*") + " " + text)
		file = open("error.log", "ab")
		file.write(text+"\n")
		file.close()
	except: pass

class Services:
	def __init__(self):
		self.mysql_host = config.get("MYSQL", "host")
		self.mysql_port = config.getint("MYSQL", "port")
		self.mysql_name = config.get("MYSQL", "name")
		self.mysql_user = config.get("MYSQL", "user")
		self.mysql_passwd = config.get("MYSQL", "passwd")
		self.server_name = config.get("SERVER", "name")
		self.server_address = config.get("SERVER", "address")
		self.server_port = config.get("SERVER", "port")
		self.server_id = config.get("SERVER", "id")
		self.server_password = config.get("SERVER", "password")
		self.services_name = config.get("SERVICES", "name")
		self.services_id = config.get("SERVICES", "id")
		self.services_address = config.get("SERVICES", "address")
		self.services_description = config.get("SERVICES", "description")
		self.debug = config.get("OTHER", "debug")
		self.email = config.get("OTHER", "email")
		self.ipv6 = config.getboolean("OTHER", "ipv6")
		self.ssl = config.getboolean("OTHER", "ssl")
		self.regmail = config.get("OTHER", "regmail")
		self.oper_not = config.getboolean("OPERS", "notifications")
		
	def query(self, string, *args):
		conn = _mysql.connect(host=self.mysql_host, port=self.mysql_port, db=self.mysql_name, user=self.mysql_user, passwd=self.mysql_passwd)
		conn.query("SET @s = '" + conn.escape_string(str(string)) + "'")
		conn.query("PREPARE query FROM @s")
		
		i = 0
		all_variables = ""
		
		for arg in args:
			i += 1
			conn.query("SET @" + str(i) + " = '" + conn.escape_string(str(arg)) + "'")
			
			if i == 1:
				all_variables += " USING @" + str(i)
			else:
				all_variables += ", @" + str(i)
				
		conn.query("EXECUTE query" + all_variables)
		result = conn.store_result()
		conn.query("DEALLOCATE PREPARE query")
		
		if result:
			results = list()
			
			for data in result.fetch_row(maxrows=0, how=1):
				results.append(data)
				
			conn.close()
			return results
			
		conn.close()
		return None
		
	def send(self, text):
		self.con.send(text+"\n")
		debug(blue("*") + " " + text)

	def run(self):
		try:
			self.query("truncate logs")
			self.query("truncate opers")
			self.query("truncate online")
			self.query("truncate chanlist")
			self.query("truncate modules")
			shell("rm -rf logs/*")
			
			if self.ipv6 and socket.has_ipv6:
				if self.ssl:
					self.con = ssl.wrap_socket(socket.socket(socket.AF_INET6, socket.SOCK_STREAM))
				else:
					self.con = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			else:
				if self.ssl:
					self.con = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
				else:
					self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					
			self.con.connect((self.server_address, int(self.server_port)))
			self.send("SERVER %s %s 0 %s :%s" % (self.services_name, self.server_password, self.services_id, self.services_description))
			self.send(":%s BURST" % self.services_id)
			self.send(":%s ENDBURST" % self.services_id)
			__builtin__.con = self.con
			__builtin__.spamscan = {}
			__builtin__._connected = False
			__builtin__.config = config
			__builtin__.bots = bots
			
			for mods in dir(modules):
				if os.access("modules/" + mods + ".py", os.F_OK):
					moduleToCall = getattr(modules, mods)
					classToCall = getattr(moduleToCall, mods)()
					
					if classToCall.MODULE_CLASS == "SCHEDULE":
						methodToCall = getattr(classToCall, "onSchedule")
						thread.start_new_thread(methodToCall, ())
						
					self.query("INSERT INTO `modules` (`name`, `class`, `oper`, `auth`, `command`, `help`, `bot`) VALUES (?, ?, ?, ?, ?, ?, ?)", mods, classToCall.MODULE_CLASS, classToCall.NEED_OPER, classToCall.NEED_AUTH, classToCall.COMMAND, classToCall.HELP, classToCall.BOT_ID)
						
			
			while 1:
				recv = self.con.recv(25600)
				
				if not recv:
					return 1
					
				for data in recv.splitlines():
					if data.strip() != "":
						debug(green("*") + " " + data)
						thread.start_new_thread(ServiceThread().onData, (data.strip(),))
					
		except Exception:
			et, ev, tb = sys.exc_info()
			e = "{0}: {1} (Line #{2})".format(et, ev, traceback.tb_lineno(tb))
			debug(red("*") + " <<ERROR>> " + str(e))

class ServiceThread:
	import sys
	import socket
	import os
	import ConfigParser
	import time
	import hashlib
	import smtplib
	import _mysql
	import subprocess
	import urllib2
	import traceback
	import thread
	import fnmatch
	import __builtin__

	def __init__(self):
		self.mysql_host = config.get("MYSQL", "host")
		self.mysql_port = config.getint("MYSQL", "port")
		self.mysql_name = config.get("MYSQL", "name")
		self.mysql_user = config.get("MYSQL", "user")
		self.mysql_passwd = config.get("MYSQL", "passwd")
		self.server_name = config.get("SERVER", "name")
		self.server_address = config.get("SERVER", "address")
		self.server_port = config.get("SERVER", "port")
		self.server_id = config.get("SERVER", "id")
		self.server_password = config.get("SERVER", "password")
		self.services_name = config.get("SERVICES", "name")
		self.services_id = config.get("SERVICES", "id")
		self.services_description = config.get("SERVICES", "description")
		self.services_address = config.get("SERVICES", "address")
		self.debug = config.get("OTHER", "debug")
		self.email = config.get("OTHER", "email")
		self.ipv6 = config.getboolean("OTHER", "ipv6")
		self.ssl = config.getboolean("OTHER", "ssl")
		self.regmail = config.get("OTHER", "regmail")
		
		self.bot = "%sAAAAAA" % self.services_id
		self.bot_nick = bots.get("1", "nick").split()[0]
		self.bot_user = bots.get("1", "user").split()[0]
		self.bot_real = bots.get("1", "real")
		
		self.oper_not = config.getboolean("OPERS", "notifications")
		self.con = con
		
	def shell(self, text):
		subprocess.Popen(text+" >> /dev/null", shell=True).wait()
	
	def onData(self, data):
		try:
			if data.split()[1] == "PING":
				self.send(":%s PONG %s %s" % (self.services_id, self.services_id, data.split()[2]))
				self.send(":%s PING %s %s" % (self.services_id, self.services_id, data.split()[2]))
			elif data.split()[1] == "ENDBURST" and not _connected:
				__builtin__._connected = True
				
				for bot in bots.sections():
					botuid = self.services_id + bots.get(bot, "uuid")
					self.send(":%s UID %s %s %s %s %s %s %s %s +Ik :%s" % (self.services_id, botuid, time.time(), bots.get(bot, "nick"), self.services_name, self.services_name, bots.get(bot, "user"), self.services_address, time.time(), bots.get(bot, "real")))
					self.send(":%s OPERTYPE Service" % botuid)
					self.meta(self.bot, "accountname", bots.get(bot, "nick"))
					
				self.msg("$*", "Services are now back online. Have a nice day :)")
				self.msg("$*", "Please note that you have to login manually after a restart!")
				
				for channel in self.query("select name,modes,topic from channelinfo"):
					self.join(str(channel["name"]))
					
					if self.chanflag("m", channel["name"]):
						self.mode(channel["name"], channel["modes"])
						
					if self.chanflag("t", channel["name"]):
						self.send(":{0} TOPIC {1} :{2}".format(self.bot, channel["name"], channel["topic"]))
						
						if self.chanflag("l", channel["name"]):
							self.log(self.bot_nick, "topic", channel["name"], ":"+channel["topic"])
							
			else:
				for module in self.query("SELECT * FROM `modules` WHERE `class` = ?", data.split()[1]):
					if os.access("modules/" + module["name"] + ".py", os.F_OK):
						moduleToCall = getattr(modules, module["name"])
						classToCall = getattr(moduleToCall, module["name"])()
						
						if classToCall.MODULE_CLASS.lower() == data.split()[1].lower():
							methodToCall = getattr(classToCall, "onData")
							thread.start_new_thread(methodToCall, (data, ))
							
			if data.split()[1] == "PRIVMSG":
				for bot in bots.sections():
					botuid = self.services_id + bots.get(bot, "uuid")
					
					if data.split()[2] == botuid:
						iscmd = False
						cmd = data.split()[3][1:]
						
						for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `command` = ? AND `bot` = ?", cmd, bot):
							if os.access("modules/" + command["name"] + ".py", os.F_OK):
								iscmd = True
								
								cmd_auth = int(command["auth"])
								cmd_oper = int(command["oper"])
								
								moduleToCall = getattr(modules, command["name"])
								classToCall = getattr(moduleToCall, command["name"])()
								methodToCall = getattr(classToCall, "onCommand")
								
								if cmd_oper and self.isoper(data.split()[0][1:]):
									if len(data.split()) == 4:
										thread.start_new_thread(methodToCall, (data.split()[0][1:], ''))
									elif len(data.split()) > 4:
										thread.start_new_thread(methodToCall, (data.split()[0][1:], ' '.join(data.split()[4:])))
								elif not cmd_auth and not cmd_oper:
									if len(data.split()) == 4:
										thread.start_new_thread(methodToCall, (data.split()[0][1:], ''))
									elif len(data.split()) > 4:
										thread.start_new_thread(methodToCall, (data.split()[0][1:], ' '.join(data.split()[4:])))
								elif cmd_auth and not cmd_oper:
									if self.auth(data.split()[0][1:]):
										if len(data.split()) == 4:
											thread.start_new_thread(methodToCall, (data.split()[0][1:], ''))
										elif len(data.split()) > 4:
											thread.start_new_thread(methodToCall, (data.split()[0][1:], ' '.join(data.split()[4:])))
									else:
										self.msg(data.split()[0][1:], "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()), uid=botuid)
										
						if not iscmd:
							self.msg(data.split()[0][1:], "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()), uid=botuid)
								
				if data.split()[2].startswith("#") and self.chanflag("f", data.split()[2]) and self.chanexist(data.split()[2]):
					if data.split()[3][1:].startswith(self.fantasy(data.split()[2])):
						botuid = self.services_id + bots.get("3", "uuid")
						iscmd = False
						fuid = data.split()[0][1:]
						cmd = self.fantasy(data.split()[2])
						
						if len(data.split()[3]) > int(1+len(self.fantasy(data.split()[2]))):
							fchan = data.split()[2]
							cmd = data.split()[3][int(1+len(self.fantasy(fchan))):]
							
							if len(data.split()) > 4:
								args = ' '.join(data.split()[4:]).replace("'", "\\'")
								
							for command in self.query("SELECT * FROM `modules` WHERE `class` = 'COMMAND' AND `command` = ? AND `oper` = 0 AND `bot` = '3'", cmd):
								if os.access("modules/" + command["name"] + ".py", os.F_OK):
									iscmd = True
									moduleToCall = getattr(modules, command["name"])
									classToCall = getattr(moduleToCall, command["name"])()
									methodToCall = getattr(classToCall, "onFantasy")
									
									if not classToCall.NEED_AUTH:
										if len(data.split()) == 4:
											thread.start_new_thread(methodToCall, (fuid, fchan, ''))
										elif len(data.split()) > 4:
											thread.start_new_thread(methodToCall, (fuid, fchan, args))
									elif classToCall.NEED_AUTH:
										if self.auth(fuid):
											if len(data.split()) == 4:
												thread.start_new_thread(methodToCall, (fuid, fchan, ''))
											elif len(data.split()) > 4:
												thread.start_new_thread(methodToCall, (fuid, fchan, args))
										else:
											self.msg(fuid, "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()), uid=botuid)
									
					if not iscmd:
						self.msg(fuid, "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()), uid=botuid)
		except Exception:
			et, ev, tb = sys.exc_info()
			e = "{0}: {1} (Line #{2})".format(et, ev, traceback.tb_lineno(tb))
			debug(red("*") + " <<ERROR>> " + str(e))

	def send_bot(self, content):
		self.send(":" + self.bot + " " + content)

	def send_serv(self, content):
		self.send(":" + self.services_id + " " + content)

	def send_to_op(self, content):
		if not self.oper_not:
			return 0;
			
		result = self.query("SELECT `uid` FROM `opers`")
		for row in result:
			self.send_serv("PRIVMSG " + row["uid"] + " :-" + self.services_name + "- " + content)

	def metadata(self, uid, string, content):
		if string == "accountname":
			if self.ison(content, True):
				self.query("UPDATE `online` SET `account` = ? WHERE `uid` = ?", content, uid)
				self.msg(uid, "You are now logged in as %s" % content)
				self.vhost(uid)
				self.flag(uid)
				self.memo(content)

	def regexflag (self, original, pattern, include_negatives = False):
		pflags = ""
		nflags = ""
		actflag = ""
		
		for char in original:
			if char.isalpha() or char == "+" or char == "-":
				if char == "+":
					actflag = "+"
				elif char == "-":
					actflag = "-"
				elif actflag == "+":
					if pflags.find(char) == -1:
						pflags += char
				elif actflag == "-":
					if nflags.find(char) == -1:
						nflags += char
				else:
					if pflags.find(char) == -1:
						pflags += char
			else:
				return original
		
		for char in pattern:
			if char.isalpha() or char == "+" or char == "-":
				if char == "+":
					actflag = "+"
				elif char == "-":
					actflag = "-"
				elif actflag == "+":
					if pflags.find(char) == -1:
						if nflags.find(char) == -1:
							pflags += char
						else:
							nflags = nflags.replace(char, "")
				elif actflag == "-":
					if nflags.find(char) == -1:
						if pflags.find(char) == -1:
							nflags += char
						else:
							pflags = pflags.replace(char, "")
			else:
				return original
				
		if include_negatives:
			rData = ""
			if pflags:
				rData += "+"
				rData += pflags
			if nflags:
				rData += "-"
				rData += nflags
				
			return rData
			
		return pflags
		
	def metadata(self, uid, string, content):
		if string == "accountname":
			if self.ison(uid, True):
				self.query("UPDATE `online` SET `account` = ? WHERE `uid` = ?", content, uid)
				self.msg(uid, "You are now logged in as %s" % content)
				self.vhost(uid)
				self.flag(uid)
				self.memo(content)


	def uid (self, nick):
		if nick == self.bot_nick:
			return self.bot
			
		for data in self.query("select uid from online where nick = ?", nick):
			return str(data["uid"])
			
		return nick

	def nick (self, source):
		if source == self.bot:
			return self.bot_nick
			
		for data in self.query("select nick from online where uid = ?", source):
			return str(data["nick"])
			
		return source

	def user (self, user):
		if user.lower() == self.bot_nick.lower():
			return self.bot_nick
			
		for data in self.query("select name from users where name = ?", user):
			return str(data["name"])
			
		return False

	def banned(self, user):
		for data in self.query("select * from users where name = ? and suspended != '0'", user):
			return data["suspended"]
			
		return False

	def gateway (self, target):
		uid = self.uid(target)
		
		for data in self.query("select uid from gateway where uid = ?", uid):
			return True
			
		return False

	def send(self, text):
		self.con.send(text+"\n")
		debug(blue("*") + " " + text)

	def push(self, target, message):
		self.send(":{uid} PUSH {target} ::{message}".format(uid=self.services_id, target=target, message=message))

	def help(self, target, command, description=""):
		self.msg(target, command.upper()+" "*int(20-len(command))+description)

	def ison(self, user, uid=False):
		if not uid:
			for data in self.query("select nick from online where account = ? LIMIT 1", user):
				return True
		else:
			for data in self.query("select nick from online where uid = ? LIMIT 1", user):
				return True
			
		return False

	def usermodes(self, target):
		user = self.auth(target)
		
		if self.ison(user):
			for data in self.query("select modes from users where name = ?", user):
				self.mode(target, data["modes"])
				
				if data["modes"].find("+") != -1:
					modes = data["modes"].split("+")[1]
					
					if modes.find("-") != -1:
						modes = modes.split("-")[0]
						
					if modes.find("B") != -1:
						if not self.gateway(target):
							self.query("insert into gateway values (?)", target)
							self.vhost(target)
							
				if data["modes"].find("-") != -1:
					modes = data["modes"].split("-")[1]
					
					if modes.find("+") != -1:
						modes.split("+")[0]
						
					if modes.find("B") != -1:
						if self.gateway(target):
							self.query("delete from gateway where uid = ?", target)
							self.vhost(target)

	def userflags(self, target):
		user = self.auth(target)
		
		if user == 0:
			user = target
			
		for data in self.query("select flags from users where name = ?", user):
			return data["flags"]

	def userflag(self, target, flag):
		user = self.auth(target)
		
		if self.ison(user):
			for data in self.query("select flags from users where name = ?", user):
				if str(data["flags"]).find(flag) != -1:
					return True
		else:
			if flag == "n":
				return True
				
		return False

	def msg(self, target, text=" ", action=False, uid=""):
		source = self.bot
		
		if uid != "":
			source = uid
			
		if self.userflag(target, "n") and not action:
			self.send(":%s NOTICE %s :%s" % (source, target, text))
		elif not self.userflag(target, "n") and not action:
			self.send(":%s PRIVMSG %s :%s" % (source, target, text))
		else:
			self.send(":%s PRIVMSG %s :\001ACTION %s\001" % (self.bot, target, text))

	def mode(self, target, mode):
		self.send(":%s SVSMODE %s %s" % (self.bot, target, mode))
		
		if target.startswith("#"):
			if self.chanflag("l", target):
				self.log(self.bot_nick, "mode", target, mode)

	def meta(self, target, meta, content):
		self.send(":%s METADATA %s %s :%s" % (self.services_id, target, meta, content))

	def auth(self, target):
		for data in self.query("select account from online where uid = ? and account != ''", target):
			return data["account"]
			
		return 0

	def sid(self, account):
		uids = list()
		
		for data in self.query("select uid from online where account = ?", account):
			uids.append(data["uid"])
			
		return uids

	def memo(self, user):
		for data in self.query("select source,message from memo where user = ?", user):
			online = False
			
			for source in self.sid(user):
				online = True
				self.msg(source, "[Memo] From: %s, Message: %s" % (data["source"], data["message"]))
				
			if online:
				self.query("delete from memo where user = ? and source = ? and message = ?", user, data["source"], data["message"])

	def chanexist(self, channel):
		for data in self.query("select name from channelinfo where name = ?", channel):
			return True
			
		return False
		
	def gettopic(self, channel):
		if self.chanexist(channel):
			for data in self.query("select topic from channelinfo where name = ?", channel):
				return data["topic"]
				
		return ""

	def join(self, channel):
		if self.chanexist(channel) and not self.suspended(channel):
			self.send(":%s JOIN %s" % (self.services_id + bots.get("3", "uuid"), channel))
			self.mode(channel, "+ryo {0} {0}".format(self.services_id + bots.get("3", "uuid")))

	def statistics(self):
		stats = dict()
		
		for data in self.query("select * from statistics"):
			stats[data["attribute"]] = data["value"]
			
		return stats

	def killcount(self):
		kills = int(self.statistics()["kills"])
		kills += 1
		self.query("update statistics set `value` = ? where attribute = 'kills'", kills)
		return kills

	def kickcount(self):
		kicks = int(self.statistics()["kicks"])
		kicks += 1
		self.query("update statistics set `value` = ? where attribute = 'kicks'", kicks)
		return kicks

	def kill(self, target, reason="You're violating network rules"):
		if not self.isoper(self.uid(target)):
			self.send_serv("KILL %s :Killed (*.%s (%s (#%s)))" % (self.uid(target), self.getservicedomain(), reason, str(self.killcount())))

	def vhost(self, target):
		if not self.gateway(target):
			entry = False
			
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", self.auth(target)):
				entry = True
				vhost = str(data["vhost"])
				
				if str(data["vhost"]).find("@") != -1:
					vident = vhost.split("@")[0]
					vhost = vhost.split("@")[1]
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, vident))
					
				self.send(":%s CHGHOST %s %s" % (self.bot, target, vhost))
				self.msg(target, "Your vhost %s has been activated" % data["vhost"])
				
			if not entry:
				if not self.userflag(target, "x"):
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, self.getident(target)))
					self.send(":%s CHGHOST %s %s" % (self.bot, target, self.gethost(target)))
				else:
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, self.getident(target)))
					self.send(":%s CHGHOST %s %s.users.%s" % (self.bot, target, self.auth(target), self.getservicedomain()))
		else:
			username = self.userhost(target).split("@")[0]
			self.send(":%s CHGIDENT %s %s" % (self.bot, target, username))
			crypthost = self.encode_md5(target + ":" + self.nick(target) + "!" + self.userhost(target))
			self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, target, crypthost, self.getservicedomain()))
			self.msg(target, "Your vhost %s.gateway.%s has been activated" % (crypthost, self.getservicedomain()))
			
	def getservicedomain(self):
		rawdomain = self.services_name.split(".")[-2:]
		fulldomain = '.'.join(rawdomain)
		return fulldomain

	def flag(self, target, channel = ""):
		account = self.auth(target)
		if account != 0:
			if channel != "":
				for flag in self.query("select flag,channel from channels where user = ? and channel = ?", account, channel):
					if flag["flag"] == "n" or flag["flag"] == "q":
						self.mode(flag["channel"], "+qo " + target + " " + target)
					elif flag["flag"] == "a":
						self.mode(flag["channel"], "+ao " + target + " " + target)
					elif flag["flag"] == "o":
						self.mode(flag["channel"], "+o " + target)
					elif flag["flag"] == "h":
						self.mode(flag["channel"], "+h " + target)
					elif flag["flag"] == "v":
						self.mode(flag["channel"], "+v " + target)
					elif flag["flag"] == "b":
						self.kick(flag["channel"], target, "Banned.")
			else:
				for flag in self.query("select flag,channel from channels where user = ? order by channel", account):
					if flag["flag"] == "n" or flag["flag"] == "q":
						self.mode(flag["channel"], "+qo " + target + " " + target)
					elif flag["flag"] == "a":
						self.mode(flag["channel"], "+ao " + target + " " + target)
					elif flag["flag"] == "o":
						self.mode(flag["channel"], "+o " + target)
					elif flag["flag"] == "h":
						self.mode(flag["channel"], "+h " + target)
					elif flag["flag"] == "v":
						self.mode(flag["channel"], "+v " + target)
					elif flag["flag"] == "b":
						self.kick(flag["channel"], target, "Banned.")

	def autojoin(self, target):
		user = self.auth(target)
		
		if self.ison(user):
			if self.userflag(target, "a"):
				for data in self.query("select channel,flag from channels where user = ?", user):
					channel = data["channel"]
					flag = data["flag"]
					
					if flag == "n" or flag == self.bot_nick or flag == "a" or flag == "o" or flag == "h" or flag == "v":
						self.send(":%s SVSJOIN %s %s" % (self.bot, target, channel))

	def getflag(self, target, channel):
		for data in self.query("select account from online where uid = ?", target):
			for flag in self.query("select flag from channels where channel = ? and user = ?", channel, data["account"]):
				return flag["flag"]
				
		return 0

	def chanflag(self, flag, channel):
		for data in self.query("select flags from channelinfo where name = ?", channel):
			if data["flags"].find(flag) != -1:
				return True
				
		return False

	def isoper(self, target):
		if self.isserv(target):
			return True
			
		isoper = False
		
		for data in self.query("select * from opers where uid = ?", target):
			isoper = True
			
		return isoper

	def encode(self, string):
		return hashlib.sha512(string).hexdigest()

	def encode_md5(self, string):
		return hashlib.md5(string).hexdigest()

	def query(self, string, *args):
		conn = _mysql.connect(host=self.mysql_host, port=self.mysql_port, db=self.mysql_name, user=self.mysql_user, passwd=self.mysql_passwd)
		
		conn.query("SET @s = '" + conn.escape_string(str(string)) + "'")
		conn.query("PREPARE query FROM @s")
		
		i = 0
		all_variables = ""
		
		for arg in args:
			i += 1
			conn.query("SET @" + str(i) + " = '" + conn.escape_string(str(arg)) + "'")
			
			if i == 1:
				all_variables += " USING @" + str(i)
			else:
				all_variables += ", @" + str(i)
		
		conn.query("EXECUTE query" + all_variables)
		result = conn.store_result()
		conn.query("DEALLOCATE PREPARE query")
		
		if result:
			results = list()
			
			for data in result.fetch_row(maxrows=0, how=1):
				results.append(data)
				
			conn.close()
			return results
			
		conn.close()
		return None

	def query_row(self, string, *args):
		conn = _mysql.connect(host=self.mysql_host, port=self.mysql_port, db=self.mysql_name, user=self.mysql_user, passwd=self.mysql_passwd)
		
		conn.query("SET @s = '" + conn.escape_string(str(string)) + "'")
		conn.query("PREPARE query FROM @s")
		
		i = 0
		all_variables = ""
		
		for arg in args:
			i += 1
			conn.query("SET @" + str(i) + " = '" + conn.escape_string(str(arg)) + "'")
			
			if i == 1:
				all_variables += " USING @" + str(i)
			else:
				all_variables += ", @" + str(i)
		
		conn.query("EXECUTE query" + all_variables)
		result = conn.store_result()
		conn.query("DEALLOCATE PREPARE query")
		
		if result:
			for data in result.fetch_row(maxrows=1, how=1):
				conn.close()
				return data
				
		conn.close()
		return None

	def mail(self, receiver, message):
		try:
			mail = smtplib.SMTP('127.0.0.1', 25)
			mail.sendmail(self.email, ['%s' % receiver], message)
			mail.quit()
		except Exception,e:
			debug(red("*") + " <<MAIL-ERROR>> "+str(e))

	def log(self, source, msgtype, channel, text=""):
		try:
			if msgtype.lower() == "mode" and len(text.split()) > 1:
				nicks = list()
				
				for nick in text.split()[1:]:
					nicks.append(self.nick(nick))
					
				text = "{text} {nicks}".format(text=text.split()[0], nicks=' '.join(nicks))
				
			if source == self.bot_nick:
				sender = self.bot_nick+"!"+self.bot_user+"@"+self.services_name
			else:
				hostmask = self.hostmask(source)
				sender = hostmask[len(hostmask)-1]
				
			result = self.query("SELECT COUNT(*) FROM `logs` WHERE `channel` = ?", channel)
			for row in result:
				if row["COUNT(*)"] == 50:
					self.query("DELETE FROM `logs` WHERE `channel` = ? LIMIT 1", channel)
					
			self.query("INSERT INTO `logs` (`channel`, `sender`, `action`, `message`) VALUES (?, ?, ?, ?)", channel, sender, msgtype.upper(), text)
		except:
			pass

	def showlog(self, source, channel):
		try:
			escaped_actions = list()
			escaped_actions.append("JOIN")
			escaped_actions.append("PART")
			escaped_actions.append("QUIT")
			escaped_actions.append("MODE")
			escaped_actions.append("KICK")
			escaped_actions.append("TOPIC")
			
			self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE "+channel+" :*** Log start")
			
			result = self.query("SELECT `channel`, `sender`, `action`, `message` FROM `logs` WHERE `channel` = ? ORDER BY `id`", channel)
			for row in result:
				escaped_action = False
				
				for action in escaped_actions:
					if row["action"] == action:
						escaped_action = True
						
				if not escaped_action:
					if row["action"] == "PRIVMSG":
						row["action"] = "NOTICE"
						
					self.push(source, row["sender"] + " " + row["action"] + " " + row["channel"] + " " + row["message"])
				else:
					message = row["sender"] + " " + row["action"] + " " + row["channel"] + " " + row["message"]
					self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE " + row["channel"] + " :" + message)
					
			self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE "+channel+" :*** Log end")
		except:
			pass

	def convert_timestamp(self, timestamp):
		dif = int(timestamp)
		days = 0
		hours = 0
		minutes = 0
		seconds = 0
		
		if dif == 86400 or dif > 86400:
			days = int(dif)/86400
			dif = int(dif)-int(days)*86400
			
		if dif == 3600 or dif > 3600:
			hours = int(dif)/3600
			dif = int(dif)-int(hours)*3600
			
		if dif == 60 or dif > 60:
			minutes = int(dif)/60
			dif = int(dif)-int(minutes)*60
			
		seconds = dif
		
		if days > 0:
			return "%s days %s hours %s minutes %s seconds" % (days, hours, minutes, seconds)
			
		if hours > 0:
			return "%s hours %s minutes %s seconds" % (hours, minutes, seconds)
			
		if minutes > 0:
			return "%s minutes %s seconds" % (minutes, seconds)
			
		return "%s seconds" % seconds

	def kick(self, channel, target, reason="Requested."):
		uid = self.uid(target)
		
		if self.onchan(channel, target):
			if self.chanflag("c", channel):
				self.send(":{uid} KICK {channel} {target} :{reason} (#{count})".format(uid=self.bot, target=uid, channel=channel, reason=reason, count=str(self.kickcount())))
			else:
				self.send(":{uid} KICK {channel} {target} :{reason}".format(uid=self.bot, target=uid, channel=channel, reason=reason))
				self.kickcount()
				
			self.query("delete from chanlist where channel = ? and uid = ?", channel, uid)

	def userlist(self, channel):
		uid = list()
		
		for user in self.query("select uid from chanlist where channel = ?", channel):
			uid.append(user["uid"])
			
		return uid

	def onchan(self, channel, target):
		uid = self.uid(target)
		
		for data in self.query("select * from chanlist where channel = ? and uid = ?", channel, uid):
			return True
			
		return False

	def getident(self, target):
		uid = self.uid(target)
		
		for data in self.query("select username from online where uid = ?", uid):
			return data["username"]
			
		return 0

	def gethost(self, target):
		uid = self.uid(target)
		
		for data in self.query("select host from online where uid = ?", uid):
			return data["host"]
			
		return 0

	def hostmask(self, target):
		uid = self.uid(target)
		masks = list()
		nick = None
		username = None
		account = self.auth(uid)
		
		for data in self.query("select nick,username,host from online where uid = ?", uid):
			nick = data["nick"]
			username = data["username"]
			masks.append(data["nick"]+"!"+data["username"]+"@"+data["host"])
			
		if self.auth(uid) != 0:
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", account):
				if str(data["vhost"]).find("@") != -1:
					masks.append(nick+"!"+data["vhost"])
				else:
					masks.append(nick+"!"+username+"@"+data["vhost"])
					
			if self.userflag(uid, "x"):
				masks.append(nick + "!" + username + "@" + account + ".users." + self.getservicedomain())
					
		return masks

	def enforceban(self, channel, target):
		if target != "*!*@*":
			for user in self.userlist(channel):
				if self.gateway(user):
					crypthost = self.encode_md5(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+self.getservicedomain()
					
					if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, target):
						self.mode(channel, "+b "+target)
						self.kick(channel, user, "Banned.")
						
				for hostmask in self.hostmask(user):
					if fnmatch.fnmatch(hostmask, target):
						self.mode(channel, "+b "+target)
						self.kick(channel, user, "Banned.")

	def enforcebans(self, channel):
		for data in self.query("select ban from banlist where channel = ?", channel):
			if data["ban"] != "*!*@*":
				for user in self.userlist(channel):
					if self.gateway(user):
						crypthost = self.encode_md5(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+'.'.join(self.services_name.split(".")[-2:])
						
						
						if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, data["ban"]):
							self.mode(channel, "+b "+data["ban"])
							self.kick(channel, user, "Banned.")
							
					for hostmask in self.hostmask(user):
						if fnmatch.fnmatch(hostmask, data["ban"]):
							self.mode(channel, "+b "+data["ban"])
							self.kick(channel, user, "Banned.")

	def checkbans(self, channel, bans):
		if self.chanflag("e", channel):
			for ban in bans.split():
				if fnmatch.fnmatch(ban, "*!*@*") and ban != "*!*@*":
					for user in self.userlist(channel):
						if self.gateway(user):
							crypthost = self.encode(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+'.'.join(self.services_name.split(".")[-2:])
							
							if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, ban):
								self.kick(channel, user, "Banned.")
								
						for hostmask in self.hostmask(user):
							if fnmatch.fnmatch(hostmask, ban):
								self.kick(channel, user, "Banned.")
								
						for ip in self.getip(user):
							if fnmatch.fnmatch("*!*@"+ip, ban):
								self.kick(channel, user, "Banned.")
				elif ban == "*!*@*":
					self.mode(channel, "-b *!*@*")

	def getip(self, target):
		uid = self.uid(target)
		
		for data in self.query("select address from online where uid = ?", uid):
			return data["address"]
			
		return 0

	def gline(self, target, reason="", bantime="1800", addentry=False):
		uid = self.uid(target)
		
		if uid != self.bot and target.lower() != self.bot_nick.lower() and not self.isoper(uid):
			ip = self.getip(uid)
			
			if addentry:
				rows = int(self.query_row("SELECT COUNT(*) FROM `glines` WHERE `mask` = ?", "*@" + ip)["COUNT(*)"])
				
				if rows == 0:
					etime = int(time.time()) + int(bantime)
					self.query("INSERT INTO `glines` (`mask`, `timestamp`) VALUES (?, ?)", "*@" + ip, etime)
					
			for data in self.query("select uid from online where address = ?", self.getip(uid)):
				self.send_serv("KILL "+data["uid"]+" :G-lined")
				
			self.send_serv("GLINE *@"+ip+" "+str(bantime)+" :"+reason)
			self.send_to_op("#G-line# *@" + ip + " added (" + self.convert_timestamp(int(bantime)) + ")")

	def suspended(self, channel):
		for data in self.query("select reason from suspended where channel = ?", channel):
			return data["reason"]
			
		return False

	def userhost(self, target):
		uid = self.uid(target)
		
		for data in self.query("select username,host from online where uid = ?", uid):
			return data["username"]+"@"+data["host"]
			
		return 0

	def getvhost(self, target):
		for data in self.query("select vhost from vhosts where user = ? and active = '1'", target):
			return data["vhost"]
			
		if self.userflag(target, "x"):
			return "{0}.users.{1}".format(self.auth(target), self.getservicedomain())
			
		return "None"

	def scanport(self, host, port):
		try:
			scpo = socket.socket()
			scpo.settimeout(1)
			scpo.connect((str(host), int(port)))
			scpo.close()
			return True
		except socket.error:
			return False

	def fantasy(self, channel):
		if self.chanexist(channel):
			for data in self.query("select fantasy from channelinfo where name = ?", channel):
				return data["fantasy"]
				
		return False

	def getconns(self, address):
		result = self.query("SELECT COUNT(*) FROM `online` WHERE `address` = ?", address)
		for row in result:
			return int(row["COUNT(*)"])
			
		return 0

	def checkconnection(self, uid):
		if self.isserv(uid):
			return False
			
		user_ip = self.getip(uid)
		user_host = self.gethost(uid)
		user_name = self.userhost(uid).split("@")[0]
		timestamp = time.time()
		
		if user_ip == 0:
			return False
			
		limit = 3
		result = self.query("SELECT `limit` FROM `trust` WHERE (`address` = ? OR `address` = ?) AND `timestamp` > ?", user_ip, user_host, timestamp)
		for row in result:
			limit = int(row["limit"])
			
			if user_name.startswith("~"):
				self.msg(uid, "You ignored the trust rules. Please run an identd before you connect again.")
				self.gline(uid, "Ignored trust rules. Run an identd before connecting again.", addentry=True)
				return 0
				
		if self.getconns(user_ip) > limit:
			self.gline(uid, "Connection limit ({0}) reached".format(str(limit)), addentry=True)
			return True
		elif self.getconns(user_ip) == limit:
			for row in self.query("SELECT `uid` FROM `online` WHERE `address` = ? OR `host` = ?", user_ip, user_host):
				self.msg(nick["uid"], "Your IP is scratching the connection limit. If you need more connections please request a trust.")
				
		return False

	def isserv(self, uid):
		uid = self.uid(uid)
		if uid.startswith(self.services_id):
			return True
			
		return False
		
	def opertype(self, uid):
		for row in self.query("SELECT `opertype` FROM `opers` WHERE `uid` = ?", uid):
			return row["opertype"]
			
		return None

	def isoptype(self, uid, type):
		for row in self.query("SELECT `uid` FROM `opers` WHERE `uid` = ? AND `opertype` = ?", uid, type):
			return True
			
		return False

class cDISModule:
	import sys
	import os
	import time
	import ConfigParser
	import hashlib
	import smtplib
	import _mysql
	import traceback
	import fnmatch
	import __builtin__
	
	HELP = ''
	NEED_OPER = 0
	NEED_AUTH = 0
	MODULE_CLASS = ''
	COMMAND = ''
	BOT_ID = '0'

	def __init__(self):
		self.con = con
		self.mysql_host = config.get("MYSQL", "host")
		self.mysql_port = config.getint("MYSQL", "port")
		self.mysql_name = config.get("MYSQL", "name")
		self.mysql_user = config.get("MYSQL", "user")
		self.mysql_passwd = config.get("MYSQL", "passwd")
		self.server_name = config.get("SERVER", "name")
		self.server_address = config.get("SERVER", "address")
		self.server_port = config.get("SERVER", "port")
		self.server_id = config.get("SERVER", "id")
		self.server_password = config.get("SERVER", "password")
		self.services_name = config.get("SERVICES", "name")
		self.services_id = config.get("SERVICES", "id")
		self.services_description = config.get("SERVICES", "description")
		self.services_address = config.get("SERVICES", "address")
		self.debug = config.get("OTHER", "debug")
		self.email = config.get("OTHER", "email")
		self.ipv6 = config.getboolean("OTHER", "ipv6")
		self.ssl = config.getboolean("OTHER", "ssl")
		self.regmail = config.get("OTHER", "regmail")
		
		if self.BOT_ID == '0':
			self.bot = self.services_id
			self.bot_nick = "cDIS"
			self.bot_user = "cDIS"
			self.bot_real = "cDIS"
		else:
			self.bot = self.services_id + bots.get(self.BOT_ID, "uuid")
			self.bot_nick = bots.get(self.BOT_ID, "nick")
			self.bot_user = bots.get(self.BOT_ID, "user")
			self.bot_real = bots.get(self.BOT_ID, "real")
		
		self.oper_not = config.getboolean("OPERS", "notifications")

	def onCommand(self, uid, arguments):
		pass

	def onFantasy(self, uid, channel, arguments):
		pass
		
	def onData(self, data):
		pass
		
	def onSchedule(self):
		pass
		
	def regexflag (self, original, pattern, include_negatives = False):
		pflags = ""
		nflags = ""
		actflag = ""
		
		for char in original:
			if char.isalpha() or char == "+" or char == "-":
				if char == "+":
					actflag = "+"
				elif char == "-":
					actflag = "-"
				elif actflag == "+":
					if pflags.find(char) == -1:
						pflags += char
				elif actflag == "-":
					if nflags.find(char) == -1:
						nflags += char
				else:
					if pflags.find(char) == -1:
						pflags += char
			else:
				return original
		
		for char in pattern:
			if char.isalpha() or char == "+" or char == "-":
				if char == "+":
					actflag = "+"
				elif char == "-":
					actflag = "-"
				elif actflag == "+":
					if pflags.find(char) == -1:
						if nflags.find(char) == -1:
							pflags += char
						else:
							nflags = nflags.replace(char, "")
				elif actflag == "-":
					if nflags.find(char) == -1:
						if pflags.find(char) == -1:
							nflags += char
						else:
							pflags = pflags.replace(char, "")
			else:
				return original
				
		if include_negatives:
			rData = ""
			if pflags:
				rData += "+"
				rData += pflags
			if nflags:
				rData += "-"
				rData += nflags
				
			return rData
			
		return pflags

	def query(self, string, *args):
		conn = _mysql.connect(host=self.mysql_host, port=self.mysql_port, db=self.mysql_name, user=self.mysql_user, passwd=self.mysql_passwd)
		
		conn.query("SET @s = '" + conn.escape_string(str(string)) + "'")
		conn.query("PREPARE query FROM @s")
		
		i = 0
		all_variables = ""
		
		for arg in args:
			i += 1
			conn.query("SET @" + str(i) + " = '" + conn.escape_string(str(arg)) + "'")
			
			if i == 1:
				all_variables += " USING @" + str(i)
			else:
				all_variables += ", @" + str(i)
		
		conn.query("EXECUTE query" + all_variables)
		result = conn.store_result()
		conn.query("DEALLOCATE PREPARE query")
		
		if result:
			results = list()
			
			for data in result.fetch_row(maxrows=0, how=1):
				results.append(data)
				
			conn.close()
			return results
			
		conn.close()
		return None

	def query_row(self, string, *args):
		conn = _mysql.connect(host=self.mysql_host, port=self.mysql_port, db=self.mysql_name, user=self.mysql_user, passwd=self.mysql_passwd)
		
		conn.query("SET @s = '" + conn.escape_string(str(string)) + "'")
		conn.query("PREPARE query FROM @s")
		
		i = 0
		all_variables = ""
		
		for arg in args:
			i += 1
			conn.query("SET @" + str(i) + " = '" + conn.escape_string(str(arg)) + "'")
			
			if i == 1:
				all_variables += " USING @" + str(i)
			else:
				all_variables += ", @" + str(i)
		
		conn.query("EXECUTE query" + all_variables)
		result = conn.store_result()
		conn.query("DEALLOCATE PREPARE query")
		
		if result:
			for data in result.fetch_row(maxrows=1, how=1):
				conn.close()
				return data
				
		conn.close()
		return None

	def send_bot(self, content):
		self.send(":" + self.bot + " " + content)

	def send_serv(self, content):
		self.send(":" + self.services_id + " " + content)

	def send_to_op(self, content):
		if not self.oper_not:
			return 0;
			
		result = self.query("SELECT `uid` FROM `opers`")
		for row in result:
			self.send_serv("PRIVMSG " + row["uid"] + " :-" + self.services_name + "- " + content)

	def metadata(self, uid, string, content):
		if string == "accountname":
			if self.ison(uid, True):
				self.query("UPDATE `online` SET `account` = ? WHERE `uid` = ?", content, uid)
				self.msg(uid, "You are now logged in as %s" % content)
				self.vhost(uid)
				self.flag(uid)
				self.memo(content)


	def uid (self, nick):
		if nick == self.bot_nick:
			return self.bot
			
		for data in self.query("select uid from online where nick = ?", nick):
			return str(data["uid"])
			
		return nick

	def nick (self, source):
		if source == self.bot:
			return self.bot_nick
			
		for data in self.query("select nick from online where uid = ?", source):
			return str(data["nick"])
			
		return source

	def user (self, user):
		if user.lower() == self.bot_nick.lower():
			return self.bot_nick
			
		for data in self.query("select name from users where name = ?", user):
			return str(data["name"])
			
		return False

	def banned(self, user):
		for data in self.query("select * from users where name = ? and suspended != '0'", user):
			return data["suspended"]
			
		return False

	def gateway (self, target):
		uid = self.uid(target)
		
		for data in self.query("select uid from gateway where uid = ?", uid):
			return True
			
		return False

	def send(self, text):
		self.con.send(text+"\n")
		debug(blue("*") + " " + text)

	def push(self, target, message):
		self.send(":{uid} PUSH {target} ::{message}".format(uid=self.services_id, target=target, message=message))

	def help(self, target, command, description=""):
		self.msg(target, command.upper()+" "*int(20-len(command))+description)

	def ison(self, user, uid=False):
		if not uid:
			for data in self.query("select nick from online where account = ? LIMIT 1", user):
				return True
		else:
			for data in self.query("select nick from online where uid = ? LIMIT 1", user):
				return True
			
		return False

	def usermodes(self, target):
		user = self.auth(target)
		
		if self.ison(user):
			for data in self.query("select modes from users where name = ?", user):
				self.mode(target, data["modes"])
				
				if data["modes"].find("+") != -1:
					modes = data["modes"].split("+")[1]
					
					if modes.find("-") != -1:
						modes = modes.split("-")[0]
						
					if modes.find("B") != -1:
						if not self.gateway(target):
							self.query("insert into gateway values (?)", target)
							self.vhost(target)
							
				if data["modes"].find("-") != -1:
					modes = data["modes"].split("-")[1]
					
					if modes.find("+") != -1:
						modes.split("+")[0]
						
					if modes.find("B") != -1:
						if self.gateway(target):
							self.query("delete from gateway where uid = ?", target)
							self.vhost(target)

	def userflags(self, target):
		user = self.auth(target)
		
		if user == 0:
			user = target
			
		for data in self.query("select flags from users where name = ?", user):
			return data["flags"]

	def userflag(self, target, flag):
		user = self.auth(target)
		
		if self.ison(user):
			for data in self.query("select flags from users where name = ?", user):
				if str(data["flags"]).find(flag) != -1:
					return True
		else:
			if flag == "n":
				return True
				
		return False

	def msg(self, target, text=" ", action=False, uid=""):
		source = self.bot
		
		if uid != "":
			source = uid
			
		if self.userflag(target, "n") and not action:
			self.send(":%s NOTICE %s :%s" % (source, target, text))
		elif not self.userflag(target, "n") and not action:
			self.send(":%s PRIVMSG %s :%s" % (source, target, text))
		else:
			self.send(":%s PRIVMSG %s :\001ACTION %s\001" % (self.bot, target, text))

	def mode(self, target, mode):
		self.send(":%s SVSMODE %s %s" % (self.bot, target, mode))
		
		if target.startswith("#"):
			if self.chanflag("l", target):
				self.log(self.bot_nick, "mode", target, mode)

	def meta(self, target, meta, content):
		self.send(":%s METADATA %s %s :%s" % (self.services_id, target, meta, content))

	def auth(self, target):
		for data in self.query("select account from online where uid = ? and account != ''", target):
			return data["account"]
			
		return 0

	def sid(self, account):
		uids = list()
		
		for data in self.query("select uid from online where account = ?", account):
			uids.append(data["uid"])
			
		return uids

	def memo(self, user):
		for data in self.query("select source,message from memo where user = ?", user):
			online = False
			
			for source in self.sid(user):
				online = True
				self.msg(source, "[Memo] From: %s, Message: %s" % (data["source"], data["message"]))
				
			if online:
				self.query("delete from memo where user = ? and source = ? and message = ?", user, data["source"], data["message"])

	def chanexist(self, channel):
		for data in self.query("select name from channelinfo where name = ?", channel):
			return True
			
		return False
		
	def gettopic(self, channel):
		if self.chanexist(channel):
			for data in self.query("select topic from channelinfo where name = ?", channel):
				return data["topic"]
				
		return ""

	def join(self, channel):
		if self.chanexist(channel) and not self.suspended(channel):
			self.send(":%s JOIN %s" % (self.services_id + bots.get("3", "uuid"), channel))
			self.mode(channel, "+ryo {0} {0}".format(self.services_id + bots.get("3", "uuid")))

	def statistics(self):
		stats = dict()
		
		for data in self.query("select * from statistics"):
			stats[data["attribute"]] = data["value"]
			
		return stats

	def killcount(self):
		kills = int(self.statistics()["kills"])
		kills += 1
		self.query("update statistics set `value` = ? where attribute = 'kills'", kills)
		return kills

	def kickcount(self):
		kicks = int(self.statistics()["kicks"])
		kicks += 1
		self.query("update statistics set `value` = ? where attribute = 'kicks'", kicks)
		return kicks

	def kill(self, target, reason="You're violating network rules"):
		if not self.isoper(self.uid(target)):
			self.send_serv("KILL %s :Killed (*.%s (%s (#%s)))" % (self.uid(target), self.getservicedomain(), reason, str(self.killcount())))

	def vhost(self, target):
		if not self.gateway(target):
			entry = False
			
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", self.auth(target)):
				entry = True
				vhost = str(data["vhost"])
				
				if str(data["vhost"]).find("@") != -1:
					vident = vhost.split("@")[0]
					vhost = vhost.split("@")[1]
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, vident))
					
				self.send(":%s CHGHOST %s %s" % (self.bot, target, vhost))
				self.msg(target, "Your vhost %s has been activated" % data["vhost"])
				
			if not entry:
				if not self.userflag(target, "x"):
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, self.getident(target)))
					self.send(":%s CHGHOST %s %s" % (self.bot, target, self.gethost(target)))
				else:
					self.send(":%s CHGIDENT %s %s" % (self.bot, target, self.getident(target)))
					self.send(":%s CHGHOST %s %s.users.%s" % (self.bot, target, self.auth(target), self.getservicedomain()))
		else:
			username = self.userhost(target).split("@")[0]
			self.send(":%s CHGIDENT %s %s" % (self.bot, target, username))
			crypthost = self.encode_md5(target + ":" + self.nick(target) + "!" + self.userhost(target))
			self.send(":%s CHGHOST %s %s.gateway.%s" % (self.services_id, target, crypthost, self.getservicedomain()))
			self.msg(target, "Your vhost %s.gateway.%s has been activated" % (crypthost, self.getservicedomain()))
			
	def getservicedomain(self):
		rawdomain = self.services_name.split(".")[-2:]
		fulldomain = '.'.join(rawdomain)
		return fulldomain

	def flag(self, target, channel = ""):
		account = self.auth(target)
		if account != 0:
			if channel != "":
				for flag in self.query("select flag,channel from channels where user = ? and channel = ?", account, channel):
					if flag["flag"] == "n" or flag["flag"] == "q":
						self.mode(flag["channel"], "+qo " + target + " " + target)
					elif flag["flag"] == "a":
						self.mode(flag["channel"], "+ao " + target + " " + target)
					elif flag["flag"] == "o":
						self.mode(flag["channel"], "+o " + target)
					elif flag["flag"] == "h":
						self.mode(flag["channel"], "+h " + target)
					elif flag["flag"] == "v":
						self.mode(flag["channel"], "+v " + target)
					elif flag["flag"] == "b":
						self.kick(flag["channel"], target, "Banned.")
			else:
				for flag in self.query("select flag,channel from channels where user = ? order by channel", account):
					if flag["flag"] == "n" or flag["flag"] == "q":
						self.mode(flag["channel"], "+qo " + target + " " + target)
					elif flag["flag"] == "a":
						self.mode(flag["channel"], "+ao " + target + " " + target)
					elif flag["flag"] == "o":
						self.mode(flag["channel"], "+o " + target)
					elif flag["flag"] == "h":
						self.mode(flag["channel"], "+h " + target)
					elif flag["flag"] == "v":
						self.mode(flag["channel"], "+v " + target)
					elif flag["flag"] == "b":
						self.kick(flag["channel"], target, "Banned.")

	def autojoin(self, target):
		user = self.auth(target)
		
		if self.ison(user):
			if self.userflag(target, "a"):
				for data in self.query("select channel,flag from channels where user = ?", user):
					channel = data["channel"]
					flag = data["flag"]
					
					if flag == "n" or flag == self.bot_nick or flag == "a" or flag == "o" or flag == "h" or flag == "v":
						self.send(":%s SVSJOIN %s %s" % (self.bot, target, channel))

	def getflag(self, target, channel):
		for data in self.query("select account from online where uid = ?", target):
			for flag in self.query("select flag from channels where channel = ? and user = ?", channel, data["account"]):
				return flag["flag"]
				
		return 0

	def chanflag(self, flag, channel):
		for data in self.query("select flags from channelinfo where name = ?", channel):
			if data["flags"].find(flag) != -1:
				return True
				
		return False

	def isoper(self, target):
		if self.isserv(target):
			return True
			
		isoper = False
		
		for data in self.query("select * from opers where uid = ?", target):
			isoper = True
			
		return isoper

	def encode(self, string):
		return hashlib.sha512(string).hexdigest()

	def encode_md5(self, string):
		return hashlib.md5(string).hexdigest()

	def mail(self, receiver, message):
		try:
			mail = smtplib.SMTP('127.0.0.1', 25)
			mail.sendmail(self.email, ['%s' % receiver], message)
			mail.quit()
		except Exception,e:
			debug(red("*") + " <<MAIL-ERROR>> "+str(e))

	def log(self, source, msgtype, channel, text=""):
		try:
			if msgtype.lower() == "mode" and len(text.split()) > 1:
				nicks = list()
				
				for nick in text.split()[1:]:
					nicks.append(self.nick(nick))
					
				text = "{text} {nicks}".format(text=text.split()[0], nicks=' '.join(nicks))
				
			if source == self.bot_nick:
				sender = self.bot_nick+"!"+self.bot_user+"@"+self.services_name
			else:
				hostmask = self.hostmask(source)
				sender = hostmask[len(hostmask)-1]
				
			result = self.query("SELECT COUNT(*) FROM `logs` WHERE `channel` = ?", channel)
			for row in result:
				if row["COUNT(*)"] == 50:
					self.query("DELETE FROM `logs` WHERE `channel` = ? LIMIT 1", channel)
					
			self.query("INSERT INTO `logs` (`channel`, `sender`, `action`, `message`) VALUES (?, ?, ?, ?)", channel, sender, msgtype.upper(), text)
		except:
			pass

	def showlog(self, source, channel):
		try:
			escaped_actions = list()
			escaped_actions.append("JOIN")
			escaped_actions.append("PART")
			escaped_actions.append("QUIT")
			escaped_actions.append("MODE")
			escaped_actions.append("KICK")
			escaped_actions.append("TOPIC")
			
			self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE "+channel+" :*** Log start")
			
			result = self.query("SELECT `channel`, `sender`, `action`, `message` FROM `logs` WHERE `channel` = ? ORDER BY `id`", channel)
			for row in result:
				escaped_action = False
				
				for action in escaped_actions:
					if row["action"] == action:
						escaped_action = True
						
				if not escaped_action:
					if row["action"] == "PRIVMSG":
						row["action"] = "NOTICE"
						
					self.push(source, row["sender"] + " " + row["action"] + " " + row["channel"] + " " + row["message"])
				else:
					message = row["sender"] + " " + row["action"] + " " + row["channel"] + " " + row["message"]
					self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE " + row["channel"] + " :" + message)
					
			self.push(source, self.bot_nick + "!" + self.bot_user + "@" + self.services_name + " NOTICE "+channel+" :*** Log end")
		except:
			pass

	def convert_timestamp(self, timestamp):
		dif = int(timestamp)
		days = 0
		hours = 0
		minutes = 0
		seconds = 0
		
		if dif == 86400 or dif > 86400:
			days = int(dif)/86400
			dif = int(dif)-int(days)*86400
			
		if dif == 3600 or dif > 3600:
			hours = int(dif)/3600
			dif = int(dif)-int(hours)*3600
			
		if dif == 60 or dif > 60:
			minutes = int(dif)/60
			dif = int(dif)-int(minutes)*60
			
		seconds = dif
		
		if days > 0:
			return "%s days %s hours %s minutes %s seconds" % (days, hours, minutes, seconds)
			
		if hours > 0:
			return "%s hours %s minutes %s seconds" % (hours, minutes, seconds)
			
		if minutes > 0:
			return "%s minutes %s seconds" % (minutes, seconds)
			
		return "%s seconds" % seconds

	def kick(self, channel, target, reason="Requested."):
		uid = self.uid(target)
		
		if self.onchan(channel, target):
			if self.chanflag("c", channel):
				self.send(":{uid} KICK {channel} {target} :{reason} (#{count})".format(uid=self.bot, target=uid, channel=channel, reason=reason, count=str(self.kickcount())))
			else:
				self.send(":{uid} KICK {channel} {target} :{reason}".format(uid=self.bot, target=uid, channel=channel, reason=reason))
				self.kickcount()
				
			self.query("delete from chanlist where channel = ? and uid = ?", channel, uid)

	def userlist(self, channel):
		uid = list()
		
		for user in self.query("select uid from chanlist where channel = ?", channel):
			uid.append(user["uid"])
			
		return uid

	def onchan(self, channel, target):
		uid = self.uid(target)
		
		for data in self.query("select * from chanlist where channel = ? and uid = ?", channel, uid):
			return True
			
		return False

	def getident(self, target):
		uid = self.uid(target)
		
		for data in self.query("select username from online where uid = ?", uid):
			return data["username"]
			
		return 0

	def gethost(self, target):
		uid = self.uid(target)
		
		for data in self.query("select host from online where uid = ?", uid):
			return data["host"]
			
		return 0

	def hostmask(self, target):
		uid = self.uid(target)
		masks = list()
		nick = None
		username = None
		account = self.auth(uid)
		
		for data in self.query("select nick,username,host from online where uid = ?", uid):
			nick = data["nick"]
			username = data["username"]
			masks.append(data["nick"]+"!"+data["username"]+"@"+data["host"])
			
		if self.auth(uid) != 0:
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", account):
				if str(data["vhost"]).find("@") != -1:
					masks.append(nick+"!"+data["vhost"])
				else:
					masks.append(nick+"!"+username+"@"+data["vhost"])
					
			if self.userflag(uid, "x"):
				masks.append(nick + "!" + username + "@" + account + ".users." + self.getservicedomain())
					
		return masks

	def enforceban(self, channel, target):
		if target != "*!*@*":
			for user in self.userlist(channel):
				if self.gateway(user):
					crypthost = self.encode_md5(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+self.getservicedomain()
					
					if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, target):
						self.mode(channel, "+b "+target)
						self.kick(channel, user, "Banned.")
						
				for hostmask in self.hostmask(user):
					if fnmatch.fnmatch(hostmask, target):
						self.mode(channel, "+b "+target)
						self.kick(channel, user, "Banned.")

	def enforcebans(self, channel):
		for data in self.query("select ban from banlist where channel = ?", channel):
			if data["ban"] != "*!*@*":
				for user in self.userlist(channel):
					if self.gateway(user):
						crypthost = self.encode_md5(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+'.'.join(self.services_name.split(".")[-2:])
						
						
						if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, data["ban"]):
							self.mode(channel, "+b "+data["ban"])
							self.kick(channel, user, "Banned.")
							
					for hostmask in self.hostmask(user):
						if fnmatch.fnmatch(hostmask, data["ban"]):
							self.mode(channel, "+b "+data["ban"])
							self.kick(channel, user, "Banned.")

	def checkbans(self, channel, bans):
		if self.chanflag("e", channel):
			for ban in bans.split():
				if fnmatch.fnmatch(ban, "*!*@*") and ban != "*!*@*":
					for user in self.userlist(channel):
						if self.gateway(user):
							crypthost = self.encode(user + ":" + self.nick(user) + "!" + self.userhost(user))+".gateway."+'.'.join(self.services_name.split(".")[-2:])
							
							if fnmatch.fnmatch(self.nick(user)+"!"+self.userhost(user).split("@")[0]+"@"+crypthost, ban):
								self.kick(channel, user, "Banned.")
								
						for hostmask in self.hostmask(user):
							if fnmatch.fnmatch(hostmask, ban):
								self.kick(channel, user, "Banned.")
								
						for ip in self.getip(user):
							if fnmatch.fnmatch("*!*@"+ip, ban):
								self.kick(channel, user, "Banned.")
				elif ban == "*!*@*":
					self.mode(channel, "-b *!*@*")

	def getip(self, target):
		uid = self.uid(target)
		
		for data in self.query("select address from online where uid = ?", uid):
			return data["address"]
			
		return 0

	def gline(self, target, reason="", bantime="1800", addentry=False):
		uid = self.uid(target)
		
		if uid != self.bot and target.lower() != self.bot_nick.lower() and not self.isoper(uid):
			ip = self.getip(uid)
			
			if addentry:
				rows = int(self.query_row("SELECT COUNT(*) FROM `glines` WHERE `mask` = ?", "*@" + ip)["COUNT(*)"])
				
				if rows == 0:
					etime = int(time.time()) + int(bantime)
					self.query("INSERT INTO `glines` (`mask`, `timestamp`) VALUES (?, ?)", "*@" + ip, etime)
					
			for data in self.query("select uid from online where address = ?", self.getip(uid)):
				self.send_serv("KILL "+data["uid"]+" :G-lined")
				
			self.send_serv("GLINE *@"+ip+" "+str(bantime)+" :"+reason)
			self.send_to_op("#G-line# *@" + ip + " added (" + self.convert_timestamp(int(bantime)) + ")")

	def suspended(self, channel):
		for data in self.query("select reason from suspended where channel = ?", channel):
			return data["reason"]
			
		return False

	def userhost(self, target):
		uid = self.uid(target)
		
		for data in self.query("select username,host from online where uid = ?", uid):
			return data["username"]+"@"+data["host"]
			
		return 0

	def getvhost(self, target):
		for data in self.query("select vhost from vhosts where user = ? and active = '1'", target):
			return data["vhost"]
			
		if self.userflag(target, "x"):
			return "{0}.users.{1}".format(self.auth(target), self.getservicedomain())
			
		return "None"

	def scanport(self, host, port):
		try:
			scpo = socket.socket()
			scpo.settimeout(1)
			scpo.connect((str(host), int(port)))
			scpo.close()
			return True
		except socket.error:
			return False

	def fantasy(self, channel):
		if self.chanexist(channel):
			for data in self.query("select fantasy from channelinfo where name = ?", channel):
				return data["fantasy"]
				
		return False

	def getconns(self, address):
		result = self.query("SELECT COUNT(*) FROM `online` WHERE `address` = ?", address)
		for row in result:
			return int(row["COUNT(*)"])
			
		return 0

	def checkconnection(self, uid):
		if self.isserv(uid):
			return False
			
		user_ip = self.getip(uid)
		user_host = self.gethost(uid)
		user_name = self.userhost(uid).split("@")[0]
		timestamp = time.time()
		
		if user_ip == 0:
			return False
			
		limit = 3
		result = self.query("SELECT `limit` FROM `trust` WHERE (`address` = ? OR `address` = ?) AND `timestamp` > ?", user_ip, user_host, timestamp)
		for row in result:
			limit = int(row["limit"])
			
			if user_name.startswith("~"):
				self.msg(uid, "You ignored the trust rules. Please run an identd before you connect again.")
				self.gline(uid, "Ignored trust rules. Run an identd before connecting again.", addentry=True)
				return 0
				
		if self.getconns(user_ip) > limit:
			self.gline(uid, "Connection limit ({0}) reached".format(str(limit)), addentry=True)
			return True
		elif self.getconns(user_ip) == limit:
			for row in self.query("SELECT `uid` FROM `online` WHERE `address` = ? OR `host` = ?", user_ip, user_host):
				self.msg(nick["uid"], "Your IP is scratching the connection limit. If you need more connections please request a trust.")
				
		return False

	def isserv(self, uid):
		uid = self.uid(uid)
		if uid.startswith(self.services_id):
			return True
			
		return False

	def opertype(self, uid):
		for row in self.query("SELECT `opertype` FROM `opers` WHERE `uid` = ?", uid):
			return row["opertype"]
			
		return None

	def isoptype(self, uid, type):
		for row in self.query("SELECT `uid` FROM `opers` WHERE `uid` = ? AND `opertype` = ?", uid, type):
			return True
			
		return False

class error(Exception):
	def __init__(self, value):
		self.value = value
		self.email = config.get("OTHER", "email")
	def __str__(self):
		try:
			mail = smtplib.SMTP('127.0.0.1', 25)
			mail.sendmail(self.email, ['hosting@chiruclan.de'], str(self.value))
			mail.quit()
		except:
			pass
		finally:
			return repr(self.value)

if __name__ == "__main__":
	try:
		while True:
			__version__ = open("version", "r").read()
			
			if len(sys.argv) == 1:
				__config__ = "config.cfg"
			else:
				__config__ = sys.argv[1]
				
			time.sleep(9)
			print(green("*") + " chiruclan.de IRC services (" + __version__ + ") started (config: " + __config__ + ")")
			Services().run()
			print(red("*") + " chiruclan.de IRC services (" + __version__ + ") stopped (config: " + __config__ + ")")
			
			time.sleep(1)
	except Exception,e:
		print(red("*") + " " + str(e))
	except KeyboardInterrupt:
		print(red("*") + " Aborting ... STRG +C")
