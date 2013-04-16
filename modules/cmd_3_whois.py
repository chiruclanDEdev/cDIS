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

from cDIS import cDISModule

class cmd_3_whois(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "WHOIS"
  HELP = "Shows information about a user"
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    entry = False
    
    if len(arg) == 1:
      if arg[0].startswith("#"):
        for user in self.query("select name,email from users where name = ?", arg[0][1:]):
          entry = True
          self.msg(source, "-Information for account {0}:".format(user["name"]))
          online = list()
          
          for uid in self.sid(user["name"]):
            online.append(self.nick(uid))
            
          self.msg(source, "Online Nicks  : {0}".format(' '.join(online)))
          self.msg(source, "User flags    : +{0}".format(self.userflags(user["name"])))
          self.msg(source, "Email address : {0}".format(user["email"]))
          self.msg(source, "vHost         : {0}".format(self.getvhost(user["name"])))
          
          if len(online) < 2:
            self.msg(source, "Gateway       : {0}".format(self.gateway(self.uid(online[0]))))
            
          self.msg(source, "Known on following channels:")
          self.msg(source, "Channel              Flag")
          
          for channel in self.query("select channel,flag from channels where user = ? order by flag,channel", user["name"]):
            self.msg(source, " {0}{1}+{2}".format(channel["channel"], " "*int(20-len(channel["channel"])), channel["flag"]))
            
          self.msg(source, "End of list.")
          
          if self.banned(user["name"]):
            if self.isoper(source):
              self.msg(source, "--- User " + user["name"] + " is banned: " + self.banned(user["name"]) + " ---")
            else:
              self.msg(source, "--- User " + user["name"] + " is banned. ---")
      else:
        for data in self.query("select uid from online where nick = ? ", arg[0]):
          entry = True
          user = self.auth(data["uid"])
          
          if user != 0:
            for account in self.query("select email from users where name = ?", user):
              self.msg(source, "-Information for account {0}:".format(user))
              online = list()
              
              for uid in self.sid(user):
                online.append(self.nick(uid))
                
              self.msg(source, "Online Nicks  : {0}".format(' '.join(online)))
              
              if self.isoper(source) or self.auth(source) == user:
                self.msg(source, "User flags    : +{0}".format(self.userflags(user)))
                self.msg(source, "Email address : {0}".format(account["email"]))
                
              self.msg(source, "vHost         : {0}".format(self.getvhost(user)))
              self.msg(source, "Gateway       : {0}".format(str(self.gateway(data["uid"]))))
              self.msg(source, "Known on following channels:")
              self.msg(source, "Channel              Flag")
              
            for channel in self.query("select channel,flag from channels where user = ? order by flag,channel", user):
              if self.isoper(source) or self.auth(source) == user or self.getflag(source, channel["channel"]) != 0:
                self.msg(source, " {0}{1}+{2}".format(channel["channel"], " "*int(20-len(channel["channel"])), channel["flag"]))
                  
            self.msg(source, "End of list.")
            
            if self.banned(user):
              if self.isoper(source):
                self.msg(source, "--- User " + user + " is banned: " + self.banned(user) + " ---")
              else:
                self.msg(source, "--- User " + user + " is banned. ---")
          else:
            self.msg(source, "User " + arg[0] + " is not authed.")
      if not entry:
        self.msg(source, "Can't find user {0}".format(arg[0]))
    else:
      self.msg(source, "Syntax: WHOIS <nick>/<#account>")
