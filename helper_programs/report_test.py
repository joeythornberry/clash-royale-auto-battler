import time
import sys
sys.path.insert(0, 'clash_royale_auto_battler/')
import report_handler

rh = report_handler.ReportHandler()
time.sleep(5)
rh.complete_report()
rh.report()