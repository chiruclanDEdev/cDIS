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

class cmd_3_chanlev(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "CHANLEV"
    HELP = "Edit your channel records"
    NEED_AUTH = 1
    ENABLE_FANTASY = 1
    BOT_ID = '3'

    def onCommand(self, source, args):
        arg = args.split()
        
        if len(arg) == 1:
            if arg[0].startswith("#"):
                if self.getflag(source, arg[0]) != "0":
                    channel = arg[0]
                    self.msg(source, "Known users on {0}:".format(channel))
                    self.msg(source, "Username               Flag")
                    
                    for data in self.query("""SELECT "user", "flag" FROM "channels" WHERE "channel" = %s ORDER BY "flag", "user\"""", channel):
                        self.msg(source, " {0} {1} {2}".format(data["user"], " "*int(24-len(data["user"])), data["flag"]))
                        
                    self.msg(source, "End of list.")
                else:
                    self.msg(source, "Denied.")
            else:
                self.msg(source, "Invalid channel")
        elif len(arg) == 2:
            channel = arg[0]
            
            if channel.startswith("#"):
                if arg[1].startswith("#"):
                    username = arg[1][1:]
                    entry = False
                    user = False
                    
                    for data in self.query("select name from users where name = %s", username):
                        user = True
                        
                    for data in self.query("""SELECT "channel", "flag" FROM "channels" WHERE "user" = %s AND "channel" = %s""", username, channel):
                        self.msg(source, "Flags for #"+username+" on "+data["channel"]+": +"+data["flag"])
                        channel = data["channel"]
                        entry = True
                        
                    if user and not entry:
                        self.msg(source, "User #"+username+" is not known on "+channel+".")
                    elif not user:
                        self.msg(source, "Can't find user #"+username+".")
                else:
                    username = self.auth(self.uid(arg[1]))
                    entry = False
                    
                    for data in self.query("""select channel,flag from channels where "user" = %s and channel = %s""", username, channel):
                        self.msg(source, "Flags for "+arg[1]+" on "+data["channel"]+": +"+data["flag"])
                        channel = data["channel"]
                        entry = True
                        
                    if username != 0 and not entry:
                        self.msg(source, "User "+arg[1]+" is not known on "+channel+".")
                    if username == 0:
                        self.msg(source, "Can't find user "+arg[1]+".")
            else:
                self.msg(source, "Invalid channel")
        elif len(arg) == 3:
            channel = arg[0]
            
            if channel.startswith("#"):
                entry = False
                
                for channels in self.query("""select channel from channels where "user" = %s and flag = 'n' and channel = %s""", self.auth(source), arg[0]):
                        entry = True
                        channel = str(channels["channel"])
                        
                if entry:
                    if arg[2].lower() != "q" and arg[2].lower() != "a" and arg[2].lower() != "o" and arg[2] != "h" and arg[2] != "v":
                        self.msg(source, "Invalid flag: " + arg[2])
                        return 0
                        
                    if arg[1].startswith("#"):
                        username = arg[1][1:]
                        entry = False
                        
                        for data in self.query("select name from users where name = %s", username):
                            if str(self.auth(source)).lower() != username.lower():
                                if arg[2][0] != "-":
                                    self.query("""delete from channels where channel = %s and "user" = %s""", channel, username)
                                    self.query("insert into channels values (%s, %s, %s)", channel, username, arg[2][0])
                                    
                                    for data in self.sid(username):
                                        self.flag(data, channel)
                                        uflag = self.getflag(data, arg[0])
                                        
                                        if uflag != "v" and not self.chanflag("v", arg[0]):
                                            self.mode(arg[0], "-v "+data)
                                            
                                        if uflag != "h":
                                            self.mode(arg[0], "-h "+data)
                                            
                                        if uflag != "o" and uflag != "a" and uflag != "q" and uflag != "n":
                                            self.mode(arg[0], "-o "+data)
                                            
                                        if uflag != "a":
                                            self.mode(arg[0], "-a "+data)
                                            
                                        if uflag != "q" and uflag != "n":
                                            self.mode(arg[0], "-q "+data)
                                else:
                                    self.query("""delete from channels where channel = %s and "user" = %s""", arg[0], username)
                                    
                                    for data in self.sid(username):
                                        self.flag(data, channel)
                                        uflag = self.getflag(data, arg[0])
                                        
                                        if uflag != "v" and not self.chanflag("v", arg[0]):
                                            self.mode(arg[0], "-v "+data)
                                            
                                        if uflag != "h":
                                            self.mode(arg[0], "-h "+data)
                                            
                                        if uflag != "o" and uflag != "a" and uflag != "q" and uflag != "n":
                                            self.mode(arg[0], "-o "+data)
                                            
                                        if uflag != "a":
                                            self.mode(arg[0], "-a "+data)
                                            
                                        if uflag != "q" and uflag != "n":
                                            self.mode(arg[0], "-q "+data)
                                    
                                self.msg(source, "Done.")
                            else:
                                self.msg(source, "You cannot change your own flags!")
                            entry = True
                            
                        if not entry:
                            self.msg(source, "Can't find user "+arg[1]+".")
                    else:
                        username = self.auth(self.uid(arg[1]))
                        
                        if username != 0:
                            for data in self.query("select name from users where name = %s", username):
                                if str(self.auth(source)).lower() != username.lower():
                                    if arg[2][0] != "-":
                                        self.query("""delete from channels where channel = %s and "user" = %s""", channel, username)
                                        self.query("insert into channels values (%s, %s, %s)", channel, username, arg[2][0])
                                        
                                        for data in self.sid(username):
                                            self.flag(data, channel)
                                            uflag = self.getflag(data, arg[0])
                                            
                                            if uflag != "v" and not self.chanflag("v", arg[0]):
                                                self.mode(arg[0], "-v "+data)
                                                
                                            if uflag != "h":
                                                self.mode(arg[0], "-h "+data)
                                                
                                            if uflag != "o" and uflag != "a" and uflag != "q" and uflag != "n":
                                                self.mode(arg[0], "-o "+data)
                                                
                                            if uflag != "a":
                                                self.mode(arg[0], "-a "+data)
                                                
                                            if uflag != "q" and uflag != "n":
                                                self.mode(arg[0], "-q "+data)
                                    else:
                                        self.query("""delete from channels where channel = %s and "user" = %s""", arg[0], username)
                                        
                                        for data in self.sid(username):
                                            self.flag(data, channel)
                                            uflag = self.getflag(data, arg[0])
                                            
                                            if uflag != "v" and not self.chanflag("v", arg[0]):
                                                self.mode(arg[0], "-v "+data)
                                                
                                            if uflag != "h":
                                                self.mode(arg[0], "-h "+data)
                                                
                                            if uflag != "o" and uflag != "a" and uflag != "q" and uflag != "n":
                                                self.mode(arg[0], "-o "+data)
                                                
                                            if uflag != "a":
                                                self.mode(arg[0], "-a "+data)
                                                
                                            if uflag != "q" and uflag != "n":
                                                self.mode(arg[0], "-q "+data)
                                        
                                    self.msg(source, "Done.")
                                else:
                                    self.msg(source, "You cannot change your own flags!")
                                entry = True
                                
                            if not entry:
                                self.msg(source, "Can't find user "+arg[1]+".")
                else:
                    self.msg(source, "Denied.")
            else:
                self.msg(source, "Invalid channel")
        else:
            self.msg(source, "Syntax: CHANLEV <#channel> [<user> [<flag>]]")

    def onFantasy(self, uid, chan, args):
        flag = self.getflag(uid, chan)
        
        if flag == "n" or flag == "q" or flag == "a" or flag == "o" or flag == "h":
            self.onCommand(uid, chan + " " + args)
