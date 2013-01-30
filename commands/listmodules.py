from chiruserv import CSModules

class listmodules(CSModules):
	HELP = "Lists all active modules"
	NEED_OPER = 1
	
	def onCommand(self, uid, args):
		self.msg(uid, "-=- Lists all loaded modules -=-")
		
		for data in self.query("SELECT * FROM `modules`"):
			idname_space = " " * (10 - len(str(data["id"])))
			nameclass_space = " " * (40 - len(data["name"]))
			
			self.msg(uid, "ID: {id} {idname_space} {name} {nameclass_space} {class}".format(id=str(data["id"]), idname_space=idname_space, name=data["name"], nameclass_space=nameclass_space, class=data["class"]))
			
		self.msg(uid, "-=- End of list -=-")