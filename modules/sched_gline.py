from chiruserv import CServMod
import time
import thread

class sched_gline(CServMod):
	MODULE_CLASS = "SCHEDULE"
	
	def onSchedule(self):
		while True:
			current_timestamp = time.time()
			self.msg("$*", "Running minutely cleanup task...")
			
			results = self.query("SELECT `id`, `mask`, `timestamp` FROM `glines`")
			for row in results:
				expire_timestamp = int(row["timestamp"])
				
				if current_timestamp >= expire_timestamp:
					self.query("DELETE FROM `glines` WHERE `id` = ?", row["id"])
					self.send_serv("GLINE " + row["mask"])
					
			self.msg("$*", "Minutely cleanup task successful...")
			
			time.sleep(60)