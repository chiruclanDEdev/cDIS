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

from cDIS import cDISModule, config, bots

class cmd_3_auth(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "AUTH"
  HELP = "Login with your account at " + bots.get("3", "nick") + "@" + config.get("SERVICES", "name")
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    
    if self.auth(source):
      self.msg(source, "AUTH is not available once you have authed.")
      return 0
      
    if len(arg) == 2:
      exists = False
      
      for data in self.query("select name,pass,suspended from users where name = %s", arg[0]):
        if self.encode(arg[1]) == str(data["pass"]):
          exists = True
          
          if data["suspended"] == "0":
            for user in self.query("select uid, nick, username, host from online where account = %s", str(data["name"])):
              self.msg(str(user["uid"]), "Warning: {0} ({1}@{2}) authed with your password.".format(user["nick"], user["username"], user["host"]))
              
            self.query("UPDATE online SET account = %s WHERE uid = %s", data["name"], source)
            self.msg(source, "You are now logged in as %s." % str(data["name"]))
            self.msg(source, "Remember: NO-ONE from %s will ever ask for your password. NEVER send your password to ANYONE except %s@%s." % (self.services_description, self.bot_nick, self.services_name))
            self.SetMetadata(source, "accountname", str(data["name"]))
            self.usermodes(source)
            self.vhost(source)
            self.flag(source)
            self.autojoin(source)
          else:
            self.msg(source, "Your account has been banned from " + self.services_description + ". Reason: " + data["suspended"])
            
      if not exists:
        self.msg(source, "Username or password incorrect.")
    else:
      self.msg(source, "Syntax: AUTH <username> <password>")
