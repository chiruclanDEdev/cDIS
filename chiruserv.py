#!/usr/bin/env python

# Copyright by ChiruServ 2012-2013

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
import commands
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
		config.read("config.cfg")
	else:
		config.read(sys.argv[1])
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
		self.bot = "%sAAAAAA" % self.services_id
		self.bot_nick = config.get("BOT", "nick").split()[0]
		self.bot_user = config.get("BOT", "user").split()[0]
		self.bot_real = config.get("BOT", "real")
		
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
			self.query("truncate temp_nick")
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
		self.bot_nick = config.get("BOT", "nick").split()[0]
		self.bot_user = config.get("BOT", "user").split()[0]
		self.bot_real = config.get("BOT", "real")
		self.con = con
		
	def shell(self, text):
		subprocess.Popen(text+" >> /dev/null", shell=True).wait()
	
	def onData(self, data):
		try:
			if data.split()[1] == "PING":
				self.send(":%s PONG %s %s" % (self.services_id, self.services_id, data.split()[2]))
				self.send(":%s PING %s %s" % (self.services_id, self.services_id, data.split()[2]))
			elif data.split()[1] == "ENDBURST" and not _connected:
				self.send(":%s UID %s %s %s %s %s %s %s %s +Ik :%s" % (self.services_id, self.bot, time.time(), self.bot_nick, self.services_name, self.services_name, self.bot_user, self.services_address, time.time(), self.bot_real))
				__builtin__._connected = True
				self.send(":%s OPERTYPE Service" % self.bot)
				self.meta(self.bot, "accountname", self.bot_nick)
				self.msg("$*", "Services are now back online. Have a nice day :)")
				
				for channel in self.query("select name,modes,topic from channelinfo"):
					self.join(str(channel["name"]))
					
					if self.chanflag("m", channel["name"]):
						self.mode(channel["name"], channel["modes"])
						
					if self.chanflag("t", channel["name"]):
						self.send(":{0} TOPIC {1} :{2}".format(self.bot, channel["name"], channel["topic"]))
						
						if self.chanflag("l", channel["name"]):
							self.log(self.bot_nick, "topic", channel["name"], ":"+channel["topic"])
							
				for mods in dir(modules):
					if os.access("modules/" + mods + ".py", os.F_OK):
						exec("m_class = modules.{0}.{0}().MODULE_CLASS".format(mods))
						self.query("DELETE FROM `modules` WHERE `name` = ?", mods)
						self.query("INSERT INTO `modules` (`name`, `class`) VALUES (?, ?)", mods, m_class)
			else:
				for modules in query("SELECT * FROM `modules` WHERE `class` = ?", data.split()[1]):
					if os.access("modules/" + modules["name"] + ".py", os.F_OK):
						exec("m_class = modules.{0}.{0}().MODULE_CLASS".format(module["name"]))
						if m_class.lower() == data.split()[1].lower():
							exec("thread.start_new_thread(modules.{0}.{0}().onData, ('{1}',))".format(module["name"], data))
					
			if data.split()[1] == "PRIVMSG":
				if data.split()[2] == self.bot:
					iscmd = False
					cmd = data.split()[3][1:]
					
					if os.access("commands/"+cmd.lower()+".py", os.F_OK):
						iscmd = True
						exec("oper = commands.%s.%s().NEED_OPER" % (cmd.lower(), cmd.lower()))
						
						if oper == 0:
							exec("cmd_auth = commands.%s.%s().NEED_AUTH" % (cmd.lower(), cmd.lower()))
							
							if not cmd_auth:
								if len(data.split()) == 4:
									exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', ''))" % (cmd.lower(), cmd.lower(), data.split()[0][1:]))
								elif len(data.split()) > 4:
									exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', '%s'))" % (cmd.lower(), cmd.lower(), data.split()[0][1:], ' '.join(data.split()[4:]).replace("'", "\\'")))
							elif cmd_auth:
								if self.auth(data.split()[0][1:]):
									if len(data.split()) == 4:
										exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', ''))" % (cmd.lower(), cmd.lower(), data.split()[0][1:]))
									elif len(data.split()) > 4:
										exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', '%s'))" % (cmd.lower(), cmd.lower(), data.split()[0][1:], ' '.join(data.split()[4:]).replace("'", "\\'")))
								else:
									self.msg(data.split()[0][1:], "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()))
						elif oper == 1:
							if self.isoper(data.split()[0][1:]):
								if len(data.split()) == 4:
									exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', ''))" % (cmd.lower(), cmd.lower(), data.split()[0][1:]))
								if len(data.split()) > 4:
									exec("thread.start_new_thread(commands.%s.%s().onCommand,('%s', '%s'))" % (cmd.lower(), cmd.lower(), data.split()[0][1:], ' '.join(data.split()[4:]).replace("'", "\\'")))
							else:
								self.msg(data.split()[0][1:], "You do not have sufficient privileges to use '{0}'".format(data.split()[3][1:].upper()))
								
					if not iscmd:
						self.message(data.split()[0][1:], ' '.join(data.split()[3:])[1:])
						
				if data.split()[2].startswith("#") and self.chanflag("f", data.split()[2]) and self.chanexist(data.split()[2]):
					if data.split()[3][1:].startswith(self.fantasy(data.split()[2])):
						iscmd = False
						fuid = data.split()[0][1:]
						cmd = self.fantasy(data.split()[2])
						
						if len(data.split()[3]) > int(1+len(self.fantasy(data.split()[2]))):
							fchan = data.split()[2]
							cmd = data.split()[3][int(1+len(self.fantasy(fchan))):]
							
							if len(data.split()) > 4:
								args = ' '.join(data.split()[4:]).replace("'", "\\'")
								
							if os.access("commands/"+cmd.lower()+".py", os.F_OK):
								iscmd = True
								exec("oper = commands.%s.%s().NEED_OPER" % (cmd.lower(), cmd.lower()))
								
								if oper == 0:
									exec("cmd_auth = commands.%s.%s().NEED_AUTH" % (cmd.lower(), cmd.lower()))
									
									if not cmd_auth:
										if len(data.split()) == 4:
											exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', ''))" % (cmd.lower(), cmd.lower(), fuid, fchan))
										elif len(data.split()) > 4:
											exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', '%s'))" % (cmd.lower(), cmd.lower(), fuid, fchan, args))
									elif cmd_auth:
										if self.auth(fuid):
											if len(data.split()) == 4:
												exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', ''))" % (cmd.lower(), cmd.lower(), fuid, fchan))
											elif len(data.split()) > 4:
												exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', '%s'))" % (cmd.lower(), cmd.lower(), fuid, fchan, args))
										else:
											self.msg(fuid, "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()))
								elif oper == 1:
									if self.isoper(fuid):
										if len(data.split()) == 4:
											exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', ''))" % (cmd.lower(), cmd.lower(), fuid, fchan))
										elif len(data.split()) > 4:
											exec("thread.start_new_thread(commands.%s.%s().onFantasy,('%s', '%s', '%s'))" % (cmd.lower(), cmd.lower(), fuid, fchan, args))
									else:
										self.msg(fuid, "You do not have sufficient privileges to use '{0}'".format(cmd.upper()))
										
						if not iscmd:
							if len(data.split()) == 4:
								self.message(fuid, cmd)
							elif len(data.split()) > 4:
								self.message(fuid, cmd + " " + args)
								
		except Exception:
			et, ev, tb = sys.exc_info()
			e = "{0}: {1} (Line #{2})".format(et, ev, traceback.tb_lineno(tb))
			debug(red("*") + " <<ERROR>> " + str(e))
			
	def metadata(self, uid, string, content):
		if string == "accountname":
			self.query("delete from temp_nick where nick = ?", uid)
			self.query("insert into temp_nick values (?, ?)", uid, content)
			self.msg(uid, "You are now logged in as %s" % content)
			self.vhost(uid)
			self.flag(uid)
			self.memo(content)

	def message(self, source, text):
		try:
			if len(text.split()) > 0:
				cmd = text.lower().split()[0]
				arg = list()
				args = ""
				
				if len(text.split()) > 1:
					arg = text.split()[1:]
					args = ' '.join(text.split()[1:])
					
				if cmd == "help":
					self.msg(source, "The following commands are available to you.")
					
					if len(args) != 0:
						if fnmatch.fnmatch("help", "*" + args.lower() + "*"):
							self.help(source, "HELP", "Shows information about all commands that are available to you")
					else:
						self.help(source, "HELP", "Shows information about all commands that are available to you")
						
					for command in dir(commands):
						if command != "__init__" and os.access("commands/"+command+".py", os.F_OK):
							exec("cmd_auth = commands.%s.%s().NEED_AUTH" % (command, command))
							exec("cmd_oper = commands.%s.%s().NEED_OPER" % (command, command))
							exec("cmd_help = commands.%s.%s().HELP" % (command, command))
							
							if not cmd_auth and not cmd_oper:
								if len(args) != 0:
									if fnmatch.fnmatch(command.lower(), "*" + args.lower() + "*"):
										self.help(source, command, cmd_help)
								else:
									self.help(source, command, cmd_help)
							elif cmd_auth and not cmd_oper and self.auth(source):
								if len(args) != 0:
									if fnmatch.fnmatch(command.lower(), "*" + args.lower() + "*"):
										self.help(source, command, cmd_help)
								else:
									self.help(source, command, cmd_help)
									
					if self.isoper(source):
						self.msg(source)
						self.msg(source, "For operators:")
						
						for command in dir(commands):
							if command != "__init__" and os.access("commands/"+command+".py", os.F_OK):
								exec("cmd_oper = commands.%s.%s().NEED_OPER" % (command, command))
								exec("cmd_help = commands.%s.%s().HELP" % (command, command))
								
								if cmd_oper and self.isoper(source):
									if len(args) != 0:
										if fnmatch.fnmatch(command.lower(), "*" + args.lower() + "*"):
											self.help(source, command, cmd_help)
									else:
										self.help(source, command, cmd_help)
										
						if len(args) != 0:
							if fnmatch.fnmatch("reload", "*" + args.lower() + "*"):
								self.help(source, "RELOAD", "Reloads the config")
						else:
							self.help(source, "RELOAD", "Reloads the config")
							
						if len(args) != 0:
							if fnmatch.fnmatch("update", "*" + args.lower() + "*"):
								self.help(source, "UPDATE", "Updates the services")
						else:
							self.help(source, "UPDATE", "Updates the services")
							
						if len(args) != 0:
							if fnmatch.fnmatch("quit", "*" + args.lower() + "*"):
								self.help(source, "QUIT", "Shutdowns the services")
						else:
							self.help(source, "QUIT", "Shutdowns the services")
							
						self.msg(source)
						
					self.msg(source, "End of list.")
				elif cmd == "reload" and self.isoper(source):
					config.read("config.cfg")
					self.debug = config.get("OTHER", "debug")
					self.email = config.get("OTHER", "email")
					self.regmail = config.get("OTHER", "regmail")
					reload(commands)
					reload(modules)
					
					self.query("TRUNCATE `modules`")
					for mods in dir(modules):
						if os.access("modules/" + mods + ".py", os.F_OK):
							exec("m_class = modules.{0}.{0}().MODULE_CLASS".format(mods))
							self.query("INSERT INTO `modules` (`name`, `class`) VALUES (?, ?)", mods, m_class)
							
					self.msg(source, "Done.")
				elif cmd == "update" and self.isoper(source):
					_web = urllib2.urlopen("https://bitbucket.org/ChiruclanDE/chiruserv/raw/master/version")
					_version = _web.read()
					_web.close()
					
					if open("version", "r").read() != _version:
						_updates = len(os.listdir("sql/updates"))
						_hash = self.encode(open("chiruserv.py", "r").read())
						_cmdlist = list()
						
						for cmds in dir(commands):
							if os.access("commands/"+cmds+".py", os.F_OK):
								_cmdlist.append(cmds)
								
						_modlist = list()
						
						for mods in dir(modules):
							if os.access("modules/" + mods + ".py", os.F_OK):
								_modlist.append(mods)
								
						self.msg(source, "{0} -> {1}".format(open("version", "r").read(), _version))
#						shell("git add config.cfg")
#						shell("git commit -m 'Save'")
						shell("git pull")
						_files = os.listdir("sql/updates")
						__updates = len(_files)
						
						if __updates > _updates:
							while _updates != __updates:
								_updates += 1
								
								for sql in _files:
									if sql.startswith(str(_updates)+"_"):
										self.msg(source, " - Insert '{0}'".format(sql))
										file = open("sql/updates/"+sql, "r")
										
										for line in file.readlines():
											self.query(line)
											
										file.close()
										
						if _hash != self.encode(open("chiruserv.py", "r").read()):
							self.msg(source, "Done.")
							self.msg(source, "Please note that you have to restart the services manually.")
						else:
							self.msg(source, "Reload ...")
							reload(commands)
							
							for cmds in _cmdlist:
								if not os.access("commands/"+cmds+".py", os.F_OK):
									exec("del commands."+cmds)
									exec("""del sys.modules["commands.%s"]""" % cmds)
									
							reload(modules)
									
							for mod in _modlist:
								if not os.access("modules/" + mod + ".py", os.F_OK):
									exec("del modules." + mod)
									exec("""del sys.modules["modules.%s"]""" % mod)
									
							self.query("TRUNCATE `modules`")
							
							for mods in dir(modules):
								if os.access("modules/" + mods + ".py", os.F_OK):
									exec("m_class = modules.{0}.{0}().MODULE_CLASS".format(mods))
									self.query("INSERT INTO `modules` (`name`, `class`) VALUES (?, ?)", mods, m_class)
									
							self.msg(source, "Done.")
					else:
						self.msg(source, "No update available.")
				elif cmd == "quit" and self.isoper(source):
					if os.access("chiruserv.pid", os.F_OK):
						if len(arg) == 0:
							msg = "Services are going offline."
							self.send(":%s QUIT :%s" % (self.bot, msg))
						else:
							self.send(":%s QUIT :%s" % (self.bot, args))
							
						self.send(":%s SQUIT %s" % (self.services_id, self.services_name))
						self.con.close()
						shell("sh chiruserv stop")
					else:
						self.msg(source, "You're running the debug mode. You cannot restart via commands!")
				else:
					self.msg(source, "Unknown command {0}. Please try HELP for more information.".format(text.split()[0].upper()))
			else:
				self.msg(source, "Unknown command NULL. Please try HELP for more information.")
		except Exception:
			self.msg(source, "An error has occured. The Development-Team has been notified about this problem.")
			et, ev, tb = sys.exc_info()
			e = "{0}: {1} (Line #{2})".format(et, ev, traceback.tb_lineno(tb))
			if self.email != "":
				self.mail("mechi.community@yahoo.de", "From: {0} <{1}>\nTo: ChiruServ Development <mechi.community@yahoo.de>\nSubject: Bug on {0}\n{2}".format(self.services_description, self.email, str(e)))
				
			debug(red("*") + " <<MSG-ERROR>> "+str(e))
			
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
			self.query("delete from temp_nick where nick = ?", uid)
			self.query("insert into temp_nick values (?, ?)", uid, content)
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

	def ison(self, user):
		for data in self.query("select * from temp_nick where user = ?", user):
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

	def msg(self, target, text=" ", action=False):
		if self.userflag(target, "n") and not action:
			self.send(":%s NOTICE %s :%s" % (self.bot, target, text))
		elif not self.userflag(target, "n") and not action:
			self.send(":%s PRIVMSG %s :%s" % (self.bot, target, text))
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
		for data in self.query("select user from temp_nick where nick = ?", target):
			return data["user"]
			
		return 0

	def sid(self, nick):
		nicks = list()
		
		for data in self.query("select nick from temp_nick where user = ?", nick):
			nicks.append(data["nick"])
			
		return nicks

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
			self.send(":%s JOIN %s" % (self.bot, channel))
			self.mode(channel, "+ryo {0} {0}".format(self.bot))

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
		if target.lower() != self.bot_nick.lower() and not self.isoper(self.uid(target)):
			self.send(":%s KILL %s :Killed (*.%s (%s (#%s)))" % (self.bot, target, self.getservicedomain(), reason, str(self.killcount())))

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
		for data in self.query("select user from temp_nick where nick = ?" % target):
			for flag in self.query("select flag from channels where channel = ? and user = ?", channel, data["user"]):
				return flag["flag"]
				
		return 0

	def chanflag(self, flag, channel):
		for data in self.query("select flags from channelinfo where name = ?", channel):
			if data["flags"].find(flag) != -1:
				return True
				
		return False

	def isoper(self, target):
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
				sender = self.nick(source)+"!"+self.userhost(source)
				
			file = open("logs/"+channel, "ab+")
			lines = file.readlines()
			
			if len(lines) > 100:
				file.close()
				file = open("logs/"+channel, "wb")
				i = 49
				
				while i != 0:
					file.write(lines[-i])
					i -= 1
					
				file.write(sender+" "+msgtype.upper()+" "+channel+" "+text+"\n")
			else:
				file.write(sender+" "+msgtype.upper()+" "+channel+" "+text+"\n")
				
			file.close()
		except:
			pass

	def showlog(self, source, channel):
		try:
			file = open("logs/"+channel, "rb")
			self.push(source, "!@ PRIVMSG "+channel+" :*** Log start")
			
			for line in file.readlines():
				if line.split()[1] != "PART" and line.split()[1] != "JOIN" and line.split()[1] != "QUIT":
					self.push(source, line.rstrip())
				else:
					self.push(source, "*!@ PRIVMSG "+channel+" :"+line.rstrip())
					
			self.push(source, "!@ PRIVMSG "+channel+" :*** Log end")
			file.close()
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
		
		for data in self.query("select nick,username,host from online where uid = ?", uid):
			nick = data["nick"]
			username = data["username"]
			masks.append(data["nick"]+"!"+data["username"]+"@"+data["host"])
			
		if self.auth(uid) != 0:
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", self.auth(uid)):
				if str(data["vhost"]).find("@") != -1:
					masks.append(nick+"!"+data["vhost"])
				else:
					masks.append(nick+"!"+username+"@"+data["vhost"])
					
			if self.userflag(uid, "x"):
				masks.append(nick + "!" + username + "@" + target + ".users." + self.getservicedomain())
					
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

	def gline(self, target, reason=""):
		uid = self.uid(target)
		
		if uid != self.bot and target.lower() != self.bot_nick.lower():
			ip = self.getip(uid)
			
			for data in self.query("select uid from online where address = ?", self.getip(uid)):
				self.send(":"+self.bot+" KILL "+data["uid"]+" :G-lined")
				
			self.send(":"+self.bot+" GLINE *@"+ip+" 1800 :"+reason)

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

class Module:
	import sys
	import os
	import time
	import hashlib
	import smtplib
	import _mysql
	import traceback
	import fnmatch
	import time
	import __builtin__
	
	HELP = "unknown"
	NEED_OPER = 0
	NEED_AUTH = 0
	MODULE_CLASS = "Command"

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
		self.bot = "%sAAAAAA" % self.services_id
		self.bot_nick = config.get("BOT", "nick").split()[0]
		self.bot_user = config.get("BOT", "user").split()[0]
		self.bot_real = config.get("BOT", "real")

	def onCommand(self, uid, arguments):
		pass

	def onFantasy(self, uid, channel, arguments):
		pass
		
	def onData(self, data):
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

	def metadata(self, uid, string, content):
		if string == "accountname":
			self.query("delete from temp_nick where nick = ?", uid)
			self.query("insert into temp_nick values (?, ?)", uid, content)
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

	def ison(self, user):
		for data in self.query("select * from temp_nick where user = ?", user):
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

	def msg(self, target, text=" ", action=False):
		if self.userflag(target, "n") and not action:
			self.send(":%s NOTICE %s :%s" % (self.bot, target, text))
		elif not self.userflag(target, "n") and not action:
			self.send(":%s PRIVMSG %s :%s" % (self.bot, target, text))
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
		for data in self.query("select user from temp_nick where nick = ?", target):
			return data["user"]
			
		return 0

	def sid(self, nick):
		nicks = list()
		
		for data in self.query("select nick from temp_nick where user = ?", nick):
			nicks.append(data["nick"])
			
		return nicks

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
			self.send(":%s JOIN %s" % (self.bot, channel))
			self.mode(channel, "+ryo {0} {0}".format(self.bot))

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
		if target.lower() != self.bot_nick.lower() and not self.isoper(self.uid(target)):
			self.send(":%s KILL %s :Killed (*.%s (%s (#%s)))" % (self.bot, target, self.getservicedomain(), reason, str(self.killcount())))

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
		for data in self.query("select user from temp_nick where nick = ?" % target):
			for flag in self.query("select flag from channels where channel = ? and user = ?", channel, data["user"]):
				return flag["flag"]
				
		return 0

	def chanflag(self, flag, channel):
		for data in self.query("select flags from channelinfo where name = ?", channel):
			if data["flags"].find(flag) != -1:
				return True
				
		return False

	def isoper(self, target):
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
				sender = self.nick(source)+"!"+self.userhost(source)
				
			file = open("logs/"+channel, "ab+")
			lines = file.readlines()
			
			if len(lines) > 100:
				file.close()
				file = open("logs/"+channel, "wb")
				i = 49
				
				while i != 0:
					file.write(lines[-i])
					i -= 1
					
				file.write(sender+" "+msgtype.upper()+" "+channel+" "+text+"\n")
			else:
				file.write(sender+" "+msgtype.upper()+" "+channel+" "+text+"\n")
				
			file.close()
		except:
			pass

	def showlog(self, source, channel):
		try:
			file = open("logs/"+channel, "rb")
			self.push(source, "!@ PRIVMSG "+channel+" :*** Log start")
			
			for line in file.readlines():
				if line.split()[1] != "PART" and line.split()[1] != "JOIN" and line.split()[1] != "QUIT":
					self.push(source, line.rstrip())
				else:
					self.push(source, "*!@ PRIVMSG "+channel+" :"+line.rstrip())
					
			self.push(source, "!@ PRIVMSG "+channel+" :*** Log end")
			file.close()
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
		
		for data in self.query("select nick,username,host from online where uid = ?", uid):
			nick = data["nick"]
			username = data["username"]
			masks.append(data["nick"]+"!"+data["username"]+"@"+data["host"])
			
		if self.auth(uid) != 0:
			for data in self.query("select vhost from vhosts where user = ? and active = '1'", self.auth(uid)):
				if str(data["vhost"]).find("@") != -1:
					masks.append(nick+"!"+data["vhost"])
				else:
					masks.append(nick+"!"+username+"@"+data["vhost"])
					
			if self.userflag(uid, "x"):
				masks.append(nick + "!" + username + "@" + target + ".users." + self.getservicedomain())
					
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

	def gline(self, target, reason=""):
		uid = self.uid(target)
		
		if uid != self.bot and target.lower() != self.bot_nick.lower():
			ip = self.getip(uid)
			
			for data in self.query("select uid from online where address = ?", self.getip(uid)):
				self.send(":"+self.bot+" KILL "+data["uid"]+" :G-lined")
				
			self.send(":"+self.bot+" GLINE *@"+ip+" 1800 :"+reason)

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

class error(Exception):
	def __init__(self, value):
		self.value = value
		self.email = config.get("OTHER", "email")
	def __str__(self):
		try:
			mail = smtplib.SMTP('127.0.0.1', 25)
			mail.sendmail(self.email, ['mechi.community@yahoo.de'], str(self.value))
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
			print(green("*") + " ChiruServ (" + __version__ + ") started (config: " + __config__ + ")")
			Services().run()
			print(red("*") + " ChiruServ (" + __version__ + ") stopped (config: " + __config__ + ")")
			
			time.sleep(1)
	except Exception,e:
		print(red("*") + " " + str(e))
	except KeyboardInterrupt:
		print(red("*") + " Aborting ... STRG +C")
