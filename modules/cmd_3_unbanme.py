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

class cmd_3_unbanme(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "UNBANME"
    HELP = "Unbans you from a channel where you are known"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, uid, args):
        from fnmatch import fnmatch
        arg = args.split()
        
        if len(arg) == 1:
            if self.chanexist(arg[0]):
                flag = self.getflag(uid, arg[0])
                
                if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
                    for ban in self.query("select ban from banlist where channel = %s", arg[0]):
                        if self.gateway(uid):
                            crypthost = self.encode_md5(uid)+".gateway."+'.'.join(self.services_name.split(".")[-2:])
                            
                            if fnmatch(self.nick(uid)+"!"+self.userhost(uid).split("@")[0]+"@"+crypthost, ban["ban"]):
                                self.mode(arg[0], "-b "+ban["ban"])
                                self.msg(uid, " - removed '"+ban["ban"]+"'")
                                self.query("delete from banlist where channel = %s and ban = %s", arg[0], ban["ban"])
                                
                        for hostmask in self.hostmask(uid):
                            if fnmatch(hostmask, str(ban["ban"])):
                                self.mode(arg[0], "-b "+ban["ban"])
                                self.msg(uid, " - removed '"+ban["ban"]+"'")
                                self.query("delete from banlist where channel = %s and ban = %s", arg[0], ban["ban"])
                                
                    self.msg(uid, "Done.")
                else:
                    self.msg(uid, "Denied.")
            else:
                self.msg(uid, "Invalid channel: "+arg[0])
        else:
            self.msg(uid, "Syntax: UNBANME <#channel>")
