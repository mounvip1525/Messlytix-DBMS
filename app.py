import numpy as np
from flask import Flask, request, jsonify, render_template,flash,redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import time
import datetime
import pickle
from passlib.hash import sha256_crypt

usr='Admin' #Default Admin Username
pwd=sha256_crypt.hash('Password') #Default Admin Password
usrnm=""

app = Flask(__name__,
            static_folder='static')
app.debug = True
app.secret_key = "super secret key"

conn=mysql.connector.connect(host="remotemysql.com",
                            user="q97ShIgpvf",           #enter username for your mysql usernmae , defaultis root
                            password="kwoOpcYuzD",         #enter the password
                            database="q97ShIgpvf")         #enter the database
cur=conn.cursor()


model = pickle.load(open('messmodel.pkl', 'rb'))
def getattendees():
    query=("SELECT count(*) FROM feedback WHERE attendance=1")
    cur.execute(query)
    q=cur.fetchone()
    ans = q[0]
    return ans

def getmeal():
    now=datetime.datetime.now()
    actual_time=datetime.time(now.hour,now.minute,now.second)
    t1=datetime.time(12,0,0)
    t2=datetime.time(20,0,0)
    if(actual_time<t1):
        meal='breakfast'
    elif(actual_time>t1 and actual_time<t2):
        meal='lunch'
    else:
        meal='dinner'
    return meal

m=getmeal()
print(m)


def getmenuitemsbymeal(meal):
    global usrnm
    query=("select i.item_id,i.item_name from student_admin s,mess,contains c,menu_items i where s.reg_no=%s and s.mess_id=mess.mess_id and mess.date=%s and mess.meal=%s and mess.menu_id=c.menu_id and c.item_id=i.item_id")
    # ts = time.time()
    # timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timestamp=datetime.date(2020,1,11)
    vals=(usrnm,timestamp,meal)
    cur.execute(query,vals)
    result=cur.fetchall()
    return result

def getmenuid(meal):
    global usrnm
    query=("select m.menu_id,m.total_cal from student_admin s,mess,menu m where s.reg_no=%s and s.mess_id=mess.mess_id and mess.date=%s and mess.meal=%s and mess.menu_id=m.menu_id")
    timestamp=datetime.date(2020,1,11)
    vals=(usrnm,timestamp,meal)
    cur.execute(query,vals)
    result=cur.fetchall()
    return result


@app.route('/', methods=["GET", "POST"])
# home
@app.route('/home')
def home():
    return render_template('index.html')

# student signup
@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')

# Choose
@app.route('/choose')
def choose():
    return render_template('choose.html')
    
#student login
@app.route('/slogin',methods=['GET','POST'])
def studentlogin():
    return render_template('studentlogin.html')

# Admin Login
@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    return render_template('adminlogin.html')

# admin
@app.route('/admin',methods=['GET','POST'])
def admin():
    uname=request.form.get('username')
    pw=request.form.get('password')
    global usr
    global pwd
    attendees=getattendees()
    if(uname==usr and sha256_crypt.verify(pw,pwd)):
        return render_template('admin.html',new_attendance='The number of attendees are {} \n'.format(attendees))
    else:
        return redirect('/adminlogin')

# analyse
@app.route('/analyse')
def analyse():
    return render_template('analyze.html')

# STUDENT
@app.route('/student',methods=['GET','POST'])
def student():
    global usrnm 
    usrnm = request.form.get('username')
    pswd=request.form.get('password')
    print(usrnm,pswd)
    query=("SELECT password FROM student_admin WHERE reg_no = %s ")
    credentials=(usrnm,)
    cur.execute(query,credentials)
    ans=cur.fetchone()
    ans=ans[0]
    print(ans)
    if(sha256_crypt.verify(pswd,ans)):
        print(usrnm)
        return render_template('menu.html',items=getmenuitemsbymeal(getmeal()),ID=getmenuid(getmeal())), usrnm
    else:
        return redirect('/slogin')

#attendance page
@app.route('/attendance',methods=['POST','GET'])
def attendance():
    return render_template('student.html')

# submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        global usrnm
        regno=usrnm
        namequery=("SELECT fname FROM student_admin WHERE reg_no = %s")
        regno=(regno,)
        cur.execute(namequery,regno)
        regno=regno[0]
        name=cur.fetchone()
        name=name[0]
        attendance = request.form['attendance']
        if attendance=="yes":
            attendance=1
        elif attendance=="no":
            attendance=0
        add_entry="INSERT INTO feedback "+"(regno,name,attendance) "+"VALUES(%s,%s,%s)"
        entry=(regno,name,attendance)
        print(entry)
        try:
            cur.execute(add_entry,entry)
            conn.commit()
            return render_template('success.html')
        except mysql.connector.IntegrityError as err:
            flash("Error: Duplicate entry encountered",'error')
            return render_template("student.html")
        
        # else:
        #     return render_template('student.html')
        # return "ok"

@app.route('/submitdetails',methods=['GET','POST'])
def submitdetails():
    regno=request.form['regno']
    fname=request.form['fname']
    mname=request.form['mname']
    lname=request.form['lname']
    email=request.form.get('email')
    pwd=sha256_crypt.encrypt(request.form.get('password'))
    messid=request.form['messid']
    phno=request.form['phno']
    state=request.form['State']
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    regtime=timestamp

    sdetails=("INSERT INTO student_admin (reg_no,fname,mname,lname,email_id,phone_no,reg_time,mess_id,state,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    vals=(regno,fname,mname,lname,email,phno,regtime,messid,state,pwd)
    cur.execute(sdetails,vals)
    conn.commit()
    return render_template('success.html')

#success
app.route('/success', methods=['GET','POST'])
def success():
    return render_template('success.html')


#menu
@app.route('/menu',methods=['GET','POST'])
def menu():
    return render_template('menu.html',items=getmenuitemsbymeal(getmeal()),ID=getmenuid(getmeal()))


#special-request
@app.route('/specialrequest')
def specialrequest():
    return render_template('specialrequest.html')


#special-food
@app.route('/specialfood')
def specialfood():
    return render_template('specialfood.html')


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
