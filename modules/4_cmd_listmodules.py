from cDIS import cDISModule

class 4_cmd_listmodules(cDISModule):
	MODULE_CLASS = "COMMAND"
	COMMAND = "LISTMODULES"
	HELP = "Lists all active modules"
	NEED_OPER = 1
	BOT_ID = '4'
	
	def onCommand(self, uid, args):
		self.msg(uid, "-=- Lists all loaded modules -=-")
		
		for data in self.query("SELECT * FROM `modules` WHERE `class` != 'COMMAND'"):
			idname_space = " " * (5 - len(str(data["id"])))
			nameclass_space = " " * (20 - len(data["name"]))
			
			self.msg(uid, "ID: {id} {idname_space} Name: {name} {nameclass_space} Class: {tclass}".format(id=str(data["id"]), idname_space=idname_space, name=data["name"], nameclass_space=nameclass_space, tclass=data["class"]))
			
		self.msg(uid, "-=- End of list -=-")