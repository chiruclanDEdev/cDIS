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

class cmd_3_unban(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "UNBAN"
    HELP = "Unbans somebody from your channel"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, uid, args):
        from fnmatch import fnmatch
        arg = args.split()
        
        if len(arg) == 2:
            if self.chanexist(arg[0]):
                flag = self.getflag(uid, arg[0])
                
                if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
                    if fnmatch(arg[1], "*!*@*"):
                        entry = False
                        
                        for data in self.query("select * from banlist where ban = %s and channel = %s", arg[1], arg[0]):
                            entry = True
                            
                        if entry:
                            self.query("delete from banlist where channel = %s and ban = %s", arg[0], arg[1])
                            self.msg(uid, "Done.")
                            self.mode(arg[0], "-b " + arg[1])
                        else:
                            self.msg(uid, arg[1] + " is not in the banlist of " + arg[0])
                    else:
                        self.msg(uid, "Invalid hostmask: " + arg[1])
                else:
                    self.msg(uid, "Denied.")
            else:
                self.msg(uid, "Invalid channel: " + arg[0])
        else:
            self.msg(uid, "Syntax: UNBAN <#channel> <hostmask>")

    def onFantasy(self, uid, chan, args):
        flag = self.getflag(uid, chan)
        
        if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
            self.onCommand(uid, chan + " " + args)
