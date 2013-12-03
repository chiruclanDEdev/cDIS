#!/usr/bin/env python3

# chiruclan.de IRC services
# Copyright (C) 2012-2013  Chiruclan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import socket
import os
import configparser
import time
import hashlib
import smtplib
import psycopg2, psycopg2.extras
import subprocess
import urllib.request, urllib.error, urllib.parse
import traceback
import _thread
import fnmatch
import ssl
import threading
import modules
import builtins

def red(string):
  return("\033[91m" + string + "\033[0m")

def blue(string):
  return("\033[94m" + string + "\033[0m")

def green(string):
  return("\033[92m" + string + "\033[0m")

try:
  if not os.access("logs", os.F_OK):
    os.mkdir("logs")
  config = configparser.RawConfigParser()
  if len(sys.argv) == 1:
    config.read("configs/config.cfg")
  else:
    config.read(sys.argv[1])
    
  bots = configparser.RawConfigParser()
  bots.read("configs/" + config.get("INCLUDES", "bots"))
  
  with open(config.get("MAIL", "template"), 'r') as content_file:
    mail_template = content_file.read()
    
  mail_template = mail_template.replace("${LOGO}", config.get("MAIL", "logo"))
  mail_template = mail_template.replace("${LINK}", config.get("MAIL", "link"))
