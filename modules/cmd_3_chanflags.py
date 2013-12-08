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

class cmd_3_chanflags(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "CHANFLAGS"
  HELP = "Sets flags for your channel"
  NEED_AUTH = 1
  ENABLE_FANTASY = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    mode = list()
    desc = list()
    mode.append("p")
    desc.append("Channel rights Protection")
    mode.append("v")
    desc.append("Autovoice in channel")
    mode.append("t")
    desc.append("Topic save")
    mode.append("m")
    desc.append("Modes enforcement")
    mode.append("w")
    desc.append("Welcome message on join")
    mode.append("e")
    desc.append("Enforce bans")
    mode.append("b")
    desc.append("Bitchmode")
    mode.append("s")
    desc.append("Spamscan, prevents channel flooding")
    mode.append("f")
    desc.append("Fantasy commands")
    mode.append("k")
    desc.append("Sign kicks with {0}".format(self.bot_nick))
    mode.append("c")
    desc.append("Display count at {0}-kicks".format(self.bot_nick))
    arg = args.split()
    
    if len(arg) == 1:
      if arg[0].startswith("#"):
        if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q" or self.getflag(source, arg[0]) == "a":
          for channel in self.query("select name,flags from channelinfo where name = %s", arg[0]):
            self.msg(source, "Current flags for {0}: +{1}".format(channel["name"], channel["flags"]))
        else:
          self.msg(source, "Denied.")
      elif arg[0] == "?":
        listed = 0
        
        while listed != len(mode):
          self.msg(source, "+{0} = {1}".format(mode[listed], desc[listed]))
          listed += 1
      else:
        self.msg(source, "Invalid channel '{0}'".format(arg[0]))
    elif len(arg) == 2:
      if arg[0].startswith("#"):
        if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "a":
          for channel in self.query("select name,flags from channelinfo where name = %s", arg[0]):
            chanflags = self.regexflag("+" + channel["flags"], arg[1])
            flags = ''.join([char for char in chanflags if char in ''.join(mode)])
            self.query("update channelinfo set flags = %s where name = %s", flags, channel["name"])
            self.msg(source, "Done. New flags for {0}: +{1}".format(channel["name"], flags))
        else:
          self.msg(source, "Denied.")
      else:
        self.msg(source, "Invalid channel '{0}'".format(arg[0]))
    else:
      self.msg(source, "Syntax: CHANFLAGS <#channel> [<flags>]")

  def onFantasy(self, uid, chan, args):
    flag = self.getflag(uid, chan)
    
    if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
      self.onCommand(uid, chan + " " + args)
