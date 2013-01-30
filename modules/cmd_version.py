from chiruserv import CServMod
from subprocess import Popen, PIPE

class cmd_version(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "VERSION"
	HELP = "Shows version of services"

	def onCommand(self, source, args):
		file = open("version", "r")
		version = file.read()
		file.close()
		self.msg(source, "ChiruServ {0}".format(version))
		self.msg(source, "Hash: {0}".format(Popen("git describe --match init --dirty=+ --abbrev=12 --tags", shell=True, stdout=PIPE).stdout.read().rstrip().split("-")[-1][1:]))
		
		if self.isoper(source):
			self.msg(source, "Last update: {0}".format(Popen("git show -s --format=%ci", shell=True, stdout=PIPE).stdout.read().rstrip()))

		options = list()
		
		if self.ssl:
			options.append("SSL")
			
		if self.ipv6:
			options.append("IPv6")
				
		if len(options) != 0:
			self.msg(source, "Options: {0}".format(', '.join(options)))
			
		if self.isoper(source):
			self.msg(source, "If you're looking for more commands, check this out: https://bitbucket.org/ChiruclanDE/chiruserv-commands")
			
		self.msg(source, "Developed by ChiruclanDE (https://bitbucket.org/ChiruclanDE). Suggestions to hosting@chiruclan.de.")