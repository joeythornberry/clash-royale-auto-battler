import sqlite3
from sqlite3 import Error
import exit_codes
    
create_runs_table = """CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY, 
    datetime TEXT NOT NULL,
    minutes FLOAT NOT NULL,
    exit_code TEXT NOT NULL,
    error_count INT NOT NULL
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
    error_type TEXT NOT NULL,
    screenshot BLOB NOT NULL
)"""

def insert_run(cursor,datetime,minutes,exit_code,error_count):
    cursor.execute("""INSERT INTO runs(datetime,minutes,exit_code,error_count)
    VALUES (?,?,?,?)""", (datetime,minutes,exit_code,error_count))

def insert_battle(cursor,run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained):
    cursor.execute("""INSERT INTO battles (run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained)
    VALUES (?,?,?,?,?,?)""", (run_id,datetime,minutes,crowns,opponent_crowns,tokens_gained))

def insert_error(cursor,run_id,datetime,error_type,screenshot):
    cursor.execute("""INSERT INTO errors (run_id,datetime,error_type,screenshot)
    VALUES (?,?,?,?)""", (run_id,datetime,error_type,screenshot))

