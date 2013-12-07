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

class cmd_6_send(cDISModule):
  HELP = "Send a message to someone"
  NEED_AUTH = 1
  MODULE_CLASS = "COMMAND"
  COMMAND = "SEND"
  BOT_ID = '6'
  
  def onCommand(self, uid, args):
    arg = args.split()
    
    if len(arg) >= 2:
      user = self.user(arg[0])
      if not user:
        self.msg(uid, "No such user '%s'." % arg[0])
        return 0
      
      account = self.auth(uid)
      subject = "No subject"
      message = ' '.join(arg[1:])
      if (message.find(": ") != -1):
        subject = message.split(": ")[0]
        message = message.split(": ")[1]
      
      if (len(subject) > 64): subject = subject[:64]
      if (len(message) > 2048): message = message[:2048]
      self.query("""INSERT INTO "memo" ("recipient", "sender", "subject", "message", "read_state") VALUES (%s, %s, %s, %s, %s)""", user, account, subject, message, False)
      self.msg(uid, "Done.")
      self.memo(user)
    else:
      self.msg(uid, "Syntax: SEND <recipient> [<subject>:] <message>")
      self.msg(uid, "  You can switch to a new line using: `")