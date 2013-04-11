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
from subprocess import Popen, PIPE

class cmd_5_version(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "VERSION"
	HELP = "Shows version of services"
	BOT_ID = '5'

	def onCommand(self, uid, args):
		file = open("version", "r")
		version = file.read()
		file.close()
		self.msg(uid, "<= chiruclan.de IRC services {0} =>".format(version))
		self.msg(uid)
		self.msg(uid, "  Hash: {0}".format(Popen("git describe --match init --dirty=+ --abbrev=12 --tags", shell=True, stdout=PIPE).stdout.read().rstrip().split("-")[-1][1:]))
		
		if self.isoper(uid):
			self.msg(uid, "  Last update: {0}".format(Popen("git show -s --format=%ci", shell=True, stdout=PIPE).stdout.read().rstrip()))

		options = list()
		
		if self.ssl:
			options.append("SSL")
			
		if self.ipv6:
			options.append("IPv6")
				
		if len(options) != 0:
			self.msg(uid, "  Options: {0}".format(', '.join(options)))
			
		if self.isoper(uid):
			self.msg(uid, "  If you're looking for more modules, check this out: https://github.com/chiruclanDEdev/cDIS-Modules")
			
		self.msg(uid, "  Developed by chiruclan.de Development (https://github.com/chiruclanDEdev). Suggestions to hosting@chiruclan.de.")
		self.msg(uid)
		self.msg(uid, "<= Version end =>")