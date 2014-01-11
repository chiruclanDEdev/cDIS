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

class cmd_4_listmodules(cDISModule):
    MODULE_CLASS = "COMMAND"
    COMMAND = "LISTMODULES"
    HELP = "Lists all active modules"
    NEED_OPER = 1
    BOT_ID = '4'
    
    def onCommand(self, uid, args):
        self.msg(uid, "-=- Lists all loaded modules -=-")
        
        for data in self.query("SELECT * FROM modules WHERE class != 'COMMAND'"):
            idname_space = " " * (5 - len(str(data["id"])))
            nameclass_space = " " * (20 - len(data["name"]))
            
            self.msg(uid, "ID: {id} {idname_space} Name: {name} {nameclass_space} Class: {tclass}".format(id=str(data["id"]), idname_space=idname_space, name=data["name"], nameclass_space=nameclass_space, tclass=data["class"]))
            
        self.msg(uid, "-=- End of list -=-")