except Exception:
  et, ev, tb = sys.exc_info()
  print((red("*") + " <<ERROR>> {0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))))

def debug(text):
  if config.get("OTHER", "debug") == "1":
    print((str(text)))

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
    self.pgsql_host = config.get("PGSQL", "host")
    self.pgsql_port = config.getint("PGSQL", "port")
    self.pgsql_name = config.get("PGSQL", "name")
    self.pgsql_schema = config.get("PGSQL", "schema")
    self.pgsql_user = config.get("PGSQL", "user")
    self.pgsql_passwd = config.get("PGSQL", "passwd")
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
    
    try:
      self.db_interface = psycopg2.connect(database=self.pgsql_name, user=self.pgsql_user, password=self.pgsql_passwd, host=self.pgsql_host, port=self.pgsql_port)
      self.db_cursor = self.db_interface.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      self.db_cursor.execute("SET search_path TO %s;", (self.pgsql_schema,))
      self.db_interface.commit()
    except Exception:
      et, ev, tb = sys.exc_info()
      e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
      debug(red("*") + " <<ERROR>> " + str(e))
      sys.exit(1)
    
  def query(self, string, *args):
    try:
      debug(blue("*** => ") + " " + string % args)
      self.db_cursor.execute(string + ";", args)
      self.db_interface.commit()
      
      if self.db_cursor.rowcount > 0 and string.lower().find('select ') != -1:
        result = list()
        rows = self.db_cursor.fetchall()
        debug(green("*** <= ") + " " + str(rows))
        for row in rows:
          result.append(dict(row))
          
        return result
    except psycopg2.DatabaseError as e:
      self.db_interface.rollback()
      et, ev, tb = sys.exc_info()
      e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
      debug(red("*") + " <<ERROR>> " + str(e))
      
    return list()
    
  def send(self, text):
    self.con.send(bytes(text+"\n", "UTF-8"))
    debug(blue("*") + " " + text)

  def run(self):
    try:
      self.query("TRUNCATE opers")
      self.query("TRUNCATE online")
      self.query("TRUNCATE chanlist")
      self.query("TRUNCATE metadata")
      self.query("TRUNCATE modules")
      self.query("ALTER SEQUENCE modules_id_seq RESTART WITH 1")
      self.query("UPDATE ircd_opers SET hostname = 'root@localhost'")
      
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
      builtins.con = self.con
      builtins.spamscan = {}
      builtins._connected = False
      builtins.config = config
      builtins.bots = bots
      builtins.mail_template = mail_template
      builtins.db_interface = self.db_interface
      
      for mod in dir(modules):
        if os.access("modules/" + mod + ".py", os.F_OK):
          moduleToCall = getattr(modules, mod)
          classToCall = getattr(moduleToCall, mod)()
          
          if classToCall.MODULE_CLASS == "SCHEDULE":
            methodToCall = getattr(classToCall, "runSchedule")
            _thread.start_new_thread(methodToCall, ())
            
          self.query("INSERT INTO modules (name, class, oper, auth, command, help, bot) VALUES (%s, %s, %s, %s, %s, %s, %s)", mod, classToCall.MODULE_CLASS, classToCall.NEED_OPER, classToCall.NEED_AUTH, classToCall.COMMAND, classToCall.HELP, classToCall.BOT_ID)
          
      while 1:
        recv = self.con.recv(25600)
        
        if not recv:
          return 1
          
        for data in recv.splitlines():
          data = data.decode("UTF-8")
          if data.strip() != "":
            debug(green("*") + " " + data)
            _thread.start_new_thread(cDISModule().onInternal, (data.strip(),))
          
    except Exception:
      et, ev, tb = sys.exc_info()
      e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
      debug(red("*") + " <<ERROR>> " + str(e))

class cDISModule:
  import sys
  import socket
  import os
  import configparser
  import time
  import hashlib
  import smtplib
  import psycopg2, psycopg2.extras
  import subprocess
  import urllib.request, urllib.error, urllib.parse
  import traceback
  import _thread
  import fnmatch
  import builtins
  
  HELP = ''
  NEED_OPER = 0
  NEED_AUTH = 0
  MODULE_CLASS = ''
  COMMAND = ''
  BOT_ID = '0'
  TIMER = 0

  def __init__(self):
    self.con = con
    self.bots = bots
    
    self.pgsql_schema = config.get("PGSQL", "schema")
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
    
    self.bot = self.services_id + bots.get(self.BOT_ID, "uuid")
    self.bot_nick = bots.get(self.BOT_ID, "nick")
    self.bot_user = bots.get(self.BOT_ID, "user")
    self.bot_real = bots.get(self.BOT_ID, "real")
    
    self.oper_not = config.getboolean("OPERS", "notifications")
    
    self.mail_template = mail_template
    
    self.db_cursor = db_interface.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    self.db_cursor.execute("SET search_path TO %s;", (self.pgsql_schema,))
    db_interface.commit()
    
  def shell(self, text):
    subprocess.Popen(text+" >> /dev/null", shell=True).wait()
  
  def onInternal(self, data):
    try:
      if data.split()[1] == "PING":
        self.send(":%s PONG %s %s" % (self.services_id, self.services_id, data.split()[2]))
        self.send(":%s PING %s %s" % (self.services_id, self.services_id, data.split()[2]))
      elif data.split()[1] == "ENDBURST" and not _connected:
        self.send_serv("ENDBURST")
        builtins._connected = True
        
        for bot in bots.sections():
          botuid = self.services_id + bots.get(bot, "uuid")
          self.send_serv("UID {0} {1} {2} {3} {4} {5} {6} {7} +Ik :{8}".format(botuid, int(time.time()), bots.get(bot, "nick"), self.services_name, self.services_name, bots.get(bot, "user"), self.services_address, int(time.time()), bots.get(bot, "real")))
          self.send(":%s OPERTYPE Service" % botuid)
          self.SetMetadata(botuid, "accountname", bots.get(bot, "nick"))
          
        self.msg("$*", "Services are now back online. Have a nice day :)")
        
        self.bot = self.services_id + bots.get("3", "uuid")
        for channel in self.query("select name,modes,topic from channelinfo"):
          self.join(str(channel["name"]))
          
          if self.chanflag("m", channel["name"]):
            self.mode(channel["name"], channel["modes"])
            
          if self.chanflag("t", channel["name"]):
            self.send(":{0} TOPIC {1} :{2}".format(self.bot, channel["name"], channel["topic"]))
            
        self.bot = self.services_id + bots.get(self.BOT_ID, "uuid")
      else:
        for module in self.query("SELECT * FROM modules WHERE class = %s", data.split()[1]):
          if os.access("modules/" + module["name"] + ".py", os.F_OK):
            moduleToCall = getattr(modules, module["name"])
            classToCall = getattr(moduleToCall, module["name"])()
            
            if classToCall.MODULE_CLASS.lower() == data.split()[1].lower():
              methodToCall = getattr(classToCall, "onData")
              _thread.start_new_thread(methodToCall, (data, ))
              
      if data.split()[1] == "PRIVMSG":
        for bot in bots.sections():
          botuid = self.services_id + bots.get(bot, "uuid")
          
          if data.split()[2] == botuid:
            cmd = data.split()[3][1:]
            if self.isoper(data.split()[0][1:]): isoper = 1
            else: isoper = 0
            if self.auth(data.split()[0][1:]): isauth = 1
            else: isauth = 0
            
            if cmd.lower() == "help":
              self.bot = self.services_id + bots.get(bot, "uuid")
              
              source = data.split()[0][1:]
              args = ' '.join(data.split()[4:])
              arg = args.split()
              self.msg(source, "The following commands are available to you.")
              
              if len(arg) == 0:
                self.help(source, "HELP", "Shows information about all commands that are available to you")
                
                for command in self.query("SELECT * FROM modules WHERE class = 'COMMAND' AND bot = %s AND auth <= %s AND oper <= %s ORDER BY command", bot, isauth, isoper):
                  if os.access("modules/"+command["name"]+".py", os.F_OK):
                    self.help(source, command["command"], command["help"])
              else:
                if fnmatch.fnmatch("help", "*" + args.lower() + "*"):
                  self.help(source, "HELP", "Shows information about all commands that are available to you")
                  
                for command in self.query("SELECT * FROM modules WHERE class = 'COMMAND' AND bot = %s AND auth <= %s AND oper <= %s AND command LIKE %s ORDER BY command", bot, isauth, isoper, '%' + args + '%'):
                  if os.access("modules/"+command["name"]+".py", os.F_OK):
                    self.help(source, command["command"], command["help"])
              
              self.msg(source, "End of list.")
              
              self.bot = self.services_id + bots.get(self.BOT_ID, "uuid")
            else:
              iscmd = False
              for command in self.query("SELECT * FROM modules WHERE class = 'COMMAND' AND command = %s AND bot = %s AND auth <= %s AND oper <= %s", cmd.upper(), bot, isauth, isoper):
                if os.access("modules/" + command["name"] + ".py", os.F_OK):
                  iscmd = True
                  
                  moduleToCall = getattr(modules, command["name"])
                  classToCall = getattr(moduleToCall, command["name"])()
                  methodToCall = getattr(classToCall, "onCommand")
                  
                  if len(data.split()) == 4:
                    _thread.start_new_thread(methodToCall, (data.split()[0][1:], ''))
                  elif len(data.split()) > 4:
                    _thread.start_new_thread(methodToCall, (data.split()[0][1:], ' '.join(data.split()[4:])))
                      
              if not iscmd:
                self.msg(data.split()[0][1:], "Unknown command {0}. Please try HELP for more information.".format(cmd.upper()), uid=botuid)
                
          elif data.split()[2].startswith("#") and self.chanflag("f", data.split()[2]) and self.chanexist(data.split()[2]):
            if data.split()[3][1:].startswith(self.fantasy(data.split()[2])):
              botuid = self.services_id + bots.get(bot, "uuid")
              fuid = data.split()[0][1:]
              cmd = self.fantasy(data.split()[2])
              
              if len(data.split()[3]) > int(1+len(self.fantasy(data.split()[2]))):
                fchan = data.split()[2]
                cmd = data.split()[3][int(1+len(self.fantasy(fchan))):]
                
                if len(data.split()) > 4:
                  args = ' '.join(data.split()[4:])
                  
                for command in self.query("SELECT * FROM modules WHERE class = 'COMMAND' AND command = %s AND oper = 0 AND bot = %s", cmd.upper(), bot):
                  if os.access("modules/" + command["name"] + ".py", os.F_OK):
                    moduleToCall = getattr(modules, command["name"])
                    classToCall = getattr(moduleToCall, command["name"])()
                    methodToCall = getattr(classToCall, "onFantasy")
                    
                    if not classToCall.NEED_AUTH:
                      if len(data.split()) == 4:
                        _thread.start_new_thread(methodToCall, (fuid, fchan, ''))
                      elif len(data.split()) > 4:
                        _thread.start_new_thread(methodToCall, (fuid, fchan, args))
                    elif classToCall.NEED_AUTH:
                      if self.auth(fuid):
                        if len(data.split()) == 4:
                          _thread.start_new_thread(methodToCall, (fuid, fchan, ''))
                        elif len(data.split()) > 4:
                          _thread.start_new_thread(methodToCall, (fuid, fchan, args))
    except Exception:
      et, ev, tb = sys.exc_info()
      e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
      debug(red("*") + " <<ERROR>> " + str(e))

  def onCommand(self, uid, arguments):
    pass

  def onFantasy(self, uid, channel, arguments):
    pass
    
  def onData(self, data):
    pass
    
  def onSchedule(self):
    pass
    
  def runSchedule(self):
    if self.TIMER <= 0:
      debug(red("*") + " <<ERROR>> runSchedule -> TIMER <= 0")
      return 0
      
    while True:
      start = int(time.time())
      
      try:
        self.onSchedule()
      except Exception:
        et, ev, tb = sys.exc_info()
        e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
        debug(red("*") + " <<ERROR>> " + str(e))
        
      try:
        stop = int(time.time())
        elapsed = stop - start
        next = self.TIMER - elapsed
        
        while next <= 0:
          next = next + self.TIMER
          
        time.sleep(next)
      except Exception:
        et, ev, tb = sys.exc_info()
        e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
        debug(red("*") + " <<ERROR>> " + str(e))
        return 0
        
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
    try:
      self.db_cursor.execute(string + ";", args)
      debug(blue("*** => ") + " " + self.db_cursor.query.decode("UTF-8"))
      db_interface.commit()
      
      if self.db_cursor.rowcount > 0 and string.lower().find('select ') != -1:
        result = list()
        rows = self.db_cursor.fetchall()
        debug(green("*** <= ") + " " + str(rows))
        for row in rows:
          result.append(dict(row))
          
        return result
    except psycopg2.DatabaseError as e:
      db_interface.rollback()
      et, ev, tb = sys.exc_info()
      e = "{0}: {1} ({2})".format(et, ev, traceback.format_tb(tb))
      debug(red("*") + " <<ERROR>> " + str(e))
      
    return list()

  def send_bot(self, content):
    self.send(":" + self.bot + " " + content)

  def send_serv(self, content):
    self.send(":" + self.services_id + " " + content)

  def send_to_op(self, content):
    if not self.oper_not:
      return 0;
      
    result = self.query("SELECT uid FROM opers")
    for row in result:
      self.send_serv("PRIVMSG " + row["uid"] + " :" + content)

  def uid (self, nick):
    if nick == self.bot_nick:
      return self.bot
    elif len(nick) > 9:
      return nick
      
    for data in self.query("select uid from online where LOWER(nick) = LOWER(%s)", nick):
      return str(data["uid"])
      
    return nick

  def nick(self, source):
    if source == self.bot:
      return self.bot_nick
      
    for data in self.query("select nick from online where uid = %s", source):
      return str(data["nick"])
      
    return source

  def user(self, user):
    if user.lower() == self.bot_nick.lower():
      return self.bot_nick
      
    for data in self.query("select name from users where LOWER(name) = LOWER(%s)", user):
      return str(data["name"])
      
    return False

  def banned(self, user):
    for data in self.query("select * from users where LOWER(name) = LOWER(%s) and suspended != '0'", user):
      return data["suspended"]
      
    return False

  def gateway (self, target):
    uid = self.uid(target)
    
    for data in self.query("select uid from gateway where uid = %s", uid):
      return True
      
    return False

  def send(self, text):
    self.con.send(bytes(text+"\n", "UTF-8"))
    debug(blue("*") + " " + text)

  def push(self, target, message):
    self.send(":{uid} PUSH {target} ::{message}".format(uid=self.services_id, target=target, message=message))

  def help(self, target, command, description=""):
    self.msg(target, command.upper()+" "*int(20-len(command))+description)

  def ison(self, user, uid=False):
    if not uid:
      for data in self.query("SELECT nick FROM online WHERE LOWER(account) = LOWER(%s) LIMIT 1", user):
        return True
    else:
      for data in self.query("SELECT nick FROM online WHERE uid = %s LIMIT 1", user):
        return True
      
    return False

  def usermodes(self, target):
    user = self.auth(target)
    
    if self.ison(user):
      for data in self.query("select modes from users where LOWER(name) = LOWER(%s)", user):
        self.mode(target, data["modes"])
        
        if data["modes"].find("+") != -1:
          modes = data["modes"].split("+")[1]
          
          if modes.find("-") != -1:
            modes = modes.split("-")[0]
            
          if modes.find("B") != -1:
            if not self.gateway(target):
              self.query("insert into gateway values (%s)", target)
              self.vhost(target)
              
        if data["modes"].find("-") != -1:
          modes = data["modes"].split("-")[1]
          
          if modes.find("+") != -1:
            modes = modes.split("+")[0]
            
          if modes.find("B") != -1:
            if self.gateway(target):
              self.query("delete from gateway where uid = %s", target)
              self.vhost(target)

  def userflags(self, target):
    user = self.auth(target)
    
    if user == 0:
      user = target
      
    for data in self.query("select flags from users where LOWER(name) = (%s)", user):
      return data["flags"]
      
    return ''

  def userflag(self, target, flag):
    user = self.auth(target)
    
    if self.ison(user):
      for data in self.query("select flags from users where LOWER(name) = LOWER(%s)", user):
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

  def SetMetadata(self, uid, key, value = None):
    if value:
      count = int(self.query("SELECT COUNT(*) FROM metadata WHERE uid = %s AND key = %s", uid, key)[0]["count"])
      if count == 1:
        self.query("UPDATE metadata SET value = %s WHERE uid = %s AND key = %s", value, uid, key)
      else:
        self.query("INSERT INTO metadata (uid, key, value) VALUES (%s, %s, %s)", uid, key, value)
        
      self.send_serv("METADATA " + uid + " " + key + " :" + value)
    else:
      self.query("DELETE FROM metadata WHERE uid = %s AND key = %s", uid, key)
      self.send_serv("METADATA " + uid + " " + key)

  def GetMetadata(self, uid, key):
    result = self.query("SELECT value FROM metadata WHERE uid = %s AND key = %s", uid, key)
    for row in result:
      return row["value"]
      
    return None

  def GetAccountData(self, account):
    result = self.query("SELECT * FROM users WHERE LOWER(name) = LOWER(%s)", account)
    for row in result:
      return row
      
    return None

  def GetUserData(self, uid):
    result = self.query("SELECT * FROM online WHERE uid = %s", uid)
    for row in result:
      return row
      
    return None

  def GetChannelFlags(self, account):
    result = self.query("SELECT * FROM channels WHERE LOWER(user) = LOWER(%s)", account)
    for row in result:
      return row
      
    return None

  def GetChannnelData(self, channel):
    result = self.query("SELECT * FROM channelinfo WHERE LOWER(name) = LOWER(%s)", channel)
    for row in result:
      return row
      
    return None

  def auth(self, target):
    for data in self.query("SELECT account FROM online WHERE uid = %s AND account != ''", target):
      return data["account"]
      
    return None

  def sid(self, account):
    uids = list()
    
    for data in self.query("select uid from online where LOWER(account) = LOWER(%s)", account):
      uids.append(data["uid"])
      
    return uids

  def memo(self, user):
    for data in self.query("select source,message from memo where LOWER(user) = LOWER(%s)", user):
      online = False
      
      for source in self.sid(user):
        online = True
        self.msg(source, "[Memo] From: %s, Message: %s" % (data["source"], data["message"]))
        
      if online:
        self.query("delete from memo where LOWER(user) = LOWER(%s) and source = %s and message = %s", user, data["source"], data["message"])

  def chanexist(self, channel):
    for data in self.query("select name from channelinfo where LOWER(name) = LOWER(%s)", channel):
      return True
      
    return False

  def channelusercount(self, channel):
    count = int(self.query("SELECT COUNT(*), address FROM online WHERE uid IN (SELECT uid FROM chanlist WHERE LOWER(channel) = LOWER(%s)) GROUP BY address HAVING COUNT(*) = 1", channel)[0]["count"])
    return count
    
  def gettopic(self, channel):
    if self.chanexist(channel):
      for data in self.query("select topic from channelinfo where LOWER(name) = LOWER(%s)", channel):
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
    self.query("update statistics set value = %s where attribute = 'kills'", kills)
    return kills

  def kickcount(self):
    kicks = int(self.statistics()["kicks"])
    kicks += 1
    self.query("update statistics set value = %s where attribute = 'kicks'", kicks)
    return kicks

  def kill(self, target, reason="You're violating network rules"):
    if not self.isoper(self.uid(target)):
      self.send_serv("KILL %s :Killed (*.%s (%s (#%s)))" % (self.uid(target), self.getservicedomain(), reason, str(self.killcount())))

  def vhost(self, target):
    if not self.gateway(target):
      entry = False
      
      for data in self.query("select vhost from vhosts where user = %s and active = '1'", self.auth(target)):
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
        _flag = ''
        
        for flag in self.query("select flag,channel from channels where user = %s and LOWER(channel) = LOWER(%s)", account, channel):
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
            
          _flag = flag["flag"]
          
        if _flag == '':
          if self.chanexist(channel):
            if not self.chanflag("v", channel):
              self.mode(channel, "-qaohv {0} {0} {0} {0} {0}".format(target))
            else:
              self.mode(channel, "-qaoh {0} {0} {0} {0}".format(target))
              
        if self.chanexist(channel):
          self.setuserchanflag(channel, target, _flag.replace('n', 'q'))
      else:
        for flag in self.query("select flag,channel from channels where user = %s order by channel", account):
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
            if not self.chanflag("v", flag["channel"]):
              self.mode(flag["channel"], "-qaohv {0} {0} {0} {0} {0}".format(target))
            else:
              self.mode(flag["channel"], "-qaoh {0} {0} {0} {0}".format(target))
              
          self.setuserchanflag(flag["channel"], target, flag["flag"].replace('n', 'q'))

  def autojoin(self, target):
    user = self.auth(target)
    
    if self.ison(user):
      if self.userflag(target, "a"):
        for data in self.query("select channel,flag from channels where user = %s", user):
          channel = data["channel"]
          flag = data["flag"]
          
          if flag == "n" or flag == self.bot_nick or flag == "a" or flag == "o" or flag == "h" or flag == "v":
            self.send(":%s SVSJOIN %s %s" % (self.bot, target, channel))

  def getflag(self, target, channel):
    for data in self.query("select account from online where uid = %s", target):
      for flag in self.query("select flag from channels where channel = %s and user = %s", channel, data["account"]):
        return flag["flag"]
        
    return 0

  def chanflag(self, flag, channel):
    for data in self.query("select flags from channelinfo where LOWER(name) = LOWER(%s)", channel):
      if data["flags"].find(flag) != -1:
        return True
        
    return False

  def isoper(self, target):
    if self.isserv(target):
      return True
      
    isoper = False
    
    for data in self.query("select * from opers where uid = %s", target):
      isoper = True
      
    return isoper

  def encode(self, string):
    return hashlib.sha512(bytes(string, "UTF-8")).hexdigest()

  def encode_md5(self, string):
    return hashlib.md5(bytes(string, "UTF-8")).hexdigest()

  def mail(self, receiver, subject, message):
    try:
      from email.mime.text import MIMEText
      from email.mime.multipart import MIMEMultipart
      msg = MIMEMultipart('alternative')
      msg.attach(MIMEText(message, 'plain'))
      message = message.replace("\n", "\n<br />")
      message = self.mail_template.replace("${MESSAGE}", message)
      msg.attach(MIMEText(message, 'html'))
      msg['Subject'] = subject
      msg['From'] = self.services_description + ' <' + self.email + '>'
      msg['To'] = receiver
      mail = smtplib.SMTP('127.0.0.1', 25)
      mail.sendmail(self.email, msg['To'], msg.as_string())
      mail.quit()
    except Exception as e:
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
        
      result = self.query("SELECT COUNT(*) FROM logs WHERE channel = %s", channel)
      for row in result:
        if row["count"] == 50:
          self.query("DELETE FROM logs WHERE channel = %s LIMIT 1", channel)
          
      self.query("INSERT INTO logs (channel, sender, action, message) VALUES (%s, %s, %s, %s)", channel, sender, msgtype.upper(), text)
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
      
      result = self.query("SELECT channel, sender, action, message FROM logs WHERE channel = %s ORDER BY id", channel)
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
        
      self.query("delete from chanlist where LOWER(channel) = LOWER(%s) and uid = %s", channel, uid)

  def userlist(self, channel):
    uid = list()
    
    for user in self.query("select uid from chanlist where LOWER(channel) = LOWER(%s)", channel):
      uid.append(user["uid"])
      
    return uid

  def onchan(self, channel, target):
    uid = self.uid(target)
    
    for data in self.query("select * from chanlist where LOWER(channel) = LOWER(%s) and uid = %s", channel, uid):
      return True
      
    return False
    
  def currentuserchanflag(self, channel, target):
    uid = self.uid(target)
    
    for data in self.query("SELECT flag FROM chanlist WHERE uid = %s AND LOWER(channel) = LOWER(%s)", uid, channel):
      return data["flag"]
      
    return ""

  def setuserchanflag(self, channel, target, flag):
    uid = self.uid(target)
    self.query("UPDATE chanlist SET flag = %s WHERE uid = %s AND LOWER(channel) = LOWER(%s)", flag, uid, channel)
  
  def getident(self, target):
    uid = self.uid(target)
    
    for data in self.query("select username from online where uid = %s", uid):
      return data["username"]
      
    return 0

  def gethost(self, target):
    uid = self.uid(target)
    
    for data in self.query("select host from online where uid = %s", uid):
      return data["host"]
      
    return 0

  def hostmask(self, target):
    uid = self.uid(target)
    masks = list()
    nick = None
    username = None
    account = self.auth(uid)
    
    for data in self.query("select nick,username,host from online where uid = %s", uid):
      nick = data["nick"]
      username = data["username"]
      masks.append(data["nick"]+"!"+data["username"]+"@"+data["host"])
      
    if self.auth(uid) != 0:
      for data in self.query("select vhost from vhosts where user = %s and active = '1'", account):
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
    for data in self.query("select ban from banlist where channel = %s", channel):
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
    
    for data in self.query("select address from online where uid = %s", uid):
      return data["address"]
      
    return 0

  def gline(self, target, reason="", bantime="1800", addentry=False):
    uid = self.uid(target)
    
    if uid != self.bot and target.lower() != self.bot_nick.lower() and not self.isoper(uid):
      ip = self.getip(uid)
      
      if addentry:
        rows = int(self.query("SELECT COUNT(*) FROM glines WHERE LOWER(mask) = LOWER(%s)", "*@" + ip)[0]["count"])
        
        if rows == 0:
          etime = int(time.time()) + int(bantime)
          self.query("INSERT INTO glines (mask, timestamp) VALUES (%s, %s)", "*@" + ip, etime)
          
      for data in self.query("select uid from online where address = %s", self.getip(uid)):
        self.send_serv("KILL "+data["uid"]+" :G-lined")
        
      self.send_serv("GLINE *@"+ip+" "+str(bantime)+" :"+reason)
      self.send_to_op("#G-line# *@" + ip + " added (" + self.convert_timestamp(int(bantime)) + ")")

  def suspended(self, channel):
    for data in self.query("select reason from suspended where LOWER(channel) = LOWER(%s)", channel):
      return data["reason"]
      
    return False

  def userhost(self, target):
    uid = self.uid(target)
    
    for data in self.query("select username, host from online where uid = %s", uid):
      return data["username"]+"@"+data["host"]
      
    return 0

  def getvhost(self, target):
    for data in self.query("select vhost from vhosts where user = %s and active = '1'", target):
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
      for data in self.query("select fantasy from channelinfo where name = %s", channel):
        return data["fantasy"]
        
    return False

  def getconns(self, address):
    result = self.query("SELECT COUNT(*) FROM online WHERE address = %s", address)
    for row in result:
      return int(row["count"])
      
    return 0

  def checkconnection(self, uid):
    if self.isserv(uid):
      return False
      
    user_ip = self.getip(uid)
    user_host = self.gethost(uid)
    user_name = self.getident(uid)
    timestamp = time.time()
    
    if user_ip == 0:
      return False
      
    limit = 3
    result = self.query("SELECT \"limit\" FROM trust WHERE (address = %s OR address = %s) AND timestamp > %s", user_ip, user_host, timestamp)
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
      for row in self.query("SELECT uid FROM online WHERE address = %s OR host = %s", user_ip, user_host):
        self.msg(row["uid"], "Your IP is scratching the connection limit. If you need more connections please request a trust.")
        
    return False

  def isserv(self, uid):
    uid = self.uid(uid)
    if uid.startswith(self.services_id):
      return True
      
    return False

  def opertype(self, uid):
    for row in self.query("SELECT opertype FROM opers WHERE uid = %s", uid):
      return row["opertype"]
      
    return None

  def isoptype(self, uid, type):
    for row in self.query("SELECT uid FROM opers WHERE uid = %s AND LOWER(opertype) = LOWER(%s)", uid, type):
      return True
      
    return False

if __name__ == "__main__":
  try:
    while True:
      __version__ = open("version", "r").read()
      
      if len(sys.argv) == 1:
        __config__ = "config.cfg"
      else:
        __config__ = sys.argv[1]
        
      time.sleep(9)
      print((green("*") + " chiruclan.de IRC services (" + __version__ + ") started (config: " + __config__ + ")"))
      Services().run()
      print((red("*") + " chiruclan.de IRC services (" + __version__ + ") stopped (config: " + __config__ + ")"))
      
      time.sleep(1)
  except Exception as e:
    print((red("*") + " " + str(e)))
  except KeyboardInterrupt:
    print((red("*") + " Aborting ... STRG +C"))
    
    if os.access("cDIS.pid", os.F_OK):
      shell("sh cDIS restart")