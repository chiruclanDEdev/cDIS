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
from fnmatch import fnmatch

class cmd_3_dehalfop(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "DEHALFOP"
    HELP = "Removes halfop (+h) flag from you or someone on the channel"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, source, args):
        arg = args.split()
        
        if len(arg) == 1:
            if arg[0].startswith("#"):
                flag = self.getflag(source, arg[0])
                
                if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
                    self.mode(arg[0], "-h {0}".format(source))
                    self.msg(source, "Done.")
                else:
                    self.msg(source, "Denied.")
            else:
                self.msg(source, "Invalid channel")
        elif len(arg) == 2:
            if arg[0].startswith("#"):
                flag = self.getflag(source, arg[0])
                
                if flag == "n" or flag == "q" or flag == "a" or flag == "o":
                    for user in self.userlist(arg[0]):
                        for target in arg[1:]:
                            if fnmatch(self.nick(user).lower(), target.lower()):
                                self.mode(arg[0], "-h "+user)
                                
                                if self.chanflag("p", arg[0]):
                                    uflag = self.getflag(user, arg[0])
                                    
                                    if uflag == "h":
                                        self.mode(arg[0], "+h "+user)
                                        
                    self.msg(source, "Done.")
                else:
                    self.msg(source, "Denied.")
            else:
                self.msg(source, "Invalid channel")
        else:
            self.msg(source, "Syntax: DEHALFOP <#channel> [<nick> [<nick>]]")

    def onFantasy(self, uid, chan, args):
        flag = self.getflag(uid, chan)
        
        if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
            self.onCommand(uid, chan + " " + args)
