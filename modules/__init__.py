import os
import sys

for mod in os.listdir("modules"):
	if mod.endswith(".py"):
		mod = ' '.join(mod.split(".")[:-1])
		
		if mod != "__init__":
			if not sys.modules.has_key("modules." + mod):
				exec("import modules." + mod)
			else:
				exec("reload(modules." + mod + ")")