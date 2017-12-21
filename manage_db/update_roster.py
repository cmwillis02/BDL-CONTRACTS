import manage_rosters
import mfl_api

api= mfl_api.export()

process= manage_rosters.contract_process(api.rosters())
process.main_process()