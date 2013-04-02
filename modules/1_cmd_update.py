from cDIS import cDISModule

class 1_cmd_update(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "UPDATE"
	HELP = "Update the services"
	NEED_OPER = 1
	BOT_ID = '1'
	
	def onCommand(self, source, args):
		if not self.isoptype(source, "netadmin"):
			self.msg(source, "Denied.")
			return None
			
		_web = urllib2.urlopen("https://raw.github.com/chiruclanDEdev/cDIS/master/version")
		_version = _web.read()
		_web.close()
		
		if open("version", "r").read() != _version:
			_updates = len(os.listdir("sql/updates"))
			self.msg(source, "{0} -> {1}".format(open("version", "r").read(), _version))
			shell("git pull origin master")
			_files = os.listdir("sql/updates")
			__updates = len(_files)
			
			if __updates > _updates:
				while _updates != __updates:
					_updates += 1
					
					for sql in _files:
						if sql.startswith(str(_updates)+"_"):
							self.msg(source, " - Insert '{0}'".format(sql))
							file = open("sql/updates/"+sql, "r")
							
							for line in file.readlines():
								self.query(line)
								
							file.close()
							
			self.msg(source, "Done.")
			self.msg(source, "Please note that you have to restart the services manually.")