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

import os
import sys

for mod in os.listdir("modules"):
	if mod.endswith(".py"):
		mod = ' '.join(mod.split(".")[:-1])
		
		if mod != "__init__":
			if "modules." + mod not in sys.modules:
				exec("import modules." + mod)
			else:
				exec("reload(modules." + mod + ")")