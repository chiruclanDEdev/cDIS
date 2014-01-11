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
from time import time

class cmd_3_hello(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "HELLO"
    HELP = "Creates an account for you and sends the data to you"
    BOT_ID = '3'

    def onCommand(self, source, args):
        arg = args.split()
        
        if self.auth(source):
            self.msg(source, "HELLO is not available once you have authed.")
            return 0
            
        if len(arg) == 2:
            if self.nick(source).isalnum():
                exists = False
                
                for data in self.query("""SELECT "name" FROM "users" WHERE "email" = %s OR "name" = %s""", arg[0], self.nick(source)):
                        exists = True
                        
                if not exists:
                    if arg[0].find("@") != -1 and arg[0].find(".") != -1 and arg[0].lower() == arg[1].lower():
                        password = self.createPassword(arg[0] + arg[1])
                        self.query("""INSERT INTO "users" ("name", "pass", "email", "flags", "modes", "suspended") VALUES (%s, %s, %s,'n','+i','0')""", self.nick(source), password[1], arg[0])
                        self.msg(source, "The account %s has been created successfully. You can login now with /msg %s@%s AUTH account password" % (self.nick(source), self.bot_nick, self.services_name))
                        
                        if self.regmail == "1":
                            self.msg(source, "An email had been send to you with your password!")
                            self.mail(arg[0], "Your account on {0}".format(self.services_description), """Welcome to {4}\nYour account data:\n\nUser: {2}\nPassword: {5}\n\nAuth via "/MSG {6}@{7} AUTH {2} {5}"\nChange your password as soon as possible with "/MSG {6}@{7} NEWPASS <NEWPASSWORD>"!""".format(self.services_description, self.email, self.nick(source), arg[0], self.services_description, password[0], self.bot_nick, self.services_name))
                        else:
                            self.msg(source, """Use "/msg %s@%s auth %s %s" to auth""" % (self.bot_nick, self.services_name, self.nick(source), password[0]))
                            self.msg(source, "Change your password as soon as possible!")
                    else:
                        self.msg(source, "Invalid email %s!" % arg[0])
                else:
                    self.msg(source, "The account %s already exists or your email %s is used!" % (self.nick(source), arg[0]))
            else:
                self.msg(source, "Your nickname '" + self.nick(source) + "' contains invalid characters. Allowed are the characters A-z and 0-9.")
        else:
            self.msg(source, "Syntax: HELLO <email> <email>")
