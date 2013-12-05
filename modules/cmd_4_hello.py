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

class cmd_4_hello(cDISModule):
  MODULE_CLASS = "COMMAND"
  COMMAND = "HELLO"
  HELP = "Creates an account for users"
  NEED_OPER = 1
  BOT_ID = '4'

  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) == 2:
      if arg[0].isalnum():
        entry = False
        
        for data in self.query("""SELECT "name" FROM "users" WHERE "name" = %s""", arg[0]):
          entry = True
          
        if not entry:
          self.msg(uid, "Create account (%s, %s) ..." % (arg[0], arg[1]))
          self.query("""INSERT INTO "users" ("name", "pass", "email", "flags", "modes", "suspended") VALUES (%s, %s, %s, 'n', '+i', '0')""", arg[0], self.encode(arg[1]), self.bot_nick + "@" + self.services_name)
          self.msg(uid, "Done.")
        else:
          self.msg(uid, "%s is already in use." % arg[0])
      else:
        self.msg(uid, "The nickname '" + arg[0] + "' contains invalid characters. Allowed are the characters A-z and 0-9.")
    else:
      self.msg(uid, "Syntax: SAHELLO <account> <password>")