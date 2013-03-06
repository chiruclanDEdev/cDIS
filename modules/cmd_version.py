from cDIS import cDISModule
from subprocess import Popen, PIPE

class cmd_version(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "VERSION"
	HELP = "Shows version of services"

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