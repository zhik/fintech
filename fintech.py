import sqlite3
import time
import datetime
conn = sqlite3.connect('fintech.db')


db = conn.cursor()

# db.execute('''
# 	CREATE TABLE user (
# 	user_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	amt REAL,
# 	online_store TEXT,
# 	time_stamp TEXT,
# 	physical_store TEXT,
# 	payment_time TEXT
# 	)
# 	''')



def create_(amt, online_store):
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	db.execute('''
		INSERT INTO user(amt, online_store, time_stamp) VALUES(?, ?, ?)
		''', (amt, online_store, date))

create_(50, "target")

def update_(x, z):
	unix = time.time()
	date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	db.execute('''
		UPDATE user 
		SET physical_store=?,
		payment_time=?
		WHERE user_ID=?;
		''',(x, date ,z ))

#update_("tes124t", 1)

conn.commit()
conn.close