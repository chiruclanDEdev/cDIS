# chiruclan.de IRC services
# Copyright (C) 2012-2014  Chiruclan
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

class cmd_3_settopic(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "SETTOPIC"
    HELP = "Sets topic for your channel"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, source, args):
        arg = args.split()
        
        if len(arg) > 1:
            if arg[0].startswith("#"):
                if self.getflag(source, arg[0]) == "n" or self.getflag(source, arg[0]) == "q" or self.getflag(source, arg[0]) == "a":
                    self.query("update channelinfo set topic = %s where name = %s", ' '.join(arg[1:]), arg[0])
                    self.send(":{0} TOPIC {1} :{2}".format(self.bot, arg[0], ' '.join(arg[1:])))
                    
                    if self.chanflag("l", arg[0]):
                        self.log("Q", "topic", arg[0], ":"+' '.join(arg[1:]))
                        
                    self.msg(source, "Done.")
                else:
                    self.msg(source, "No permission")
            else:
                self.msg(source, "Invalid channel '{0}'".format(arg[0]))
        else:
            self.msg(source, "Syntax: SETTOPIC <#channel> <topic>")

    def onFantasy(self, uid, chan, args):
        flag = self.getflag(uid, chan)
        
        if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
            self.onCommand(uid, chan + " " + args)
