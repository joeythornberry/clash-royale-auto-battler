import sqlite3
from sqlite3 import Error
import exit_codes
    
create_runs_table = """CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY, 
    datetime TEXT NOT NULL,
    minutes FLOAT NOT NULL,
    exit_code TEXT NOT NULL
)"""
create_battles_table = """CREATE TABLE IF NOT EXISTS battles (
    run_id INT NOT NULL, 
    datetime TEXT NOT NULL,
    minutes FLOAT NOT NULL,
    crowns INT NOT NULL,
    opponent_crowns INT NOT NULL,
    tokens_gained INT NOT NULL
)"""
create_errors_table = """CREATE TABLE IF NOT EXISTS errors (
    run_id INT NOT NULL,
    datetime TEXT NOT NULL,
    error_type TEXT NOT NULL
)"""

def insert_run(cursor,datetime,minutes,exit_code):
    cursor.execute("""INSERT INTO runs(datetime,minutes,exit_code)
    VALUES (?,?,?)""", (datetime,minutes,exit_code))

def insert_battle(cursor,run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained):
    cursor.execute("""INSERT INTO battles (run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained)
    VALUES (?,?,?,?,?,?)""", (run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained))

def insert_error(cursor,run_id,datetime,error_type):
    cursor.execute("""INSERT INTO errors (run_id,datetime,error_type)
    VALUES (?,?,?)""", (run_id,datetime,error_type))