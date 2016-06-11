from flask import Flask, jsonify, request, abort, render_template
import sqlite3
import time
from datetime import timedelta, datetime


app = Flask(__name__)

#connect to the database 
conn = sqlite3.connect('fintech.db',check_same_thread=False)
db = conn.cursor()


def create_(amt, online_store):
    unix = time.time()
    date = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    db.execute('''
        INSERT INTO user(amt, online_store, time_stamp) VALUES(?, ?, ?)
        ''', (amt, online_store, date))
    conn.commit()

def update_(x, z):
    unix = time.time()
    date = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    db.execute('''
        UPDATE user 
        SET physical_store=?,
        payment_time=?
        WHERE user_ID=?;
        ''',(x, date ,z ))
    conn.commit()

#the "online store page"
@app.route('/')
def home():
    return render_template('form.html')

#check user (used by online store)
@app.route('/<int:user_id>', methods=['GET'])
def check_id(user_id):
    res = db.execute('''SELECT * FROM user''')
    tows = [row for row in db.fetchall() if row[0] == user_id]
    if tows[0][5] is None:
        confirms = False
    else:
        confirms = True
    return render_template("check.html", confirms = confirms)

#make "user" (used by online store) -- connected to forms
@app.route('/create', methods=['POST'])
def create_id():
    cost = request.form['cost']
    zipcode = request.form['zipcode']
    name = request.form['name']
    if cost != "" and zipcode != "":
        create_(cost, name)
        res = db.execute('''SELECT * FROM user''')
        user_id = [str(row[0]) for row in db.fetchall()]
        res = db.execute('''SELECT * FROM user''')
        start_time = [str(row[3]) for row in db.fetchall()]
        print start_time
        end_time = datetime.strptime(start_time[-1], "%Y-%m-%d %H:%M:%S")
        end_time += timedelta(hours=12)
        return render_template('confirm.html', zipcode = zipcode, user_id = user_id[-1], end_time= end_time)
    else:
        return render_template('try.html')

#approve (payment store)
@app.route('/<int:user_id>/update')
def update_id(user_id):
    res = db.execute('''SELECT * FROM user''')
    tows = [row for row in db.fetchall() if row[0] == user_id]
    if len(tows) == 0:
        abort(404)
    store = 'cvs'
    update_(store, user_id)
    return render_template("update.html", store = store , user_id = user_id)

if __name__ == '__main__':
    app.run(debug=True)
