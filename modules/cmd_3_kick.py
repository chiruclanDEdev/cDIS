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

class cmd_3_kick(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "KICK"
  HELP = "Kicks someone from the channel"
  NEED_AUTH = 1
  BOT_ID = '3'

  def onCommand(self, source, args):
    arg = args.split()
    
    if len(arg) == 2:
      if self.chanexist(arg[0]):
        flag = self.getflag(source, arg[0])
        
        if flag == "n" or flag == "q" or flag == "a" or flag =="o"or flag =="h":
          if arg[1].lower() != self.bot_nick.lower() and not self.isoper(self.uid(arg[1])):
            if self.onchan(arg[0],arg[1]):
              if self.chanflag("k", arg[0]):
                self.kick(arg[0], arg[1], self.nick(source))
              else:
                self.kick(arg[0], arg[1])
                
              self.msg(source, "Done.")
            else:
              self.msg(source, arg[1]+" is not on channel "+arg[0])
          else:
            self.msg(source, "Denied.")
        else:
          self.msg(source, "Denied.")
      else:
        self.msg(source, "Invalid channel")
    elif len(arg) > 2:
      if self.chanexist(arg[0]):
        flag = self.getflag(source, arg[0])
        
        if flag == "n" or flag == "q" or flag == "a" or flag =="o"or flag =="h":
          if arg[1].lower() != self.bot_nick.lower() and not self.isoper(self.uid(arg[1])):
            if self.onchan(arg[0],arg[1]):
              if self.chanflag("k", arg[0]):
                self.kick(arg[0], arg[1], ' '.join(arg[2:]) + " (" + self.nick(source) + ")")
              else:
                self.kick(arg[0], arg[1], ' '.join(arg[2:]))
                
              self.msg(source, "Done.")
            else:
              self.msg(source, arg[1]+" is not on channel "+arg[0])
          else:
            self.msg(source, "Denied.")
        else:
          self.msg(source, "Denied.")
      else:
        self.msg(source, "Invalid channel")
    else:
      self.msg(source, "Syntax: KICK <#channel> <user> [,<user>] [reason]")

  def onFantasy(self, uid, chan, args):
    flag = self.getflag(uid, chan)
    
    if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
      self.onCommand(uid, chan + " " + args)
