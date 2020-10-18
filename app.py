import numpy as np
from flask import Flask, request, jsonify, render_template,flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import time
from datetime import datetime
import pickle

app = Flask(__name__,
            static_folder='static')
app.debug = True
app.secret_key = "super secret key"

conn=mysql.connector.connect(user="root",           #enter username for your mysql usernmae , defaultis root
                            password="123456",         #enter the password
                            database="messlytix")         #enter the database
cur=conn.cursor()


model = pickle.load(open('messmodel.pkl', 'rb'))
def getattendees():
    query=("SELECT count(*) FROM feedback WHERE attendance=1")
    cur.execute(query)
    q=cur.fetchone()
    ans=q[0]
    return ans



@app.route('/', methods=["GET", "POST"])
# home
@app.route('/home')
def home():
    return render_template('index.html')

# student signup
@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('studentsignup.html')

# Choose
@app.route('/choose')
def choose():
    return render_template('choose.html')

# admin
@app.route('/admin')
def admin():
    attendees=getattendees()
    return render_template('admin.html',new_attendance='The number of attendees are {} \n'.format(attendees))

# analyse
@app.route('/analyse')
def analyse():
    return render_template('analyze.html')

# STUDENT
@app.route('/student')
def student():
    return render_template('student.html')

# submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        regno = request.form['regno']
        attendance = request.form['attendance']
        if attendance=="yes":
            attendance=1
        elif attendance=="no":
            attendance=0
        add_entry=("INSERT INTO feedback ""(regno,name,attendance)""VALUES(%s,%s,%s)")
        entry=(regno,name,attendance)
        try:
            cur.execute(add_entry,entry)
            conn.commit()
            return render_template('success.html')
        except mysql.connector.IntegrityError as err:
            flash("Error: Duplicate entry encountered",'error')
            return render_template("student.html")
        
        # else:
        #     return render_template('student.html')

@app.route('/submitdetails',methods=['GET','POST'])
def submitdetails():
    regno=request.form['regno']
    fname=request.form['fname']
    mname=request.form['mname']
    lname=request.form['lname']
    email=request.form.get('email')
    messid=request.form['messid']
    phno=request.form['phno']
    state=request.form['State']
    ts = time.time()
    timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    regtime=timestamp

    sdetails=("INSERT INTO student_admin (reg_no,fname,mname,lname,email_id,phone_no,reg_time,mess_id,state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    vals=(regno,fname,mname,lname,email,phno,regtime,messid,state)
    cur.execute(sdetails,vals)
    conn.commit()
    return render_template('success.html')


# prediction0
@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # int_features = [int(x) for x in request.form.values()]
    day = request.form.get("weekday")
    day1=4
    def convert_to_int(day):
        if(day=='Monday' or day=='monday'):
            return 0
        if(day == 'Tuesday' or day=='tuesday'):
            return 1
        if(day == 'Wednesday' or day=='wednesday'):
            return 2    
        if(day == 'Thursday' or day=='thursday'):
            return 3
        if(day == 'Friday' or day=='friday'):
            return 4
        if(day == 'Saturday' or day=='saturday'):
            return 5
        if(day == 'Sunday' or day=='sunday'):
            return 6
            
    day1=convert_to_int(day)
    
    def weekday():
        if(day1 != [5, 6]):
            return 0
        else:
            return 1

    def menu_rating():
        if day1 == 0:
            return 7
        elif day1 == 1:
            return 8.5
        elif day1 == 2:
            return 9.1
        elif day1 == 3:
            return 8.9
        elif day1 == 4:
            return 8.6
        elif day1 == 5:
            return 7
        elif day1 == 6:
            return 7.9

    def meanwastage():
        mean_wastage = 0
        if(day1 == 0):
            return 153.33333333333
        elif(day1 == 1):
            return 143
        elif(day1 == 2):
            return 107.233
        elif(day1 == 3):
            return 102.233
        elif(day1 == 4):
            return 112.344
        elif(day1 == 5):
            return 349.456
        elif(day1 == 6):
            return 330.233
    # final_features = [int_features]
    Wastage = 0
    weekend = weekday()
    mean_wastage = meanwastage()
    New_Menu_rating = menu_rating()
    prediction = model.predict([[day1, weekend, New_Menu_rating, Wastage]])
    print([day1, weekend, New_Menu_rating, Wastage])
    output = round(prediction[0], 3)
    attendees = getattendees()

    return render_template('admin.html', new_attendance='The number of attendees are {} \n'.format(attendees), prediction_text1='Menu rating for Today is : {} \n'.format(New_Menu_rating), prediction_text2='Average wastage on this day is: {} \n '.format(mean_wastage), prediction_text3='To avoid this wastage this is the predicted amount to be cooked :\n{}'.format(output))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run()
