from chiruserv import CServMod
import time

class sched_gline(CServMod):
	MODULE_CLASS = "SCHEDULE"
	NEED_OPER = 1
	
	def onSchedule(self):
		while True:
			current_timestamp = time.time()
			
			results = self.query("SELECT `id`, `mask`, `timestamp` FROM `glines`")
			for row in results:
				expire_timestamp = int(row["timestamp"])
				
				if current_timestamp >= expire_timestamp:
					self.query("DELETE FROM `glines` WHERE `id` = ?", row["id"])
					self.send_serv("GLINE " + row["mask"])
					self.send_to_op("#G-line# Removed ID #" + str(row["id"]) + " (Hostmask: " + row["mask"] + ")")
					
			time.sleep(60)