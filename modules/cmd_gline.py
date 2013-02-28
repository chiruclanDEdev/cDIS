from chiruserv import CServMod
import time

class cmd_gline(CServMod):
	MODULE_CLASS = "COMMAND"
	COMMAND = "GLINE"
	HELP = "G-Line actions"
	NEED_OPER = 1

	def onCommand(self, uid, args):
		arg = args.split()
		
		if len(arg) == 1:
			if arg[0].lower() == "list":
				current_timestamp = int(time.time())
				self.msg(uid, "-=- List of G-lines -=-")
				
				result = self.query("SELECT `id`, `mask`, `timestamp` FROM `glines`")
				for row in result:
					id = str(row["id"])
					mask = str(row["mask"])
					timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
					
					id_mask_space = " "*int(10 - len(id))
					mask_time_space = " "*int(25 - len(mask))
					
					self.msg(uid, "ID: {id} {id_mask_space} Hostmask: {mask} {mask_time_space} Time left: {time_left}".format(id=id, id_mask_space=id_mask_space, mask=mask, mask_time_space=mask_time_space, time_left=timestamp))
					
				self.msg(uid, "-=- End of list -=-")
			else:
				self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
		elif len(arg) == 2:
			if arg[0].lower() == "search":
				current_timestamp = int(time.time())
				self.msg(uid, "-=- List of G-lines -=-")
				
				result = self.query("SELECT `id`, `mask`, `timestamp` FROM `glines` WHERE `id` LIKE ? OR `mask` LIKE ?", "%" + arg[1][1:] + "%", "%" + arg[1] + "%")
				for row in result:
					id = str(row["id"])
					mask = str(row["mask"])
					timestamp = self.convert_timestamp(int(int(row["timestamp"])- current_timestamp))
					
					id_mask_space = " "*int(10 - len(id))
					mask_time_space = " "*int(25 - len(mask))
					
					self.msg(uid, "ID: {id} {id_mask_space} Hostmask: {mask} {mask_time_space} Time left: {time_left}".format(id=id, id_mask_space=id_mask_space, mask=mask, mask_time_space=mask_time_space, time_left=timestamp))
					
				self.msg(uid, "-=- End of list -=-")
			else:
				self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
			elif arg[0].lower() == "del":
				result = self.query("SELECT `id`, `mask` FROM `glines` WHERE `id` = ? OR `mask` = ?", arg[1][1:], arg[1])
					
				for row in result:
					self.query("DELETE FROM `glines` WHERE `id` = ?", row["id"])
					self.send_serv("GLINE " + row["mask"])
					self.msg(uid, "G-line ID #" + str(row["id"]) + " has been removed.")
					
				self.msg(uid, "Done.")
			else:
				self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
		elif len(arg) == 3:
			if arg[0].lower() == "set":
				if arg[2].isdigit():
					tuid = self.uid(arg[1])
					ttime = int(arg[2])
					
					if not tuid.lower() == arg[1].lower():
						if not self.isoper(tuid):
							for row in self.query("SELECT `id` FROM `glines` WHERE `mask` = ?", "*@" + self.getip(tuid)):
								self.msg(uid, "This entry is already active (ID #" + str(row["id"]) + ")!")
								return 0
								
							etime = int(time.time()) + int(ttime * 60)
							self.query("INSERT INTO `glines` (`mask`, `timestamp`) VALUES (?, ?)", "*@" + self.getip(tuid), etime)
							self.gline(tuid)
							self.msg(uid, "Done.")
						else:
							self.msg(uid, "Denied.")
					else:
						self.msg(uid, "Failed. User is not online.")
				else:
					self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
			else:
				self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
		elif len(arg) > 3:
			if arg[0].lower() == "set":
				if arg[2].isdigit():
					tuid = self.uid(arg[1])
					ttime = int(arg[2])
					treason = ' '.join(arg[3:])
					
					if not tuid.lower() == arg[1].lower():
						if not self.isoper(tuid):
							for row in self.query("SELECT `id` FROM `glines` WHERE `mask` = ?", "*@" + self.getip(tuid)):
								self.msg(uid, "This entry is already active (ID #" + str(row["id"]) + ")!")
								return 0
								
							etime = int(time.time()) + int(ttime * 60)
							self.query("INSERT INTO `glines` (`mask`, `timestamp`) VALUES (?, ?)", "*@" + self.getip(tuid), etime)
							self.gline(tuid, treason)
							self.msg(uid, "Done.")
						else:
							self.msg(uid, "Denied.")
					else:
						self.msg(uid, "Failed. User not online.")
				else:
					self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
			else:
				self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
		else:
			self.msg(uid, "Syntax: GLINE <set/del/list/search> [<user> <time (in minutes)> [<reason>]]")
