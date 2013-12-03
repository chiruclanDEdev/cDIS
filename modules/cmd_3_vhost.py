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

class cmd_3_vhost(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "VHOST"
  HELP = "Request a vHost for your account"
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    
    if len(arg) == 2 and arg[0] == "set":
      if arg[1].find(".") == -1:
        self.msg(source, "Invalid vhost. Where's the dot?")
      elif arg[1][-2] == "." or arg[1][-1] == ".":
        self.msg(source, "Domain ending is too short.")
      elif arg[1].find("@") != -1 and len(arg[1].split("@")[0]) < 3:
        self.msg(source, "vIdent too short.")
      elif arg[1].find("@") != -1 and len(arg[1].split("@")[1]) < 6:
        self.msg(source, "vHost too short.")
      elif arg[1].find("@") != -1 and arg[1].split("@")[0].find(".") != -1:
        self.msg(source, "No dots allowed in vIdent.")
      elif arg[1].find("@") != -1 and arg[1].split("@")[1].find(".") == -1:
        self.msg(source, "Thats no vHost, the DOT is missing.")
      elif len(arg[1]) < 6:
        self.msg(source, "Your vhost is too short.")
      else:
        entry = False
        vhost = arg[1]
        
        if vhost.find("@") != -1:
          vhost = vhost.split("@")[0]
          
        for data in self.query("select user from vhosts where vhost = %s and user != %s", vhost, self.auth(source)):
          user = data["user"]
          entry = True
          
        if not entry:
          self.query("delete from vhosts where user = %s", self.auth(source))
          self.query("insert into vhosts values (%s, %s, '0')", self.auth(source), arg[1])
          self.msg(source, "Your new vhost %s has been requested" % arg[1])
          
          for data in self.query("select host,username from online where uid = %s", source):
            if not self.gateway(source):
              self.send(":%s CHGIDENT %s %s" % (self.bot, source, data["username"]))
              self.send(":%s CHGHOST %s %s" % (self.bot, source, data["host"]))
            else:
              self.send(":%s CHGIDENT %s %s" % (self.bot, source, data["username"]))
              crypthost = self.encode_md5(source + ":" + self.nick(source) + "!" + self.userhost(source))
              self.send(":%s CHGHOST %s %s.gateway.%s" % (self.bot, source, crypthost, '.'.join(self.services_name.split(".")[-2:])))
              
          for data in self.query("select uid from opers"):
            self.msg(data["uid"], "vHost request received from %s" % self.auth(source))
        else:
          self.msg(source, "%s is already using this vHost." % user)
    elif len(arg) == 1 and arg[0].lower() == "info":
      vhost = self.getvhost(source)
      if vhost != "None":
        self.msg(source, "Your current vHost is: " + vhost)
      else:
        self.msg(source, "You did not set a vHost or userflag +x.")
    elif len(arg) == 1 and arg[0].lower() == "remove":
      self.query("delete from vhosts where user = %s", self.auth(source))
      self.vhost(source)
      self.msg(source, "Done.")
    else:
      self.msg(source, "Syntax: VHOST <info/set/remove> [<vhost>]")
