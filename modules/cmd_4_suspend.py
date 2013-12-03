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

class cmd_4_suspend(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "SUSPEND"
  HELP = "Suspends a channel"
  NEED_OPER = 1
  BOT_ID = '4'

  def onCommand(self, uid, args):
    arg = args.split()
    if len(arg) > 1:
      channel = arg[1]
    if len(arg) > 2:
      reason = ' '.join(arg[2:])
    
    if len(arg) == 2 and arg[0].lower() == "remove":
      if arg[1].startswith("#"):
        if self.suspended(channel):
          self.query("delete from suspended where channel = %s", channel)
          self.msg(uid, "Unsuspended.")
        else:
          self.msg(uid, arg[1]+" is not suspended.")
      else:
        self.msg(uid, "Invalid channel: "+arg[1])
    elif len(arg) > 2 and arg[0].lower() == "set":
      if arg[1].startswith("#"):
        if not self.suspended(channel):
          self.query("insert into suspended (channel, reason) values (%s, %s)", channel, reason)
          
          if self.chanexist(channel):
            self.query("delete from channels where channel = %s", channel)
            self.query("delete from channelinfo where name = %s", channel)
            self.query("delete from banlist where channel = %s", channel)
            self.send(":{0} PART {1} :Channel {1} has been suspended.".format(self.bot, arg[1]))
            
          for user in self.userlist(channel):
            if not self.isoper(user):
              self.kick(arg[1], user, "Suspended: "+' '.join(arg[2:]))
            else:
              self.msg(arg[1], "This channel is suspended: "+' '.join(arg[2:]))
        else:
          self.query("update suspended set reason = %s where channel = %s", reason, channel)
          
          for user in self.userlist(channel):
            if not self.isoper(user):
              self.kick(arg[1], user, "Suspended: "+' '.join(arg[2:]))
            else:
              self.msg(arg[1], "This channel is suspended: "+' '.join(arg[2:]))
              
        self.msg(uid, "Suspended.")
      else:
        self.msg(uid, "Invalid channel: "+arg[1])
    elif len(arg) == 1 and arg[0].lower() == "list":
      for data in self.query("select * from suspended"):
        self.msg(uid, "Channel: {0} {1} Reason: {2}".format(data["channel"], " "*int(23-len(data["channel"])), data["reason"]))
    else:
      self.msg(uid, "Syntax: SUSPEND <list/set/remove> <#channel> [<reason>]")
