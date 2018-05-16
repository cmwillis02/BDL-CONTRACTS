try:
	import manage_rosters
except:
	from manage_db import manage_rosters
try:
	import mfl_api
except:
	from manage_db import mfl_api

api= mfl_api.export()
print ('complete export')

process= manage_rosters.contract_process(api.rosters())
process.main_process()