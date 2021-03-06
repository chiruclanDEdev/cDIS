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

class cmd_3_setwhois(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "SETWHOIS"
    HELP = "Sets cool stuff in your whois"
    NEED_AUTH = 1
    BOT_ID = '3'

    def onCommand(self, source, args):
        arg = args.split()
        
        if len(arg) > 0:
            self.send(":{uid} SWHOIS {target} :{text}".format(uid=self.bot, target=source, text=' '.join(arg[0:])))
            self.msg(source, "Done.")
        else:
            self.send(":{uid} SWHOIS {target} :".format(uid=self.bot, target=source))
            self.msg(source, "Done.")