from chiruserv import Command, config
import psutil
from subprocess import Popen, PIPE

class version(Command):
	help = "Shows version of services"

	def onCommand(self, source, args):
		file = open("version", "r")
		version = file.read()
		file.close()
		self.msg(source, "ChiruServ {0}".format(version))
		self.msg(source, "Hash: {0}".format(self.encode_md5(open("list","r").read())))
		if self.isoper(source):
			self.msg(source, "Latest commit: {0}".format(Popen("git log --oneline -n 1", shell=True, stdout=PIPE).stdout.read().rstrip()))

		options = list()
		
		if self.ssl:
			options.append("SSL")
			
		if self.ipv6:
			options.append("IPv6")
			
		if self.status:
			options.append("Failover-Cluster")
			
			if self.isoper(source):
				self.msg(source, "Failover-IP: " + config.get("SERVICES", "address"))
				
		if len(options) != 0:
			self.msg(source, "Options: {0}".format(', '.join(options)))
			
		if self.isoper(source):
			self.msg(source, "If you're looking for more commands, check this out: https://github.com/ChiruclanDE/chiruserv-commands")
			
		self.msg(source, "Developed by ChiruclanDE (https://bitbucket.org/ChiruclanDE). Suggestions to hosting@chiruclan.de or mechi.community@yahoo.de.")