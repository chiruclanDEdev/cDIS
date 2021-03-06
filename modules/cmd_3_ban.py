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

class cmd_3_ban(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "BAN"
    HELP = "Bans somebody from your channel"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, uid, args):
        from fnmatch import fnmatch
        
        try:
            arg = args.split()
            
            if len(arg) == 2:
                if self.chanexist(arg[0]):
                    flag = self.getflag(uid, arg[0])
                    
                    if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
                        if fnmatch(arg[1], "*!*@*") and arg[1] != "*!*@*":
                            entry = False
                            
                            for data in self.query("select * from banlist where ban = %s and channel = %s", arg[1], arg[0]):
                                entry = True
                                
                            if not entry:
                                self.query("insert into banlist (channel, ban) values (%s, %s)", arg[0], arg[1])
                                self.msg(uid, "Done.")
                                self.enforceban(arg[0], arg[1])
                            else:
                                self.msg(uid, arg[1]+" is already in the banlist of "+arg[0])
                        else:
                            uentry = False
                            
                            for user in self.userlist(arg[0]):
                                if self.nick(user).lower() == arg[1].lower():
                                    uentry = True
                                    entry = False
                                    
                                    if self.gethost(user) == self.getip(user):
                                        if self.getip(user).find(":") != -1:
                                            ban = "*!*"+self.userhost(user).split("@")[0]+"@"+':'.join(self.getip(user).split(":")[:-2])+":*"
                                        else:
                                            ban = "*!*"+self.userhost(user).split("@")[0]+"@"+'.'.join(self.getip(user).split(".")[:-1])+".*"
                                    else:
                                        ban = "*!*"+self.userhost(user).split("@")[0]+"@*."+'.'.join(self.gethost(user).split(".")[1:])
                                        
                                    for data in self.query("select * from banlist where ban = %s and channel = %s", ban, arg[0]):
                                        entry = True
                                        
                                    if not entry:
                                        self.query("insert into banlist (channel, ban) values (%s, %s)", arg[0], ban)
                                        self.msg(uid, "Done.")
                                        self.enforceban(arg[0], ban)
                                    else:
                                        self.msg(uid, ban+" is already in the banlist of "+arg[0])
                                        
                            if not uentry:
                                self.msg(uid, "Can't find user "+arg[1]+" on "+arg[0]+".")
                    else:
                        self.msg(uid, "Denied.")
                else:
                    self.msg(uid, "Invalid channel: "+arg[0])
            else:
                self.msg(uid, "Syntax: BAN <#channel> <hostmask>")
        except Exception as e:
            pass

    def onFantasy(self, uid, chan, args):
        flag = self.getflag(uid, chan)
        
        if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
            self.onCommand(uid, chan + " " + args)
