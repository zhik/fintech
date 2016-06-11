from flask import Flask, jsonify, request, abort, render_template
import sqlite3
import time
import datetime

app = Flask(__name__)

conn = sqlite3.connect('fintech.db',check_same_thread=False)
db = conn.cursor()

def create_(amt, online_store):
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    db.execute('''
        INSERT INTO user(amt, online_store, time_stamp) VALUES(?, ?, ?)
        ''', (amt, online_store, date))
    conn.commit()

def update_(x, z):
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    db.execute('''
        UPDATE user 
        SET physical_store=?,
        payment_time=?
        WHERE user_ID=?;
        ''',(x, date ,z ))
    conn.commit()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/<int:user_id>', methods=['GET'])
def check_id(user_id):
    res = db.execute('''SELECT * FROM user''')
    tows = [row for row in db.fetchall() if row[0] == user_id]
    if tows[0][5] is None:
        return jsonify('False')
    else:
        return jsonify('True')

@app.route('/create', methods=['POST'])
def create_id():
    cost = request.form['cost']
    zipcode = request.form['zipcode']
    name = request.form['name']
    if cost != "" and zipcode != "":
        create_(cost, name)
        return render_template('confirm.html', zipcode = zipcode)
    else:
        return render_template('try.html')

@app.route('/<int:user_id>/update')
def update_id(user_id):
    #go to user_id and add id & time
    res = db.execute('''SELECT * FROM user''')
    tows = [row for row in db.fetchall() if row[0] == user_id]
    if len(tows) == 0:
        abort(404)
    store = 'cvs'
    update_(store, user_id)
    return jsonify(tows)

if __name__ == '__main__':
    app.run(debug=True)
