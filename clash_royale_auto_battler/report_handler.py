import time

SECONDS_IN_A_MINUTE = 60

class ReportHandler:
    def __init__(self):
        print("initializing report")
        self.start_time = round(time.time())
        self.end_time = None
        self.total_runtime_minutes = None
        self.battles = []

    def log_battle(self,battle_time_seconds,crowns,opponent_crowns,tokens_gained):
        battle_time_minutes = round((battle_time_seconds/SECONDS_IN_A_MINUTE),1)
        self.battles.append({
            "battle_time_minutes" : battle_time_minutes,
            "crowns" : crowns,
            "opponent_crowns" : opponent_crowns,
            "tokens_gained" : tokens_gained
        })

    def complete_report(self):
        self.end_time = round(time.time())
        self.total_runtime_minutes = round(((self.end_time - self.start_time)/SECONDS_IN_A_MINUTE),1)

    def report(self):
        if self.end_time == None:
            print("run not yet finished (no end time found). did you call complete_report?")
            return "error"
        print("runtime: "+str(self.total_runtime_minutes)+" minutes")
        print(str(self.battles))