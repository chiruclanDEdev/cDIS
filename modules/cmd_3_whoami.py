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

class cmd_3_whoami(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "WHOAMI"
  HELP = "Shows information about you"
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    auth = self.auth(source)
    
    for user in self.query("select name,email from users where name = %s", auth):
      self.msg(source, "-Information for account {0}:".format(user["name"]))
      online = list()
      
      for uid in self.sid(user["name"]):
        online.append(self.nick(uid))
        
      self.msg(source, "Online Nicks  : {0}".format(' '.join(online)))
      self.msg(source, "User flags    : +{0}".format(self.userflags(user["name"])))
      self.msg(source, "Email address : {0}".format(user["email"]))
      self.msg(source, "vHost         : {0}".format(self.getvhost(user["name"])))
      self.msg(source, "Gateway       : {0}".format(str(self.gateway(source))))
      self.msg(source, "Known on following channels:")
      self.msg(source, "Channel              Flag")
      
      for channel in self.query("select channel,flag from channels where user = %s order by flag,channel", user["name"]):
        self.msg(source, " {0}{1}+{2}".format(channel["channel"], " "*int(20-len(channel["channel"])), channel["flag"]))
        
      self.msg(source, "End of list.")