import sqlite3
from sqlite3 import Error
import datetime
import random

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("clash_royale_auto_battler.db")
cursor = connection.cursor()

create_runs_table = """CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY, 
    datetime TEXT NOT NULL,
    minutes FLOAT NOT NULL
)"""
create_battles_table = """CREATE TABLE IF NOT EXISTS battles (
    run_id INT NOT NULL, 
    minutes FLOAT NOT NULL,
    crowns INT NOT NULL,
    opponent_crowns INT NOT NULL,
    tokens_gained INT NOT NULL
)"""
cursor.execute(create_battles_table)
#now = datetime.datetime.now()
#now = now.strftime("%Y/%m/%d %H:%M:%S")
#minutes = random.randint(15,25)
#cursor.execute(f"INSERT INTO runs(datetime,minutes) VALUES (?,?)",(now,minutes))
run_id = random.randint(1,7)
crowns = random.randint(0,3)
opponent_crowns = random.randint(0,3)
tokens_gained = random.randint(30,200)
minutes = random.randint(2,5)
battle = {
    "run_id" : run_id,
    "crowns" : crowns,
    "opponent_crowns" : opponent_crowns,
    "tokens_gained" : tokens_gained,
    "minutes" : minutes
}
cursor.execute("""INSERT INTO battles(run_id,minutes,crowns,opponent_crowns,tokens_gained) 
VALUES(?,?,?,?,?)""",(battle["run_id"],battle["minutes"],battle["crowns"],battle["opponent_crowns"],battle["tokens_gained"]))
connection.commit()
runs = cursor.execute("SELECT * FROM battles ORDER BY minutes")
print(runs.fetchall())