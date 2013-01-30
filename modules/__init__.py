import os
import sys

for cmd in os.listdir("modules"):
	if cmd.endswith(".py"):
		cmd = ' '.join(cmd.split(".")[:-1])
		
		if cmd != "__init__":
			if not sys.modules.has_key("modules." + cmd):
				exec("import modules." + cmd)
			else:
				exec("reload(modules." + cmd + ")")