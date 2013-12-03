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

class cmd_4_info(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "INFO"
  HELP = "Shows all information about an user"
  NEED_OPER = 1
  BOT_ID = '4'

  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 1:
      if self.user(arg[0]):
        user = self.user(arg[0])
        
        for user in self.query("select name,email,flags,modes from users where name = %s", user):
          self.msg(uid, "-Information for account {0}:".format(user["name"]))
          online = list()
          userhosts = list()
          hosts = list()
          
          for uuid in self.sid(user["name"]):
            online.append(self.nick(uuid))
            userhosts.append(self.userhost(uuid))
            hosts.append(self.gethost(uuid))
            
          self.msg(uid, "Online Nicks  : {0}".format(' '.join(online)))
          self.msg(uid, "Hosts         : {0}".format(' '.join(hosts)))
          self.msg(uid, "Userhosts     : {0}".format(' '.join(userhosts)))
          self.msg(uid, "User flags    : +{0}".format(user["flags"]))
          self.msg(uid, "Usermode      : {0}".format(user["modes"]))
          self.msg(uid, "Email address : {0}".format(user["email"]))
          self.msg(uid, "vHost         : {0}".format(self.getvhost(user["name"])))
          
          if len(online) < 2:
            self.msg(uid, "Gateway       : {0}".format(str(self.gateway(self.uid(online[0])))))
            
          self.msg(uid, "Known on following channels:")
          self.msg(uid, "Channel              Flag")
          
          for channel in self.query("select channel,flag from channels where user = %s order by flag,channel", user["name"]):
            self.msg(uid, " {0}{1}+{2}".format(channel["channel"], " "*int(20-len(channel["channel"])), channel["flag"]))
            
          self.msg(uid, "End of list.")
          
          if self.banned(arg[0]):
            self.msg(uid, "--- User " + arg[0] + " is banned: " + self.banned(arg[0]) + " ---")
      else:
        self.msg(uid, "Can't find user " + arg[0] + ".")
    else:
      self.msg(uid, "Syntax: INFO <account>")
