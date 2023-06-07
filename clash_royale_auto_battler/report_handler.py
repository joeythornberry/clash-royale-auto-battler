import time
import exit_codes
import sqlite3
from sqlite3 import Error
import datetime
import sql_handler

SECONDS_IN_A_MINUTE = 60

class ReportHandler:
    def __init__(self):
        print("initializing report")
        self.report = {
            "datetime" : datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "minutes" : None,
            "exit_code" : None,
            "battles" : [],
            "errors" : [],
        }

    def log_battle(self,battle_time_seconds,crowns,opponent_crowns,tokens_gained):
        battle_time_minutes = round((battle_time_seconds/SECONDS_IN_A_MINUTE),1)
        self.report["battles"].append({
            "datetime" : datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "minutes" : battle_time_minutes,
            "crowns" : crowns,
            "opponent_crowns" : opponent_crowns,
            "tokens_gained" : tokens_gained
        })

    def log_error(self,error_type):
        self.report["errors"].append({
            "time" : time.asctime(),
            "error_type" : error_type
        })

    def complete_report(self,total_runtime_seconds,exit_code):
        self.report["minutes"] = round(total_runtime_seconds/SECONDS_IN_A_MINUTE,1)
        self.report["exit_code"] = exit_code

    def deliver_report(self):
        if self.report["exit_code"] == None:
            print("run not yet finished (no end time found). did you call complete_report?")
            return "error"
        print(str(self.report))

    def save_report_as_sql(self):
        try:
            connection = sqlite3.connect("clash_royale_auto_battler.db")
            cursor = connection.cursor()
            cursor.execute(sql_handler.create_runs_table)
            cursor.execute(sql_handler.create_battles_table)
            cursor.execute(sql_handler.create_errors_table)
            sql_handler.insert_run(cursor,self.report["datetime"],self.report["minutes"],self.report["exit_code"])
            run_id = cursor.lastrowid
            for battle in self.report["battles"]:
                sql_handler.insert_battle(cursor,run_id,battle["datetime"],battle["minutes"],battle["crowns"],battle["opponent_crowns"],battle["tokens_gained"])
            for error in self.report["errors"]:
                sql_handler.insert_error(cursor,run_id,error["datetime"],error["error_type"])
            connection.commit()
            connection.close()
        except Error as error:
            print(error)
            return exit_codes.UNOBSTRUCTIVE_ERROR
        
rh = ReportHandler()
rh.report = {'datetime': '2023/06/07 15:36:32', 'minutes': 3.5, 'exit_code': 'success', 'battles': [{'datetime': '2023/06/07 15:40:02', 'minutes': 3.0, 'crowns': 0, 'opponent_crowns': 1, 'tokens_gained': 156}], 'errors': []}
rh.save_report_as_sql()