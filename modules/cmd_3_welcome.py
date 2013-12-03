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

class cmd_3_welcome(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "WELCOME"
  NEED_AUTH = 1
  HELP = "Sets a welcome message for your channel"
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    
    if len(arg) == 1:
      if arg[0].startswith("#"):
        entry = False
        
        for data in self.query("select name,welcome from channelinfo where name = %s", arg[0]):
          self.msg(source, "[{0}] {1}".format(data["name"], data["welcome"]))
          entry = True
          
        if not entry:
          self.msg(source, "Channel {0} does not exist".format(arg[0]))
      else:
        self.msg(source, "Invalid channel")
    elif len(arg) > 1:
      if arg[0].startswith("#"):
        flag = self.getflag(source, arg[0])
        welcome = ' '.join(arg[1:])
        
        if flag == "n" or flag == "q" or flag == "a":
          self.query("update channelinfo set welcome = %s where name = %s", welcome, arg[0])
          self.msg(source, "Done.")
        else:
          self.msg(source, "Denied.")
      else:
        self.msg(source, "Invalid channel")
    else:
      self.msg(source, "Syntax: WELCOME <#channel> [<text>]")

  def onFantasy(self, uid, chan, args):
    flag = self.getflag(uid, chan)
    
    if flag == "n" or flag == "q" or flag == "a":
      self.onCommand(uid, chan + " " + args)
