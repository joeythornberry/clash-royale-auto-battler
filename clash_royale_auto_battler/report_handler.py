import time
import exit_codes

SECONDS_IN_A_MINUTE = 60

class ReportHandler:
    def __init__(self):
        print("initializing report")
        self.report = {
            "start_time" : round(time.time()),
            "end_time" : None,
            "total_runtime_minutes" : None,
            "battles" : [],
            "errors" : [],
        }

    def log_battle(self,battle_time_seconds,crowns,opponent_crowns,tokens_gained):
        battle_time_minutes = round((battle_time_seconds/SECONDS_IN_A_MINUTE),1)
        self.report["battles"].append({
            "end_time" : time.asctime(),
            "battle_time_minutes" : battle_time_minutes,
            "crowns" : crowns,
            "opponent_crowns" : opponent_crowns,
            "tokens_gained" : tokens_gained
        })

    def log_error(self,error_type):
        self.report["errors"].append({
            "time" : time.asctime(),
            "error_type" : error_type
        })

    def complete_report(self):
        self.report["end_time"] = round(time.time())
        self.report["total_runtime_minutes"] = round(((self.report["end_time"] - self.report["start_time"])/SECONDS_IN_A_MINUTE),1)

    def deliver_report(self):
        if self.report["end_time"] == None:
            print("run not yet finished (no end time found). did you call complete_report?")
            return "error"
        print(str(self.report))