from flask import Flask, redirect, url_for, render_template, request, session, flash, g, jsonify, make_response,Markup,Response
from flask_mail import *
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import schedule
import time
import base64
import pytz

# def dailymsg():
#     dict = {}
#     month = {	'Jan':'01',
# 		'Feb':'02',
# 		'Mar':'03',
# 		'Apr':'04',
# 		'May':'05',
# 		'Jun':'06',
# 		'Jul':'07',
# 		'Aug':'08',
# 		'Sep':'09',
# 		'Oct':'10',
# 		'Nov':'11',
# 		'Dec':'12'		}
#     endschol = []
#     temp = scholarships.query.all()
#     now = datetime.now()
#     a = int(now.strftime("%d"))
#     b = int(now.strftime("%m"))
#     print(a,b)
#     for i in temp:
#         v = i.LastDate
#         l = v[-3:]
#         m = int(month[l])
#         d = int(v[:2])
#         print(v,l,m,d)
#         if b==m:
#             print(11111)
#             if a>d:
#                 print(5555)
#                 endschol.append(i.Name)
#                 gender = i.gender
#                 inputState = i.state
#                 inputcategory = i.category
#                 income = i.income
#                 currentstudy = i.minimumGraduation
#                 res0 = res1 = list(users.query.all())
#                 print(gender,inputState,inputcategory,income,currentstudy)
#                 if gender is None:
#                     print(00)
#                     res2 = users.query.all()
#                 elif gender=='All':
#                     res1 = res1
#                 else:
#                     print(res1)
#                     res2 = users.query.filter(users.gender == gender).all()
#                     res21 = users.query.filter(users.gender == 'All').all()
#                     # print(users.query.filter(users.gender == 'All').all())
#                     # print(res2,res21)
#                     res2 = res2 + res21
#                     # print(res2,res21)
#                     res13=list(set(res1).intersection(res2))
#                     if res13 is None:
#                         print("YES")
#                         res13 = res1
#                     res1 = res13
                     
#                 print(res1)
#                 if inputState is None:
#                     res3 = users.query.all()
#                 elif inputState == 'All':
#                     res1 = res1
#                 else:
#                     res3 = users.query.filter(users.inputstate == inputState).all()
#                     res31 = users.query.filter(users.inputstate == 'All').all()
#                     res3 = res3 + res31
#                     res13=list(set(res1).intersection(res3))
#                     print(res13)
#                     if res13 is None:
#                         res13 = res1 
#                     res1 = res13
#                 print(res1)
#                 if inputcategory is None:
#                     res4 = users.query.all()
#                 elif inputcategory == 'All':
#                     res1 = res1
#                 else:
#                     res4 = users.query.filter(users.inputcategory == inputcategory).all()
#                     res41 = users.query.filter(users.inputcategory == 'All').all()
#                     res4 = res4 + res41
#                     res13=list(set(res1).intersection(res4))
#                     if res13 is None:
#                         res13 = res1 
#                     res1 = res13
#                 print(res1)
#                 if income is None:
#                     res5 = users.query.all()
#                 elif income is None:
#                     res1 = res1
#                 else:
#                     res5 = users.query.filter(str(users.income) >= str(income)).all()
#                     res51 = users.query.filter(users.income == None).all()
#                     res5 = res5 + res51
#                     res13=list(set(res1).intersection(res5))
#                     if res13 is None:
#                         res13 = res1 
#                     res1 = res13
#                 print(res1)
#                 if currentstudy is None:
#                     res6 = users.query.all()
#                 elif currentstudy == 'All':
#                     res1 = res1
#                 else:
#                     res6 = users.query.filter(users.currentstudy == currentstudy).all()
#                     res61 = users.query.filter(users.currentstudy == 'All').all()
#                     res6 = res6 + res61
#                     res13=list(set(res1).intersection(res6))
#                     if res13 is None:
#                         res13 = res1 
#                     res1 = res13
#                 print(res1)
#                 # if res1:
#                 #     msg = Message('Scholly - Scholarship About to End', sender = app.config['MAIL_USERNAME'], recipients=[i.email for i in list(res1)])  
#                 #     msg.html = render_template('endscholarship.html',values = i.Name)
#                 #     mails.send(msg)
#                 for p in res1: 
#                     ema = p.email
#                     if ema not in dict:
#                         dict[ema] = [i.Name]
#                     else:
#                         lis = dict[ema]
#                         if i.Name not in lis:
#                             lis.append(i.Name)
#                             dict[ema] = lis
#     print(dict)
#     nam2 = ""
#     for x, y in dict.items():
#         for i in users.query.all():
#             if i.email==x:
#                 nam2 = i.name
#                 break
#         msg = Message('Scholly - Scholarship About to End', sender = app.config['MAIL_USERNAME'], recipients=[x])  
#         msg.html = render_template('endscholarship.html',values = y,values2 = nam2)
#         mails.send(msg)

# if __name__ == '__main__':
#     # dailymsg()
#     schedule.every(1).seconds.do(dailymsg)
#     while True:
#         schedule.run_pending()
#         time.sleep(60)
    
app = Flask(__name__)
app.secret_key = "satya"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scholly.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
app.config['TESTING'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'schollyweb@gmail.com'  
app.config['MAIL_PASSWORD'] = 'cvjx azbw hfjk xjjr'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mails = Mail(app)  

db = SQLAlchemy(app) 
adcode = "1881"
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    dob = db.Column(db.String(10))
    inputstate = db.Column(db.String(100))
    inputdistrict = db.Column(db.String(100))
    inputcategory = db.Column(db.String(100))
    firstgraduate = db.Column(db.String(100))
    currentstudy = db.Column(db.String(100))
    passedout = db.Column(db.String(100))
    income = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary,nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __init__(self, name, email, password, gender, dob, state, district, category, firstgraduate, currentstudy , passedout, income, photo):
        self.name = name
        self.email = email
        self.set_password(password)
        self.gender = gender
        self.dob = dob
        self.inputstate = state
        self.inputdistrict = district
        self.inputcategory = category
        self.firstgraduate = firstgraduate
        self.currentstudy = currentstudy
        self.passedout = passedout
        self.income = income
        self.photo = photo

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

class scholarships(db.Model):
    LastDate=db.Column(db.String(100))
    Name=db.Column(db.String(100))
    Name_link=db.Column(db.String(100))
    index=db.Column(db.Integer, primary_key=True)
    timestamp=db.Column(db.Integer)
    timestampString=db.Column(db.String(100)) 
    uid=db.Column(db.String(100))
    url=db.Column(db.String(100))
    url_uid=db.Column(db.Integer)
    gender=db.Column(db.String(100))
    state=db.Column(db.String(100))
    category=db.Column(db.String(100))
    income=db.Column(db.Integer)
    minimumGraduation=db.Column(db.String(100))
    def __init__(self,LastDate,Name,Name_link,index,timestamp,timestampString,uid,url,url_uid,gender,state,category,income,minimumGraduation):
        self.LastDate=LastDate
        self.Name=Name
        self.Name_link=Name_link
        self.index=index
        self.timestamp=timestamp
        self.timestampString=timestampString
        self.uid=uid
        self.url=url
        self.url_uid=url_uid
        self.gender=gender
        self.state=state
        self.category=category
        self.income=income
        self.minimumGraduation=minimumGraduation

@app.route("/")
def home():
    dict = {}
    month = {	'Jan':'01',
		'Feb':'02',
		'Mar':'03',
		'Apr':'04',
		'May':'05',
		'Jun':'06',
		'Jul':'07',
		'Aug':'08',
		'Sep':'09',
		'Oct':'10',
		'Nov':'11',
		'Dec':'12'		}
    endschol = []
    temp = scholarships.query.all()
    now = datetime.now()
    a = int(now.strftime("%d"))
    b = int(now.strftime("%m"))
    print(a,b)
    for i in temp:
        v = i.LastDate
        l = v[-3:]
        m = int(month[l])
        d = int(v[:2])
        print(v,l,m,d)
        if b==m:
            print(11111)
            if a<d:
                print(5555)
                endschol.append(i.Name)
                gender = i.gender
                inputState = i.state
                inputcategory = i.category
                income = i.income
                currentstudy = i.minimumGraduation
                res0 = res1 = list(users.query.all())
                print(gender,inputState,inputcategory,income,currentstudy)
                if gender is None:
                    print(00)
                    res2 = users.query.all()
                elif gender=='All':
                    res1 = res1
                else:
                    print(res1)
                    res2 = users.query.filter(users.gender == gender).all()
                    res21 = users.query.filter(users.gender == 'All').all()
                    # print(users.query.filter(users.gender == 'All').all())
                    # print(res2,res21)
                    res2 = res2 + res21
                    # print(res2,res21)
                    res13=list(set(res1).intersection(res2))
                    if res13 is None:
                        print("YES")
                        res13 = res1
                    res1 = res13
                     
                print(res1)
                if inputState is None:
                    res3 = users.query.all()
                elif inputState == 'All':
                    res1 = res1
                else:
                    res3 = users.query.filter(users.inputstate == inputState).all()
                    res31 = users.query.filter(users.inputstate == 'All').all()
                    res3 = res3 + res31
                    res13=list(set(res1).intersection(res3))
                    print(res13)
                    if res13 is None:
                        res13 = res1 
                    res1 = res13
                print(res1)
                if inputcategory is None:
                    res4 = users.query.all()
                elif inputcategory == 'All':
                    res1 = res1
                else:
                    res4 = users.query.filter(users.inputcategory == inputcategory).all()
                    res41 = users.query.filter(users.inputcategory == 'All').all()
                    res4 = res4 + res41
                    res13=list(set(res1).intersection(res4))
                    if res13 is None:
                        res13 = res1 
                    res1 = res13
                print(res1)
                if income is None:
                    res5 = users.query.all()
                elif income is None:
                    res1 = res1
                else:
                    res5 = users.query.filter(str(users.income) >= str(income)).all()
                    res51 = users.query.filter(users.income == None).all()
                    res5 = res5 + res51
                    res13=list(set(res1).intersection(res5))
                    if res13 is None:
                        res13 = res1 
                    res1 = res13
                print(res1)
                if currentstudy is None:
                    res6 = users.query.all()
                elif currentstudy == 'All':
                    res1 = res1
                else:
                    res6 = users.query.filter(users.currentstudy == currentstudy).all()
                    res61 = users.query.filter(users.currentstudy == 'All').all()
                    res6 = res6 + res61
                    res13=list(set(res1).intersection(res6))
                    if res13 is None:
                        res13 = res1 
                    res1 = res13
                print(res1)
                # if res1:
                #     msg = Message('Scholly - Scholarship About to End', sender = app.config['MAIL_USERNAME'], recipients=[i.email for i in list(res1)])  
                #     msg.html = render_template('endscholarship.html',values = i.Name)
                #     mails.send(msg)
                for p in res1: 
                    ema = p.email
                    if ema not in dict:
                        dict[ema] = [i.Name]
                    else:
                        lis = dict[ema]
                        if i.Name not in lis:
                            lis.append(i.Name)
                            dict[ema] = lis
    print(dict)
    nam2 = ""
    for x, y in dict.items():
        lin = []
        for i in users.query.all():
            if i.email==x:
                nam2 = i.name
                break
        for j in y:
            tem = scholarships.query.filter(scholarships.Name == j).first()
            lin.append(tem.Name_link)
            print(lin)
        msg = Message('Scholly - Scholarship About to End', sender = app.config['MAIL_USERNAME'], recipients=[x])  
        msg.html = render_template('endscholarship.html',values = zip(y,lin),values2 = nam2)
        mails.send(msg)
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():

    def verify_pass(hash_password, password):
        return check_password_hash(hash_password, password)

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        login = users.query.filter_by(email=email).first()
        if login and verify_pass(login.password, password):
            session["email"] = email
            session["password"] = password
            return redirect(url_for("index1"))
        
        elif login and not verify_pass(login.password, password):
            flash("Password doesn't match! Please check your password...")
            return redirect(url_for("login"))
        else:
            flash("Couldn't find user! Please sign up to continue...")
            return redirect(url_for("signup"))
    # else:
        
    #     if "email" in session:
    #         flash("Already Logged In!")
    #         return redirect(url_for("index1"))
        
       
    return render_template("login.html")

@app.route("/resetpassword", methods=["POST", "GET"])
def resetpassword():
    if request.method == "POST":
        email = request.form["email"]
        login = users.query.filter_by(email=email).first()
        if login:
           msg = Message('Scholly - Reset Password', sender = app.config['MAIL_USERNAME'], recipients=[email])  
           msg.html = render_template('resetpassword2.html',values=login.name)
           mails.send(msg)
           flash("Reset Password Link has been sent to your mail...")
           return redirect(url_for("resetpassword"))
        
        else:
            flash("Couldn't find user! Please sign up to continue...")
            return redirect(url_for("signup"))
        
    return render_template("resetpassword.html")

@app.route("/resetpassword3", methods=["POST", "GET"])
def resetpassword3():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["confirm_password"]
        login1 = users.query.filter_by(email=email).first()
        if login1:
           if password==password2 and password is not None and password2 is not None:
               setattr(login1,"password",generate_password_hash(password))
               try:
                   db.session.commit()
                   return redirect(url_for("thankyou"))
               except:
                    flash("Looks Like there was a problem!")
           else:
               flash("Password Doesn't Matched...")      
        
        else:
            flash("Couldn't find user! Please sign up to continue...")
            return redirect(url_for("signup"))
        
    return render_template("resetpassword3.html")

@app.route("/resetpasswordadmin0", methods=["POST", "GET"])
def resetpasswordadmin0():
    if request.method == "POST":
        email = request.form["email"]
        login12 = admin.query.filter_by(email=email).first()
        if login12:
           msg = Message('Scholly - Reset Password', sender = app.config['MAIL_USERNAME'], recipients=[email])  
           msg.html = render_template('resetpasswordadmin.html',values=login12.name)
           mails.send(msg)
           flash("Reset Password Link has been sent to your mail...")
           return redirect(url_for("resetpasswordadmin0"))
        
        else:
            flash("Couldn't find user! Please sign up to continue...")
            return redirect(url_for("signup"))
        
    return render_template("resetpasswordadmin0.html")


@app.route("/resetpasswordadmin1", methods=["POST", "GET"])
def resetpasswordadmin1():
    if request.method == "POST":
        email123 = request.form["email"]
        password12 = request.form["password"]
        password24 = request.form["confirm_password"]
        login2 = admin.query.filter_by(email=email123).first()
        if login2:
           if password12==password24 and password12 is not None and password24 is not None:
               setattr(login2,"password",generate_password_hash(password12))
            #    db.session.commit()
               try:
                   db.session.commit()
                   return redirect(url_for("thankyou"))
               except:
                    flash("Looks Like there was a problem!")
           else:
               flash("Password Doesn't Matched...")      
        
        else:
            flash("Couldn't find admin! Please login as user...")
            return redirect(url_for("signup"))
        
    return render_template("resetpasswordadmin1.html")
    
@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():

    def verify_pass(hash_password, password):
        return check_password_hash(hash_password, password)
    
    if request.method == "POST":
        gh = 1
        name = request.form["name"]
        email = request.form["email"]
        password1 = request.form["password"]
        admincode = request.form["admincode"]

        if admincode==adcode:
            login = admin.query.filter_by().all()
            for i in login:
                if email == i.email:
                    res = admin.query.filter_by(email=email).first()
                    gh = 0
                    break
            print(login)
            if gh==1:
                res = admin.query.filter_by(email=email).first()
                if res is None:
                    register = admin(name = name, email = email, password = password1)
                    db.session.add(register)
                    db.session.commit()
                    res = admin.query.filter_by(email=email).first()
                    print(res)
                elif res.name!=name:
                    flash("Your Name doesn't match...")
                    return redirect(url_for("adminlogin"))
                else:
                    register = admin(name = name, email = email, password = password1)
                    db.session.add(register)
                    db.session.commit()
                    res = admin.query.filter_by(email=email).first()
                    print(res)
                
            if res.name==name and verify_pass(res.password, password1):
                session["email"] = email
                return redirect(url_for("index2"))
            
            elif not verify_pass(res.password, password1):
                flash("Your Password doesn't match...")
                return redirect(url_for("adminlogin"))
        
        else:
            flash("Sorry, Admin Code doesn't match...")
            return redirect(url_for("adminlogin"))
    
    # else:
        
    #     if "email" in session:
    #         flash("Already Logged In!")
    #         return redirect(url_for("index2"))
        
       
    return render_template("adminlogin.html")
    
@app.route("/emailadmincode", methods=["POST", "GET"])
def emailadmincode():
    if request.method == "POST":
        email1 = request.form["email"]
        login = admin.query.filter_by(email=email1).first()
        if login:
           msg = Message('Scholly - Admin Code', sender = app.config['MAIL_USERNAME'], recipients=[email1])  
           msg.html = render_template('admincodeemail.html',values=login.name,values2=adcode)
           mails.send(msg)
           flash("Admin Code has been sent to your mail...")
           return redirect(url_for("emailadmincode"))
        
        else:
            flash("Couldn't find Admin! Please login in UserLogin...")
            return redirect(url_for("login"))
        
    return render_template("emailadmincode.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        mail = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        inputstate = request.form["inputState"]
        inputdistrict = request.form["inputDistrict"]
        inputcategory = request.form["inputcategory"]
        firstgraduate = request.form["firstgraduate"]
        currentstudy = request.form["currentstudy"]
        passedout = request.form["passedout"]
        income = request.form["income"]
        register1 = users.query.filter_by(email=mail).first()
        if register1:
            flash("Account already exist!")
            return redirect(url_for("signup"))
        else:
            register = users(name = name, email = mail, password = password, gender = gender, dob = dob, state = inputstate, district = inputdistrict, category = inputcategory, firstgraduate = firstgraduate, currentstudy = currentstudy, passedout = passedout, income=income,photo=None)
            db.session.add(register)
            db.session.commit()
            res = users.query.filter_by(email=mail).first()
            msg = Message('Scholly - Successfully logged In', sender = app.config['MAIL_USERNAME'], recipients=[mail])  
            msg.html = render_template('email.html',values=res.name)
            mails.send(msg)
        flash("Login to continue...")
        return redirect(url_for("login"))         
    return render_template("signup.html")

@app.route("/home2")
def index1():
    email = session["email"]
    res = users.query.filter_by(email=email).all()
    
    # msg = Message('Scholly- Successfully logged In', sender = app.config['MAIL_USERNAME'], recipients=[email])  
    # msg.html = render_template('email.html',values=res)
    # mail.send(msg)
    # 
    # mail.send_message("New message received",
    #                     sender=app.config['MAIL_USERNAME'],
    #                     recipients=[email],
    #                     body="Hello")

    return render_template("home2.html",values=res)
        

@app.route("/home3")
def index2():
    email = session["email"]
    print(email)
    temp = admin.query.filter_by(email=email).first()
    print(temp.name)
    return render_template("home3.html",values=temp.name)

@app.route("/viewscholarships")
def viewscholarship():
    
    return render_template("viewscholarships.html", values=scholarships.query.all())

@app.route("/addscholarships", methods=['POST', 'GET'])
def addscholarships():
    if request.method == "POST":
        print("test")
        lastDate = request.form["LastDate"]
        scholarship_name = request.form["scholarship_name"]
        scholarship_link = request.form["scholarship_link"]
        index = request.form["index"]
        timestamp = request.form["timestamp"]
        # Get the current timestamp
        formatted_timestamp = datetime.now(pytz.timezone('GMT'))
        # Format the timestamp
        time_stamp_string = "\"" + (formatted_timestamp.strftime('%a, %d %b %Y %H:%M:%S %Z')) + "\""
        # time_stamp_string = request.form["time_stamp_string"]
        uid = request.form["uid"]
        url = request.form["url"] 
        url_uid = request.form["url_uid"]
        gender = request.form["gender"]
        inputState = request.form["inputState"]
        inputcategory = request.form["inputcategory"]
        income = request.form["income"]
        currentstudy = request.form["currentstudy"]
        print(lastDate,scholarship_name)
        res = scholarships(LastDate=lastDate, Name=scholarship_name, Name_link=scholarship_link, index=index, timestamp=timestamp, timestampString=time_stamp_string,
                           uid=uid, url=url, url_uid=url_uid, gender=gender, state=inputState, category=inputcategory, income=income, minimumGraduation=currentstudy)
        print(res)
        db.session.add(res)
        db.session.commit()

        res1 = list(users.query.all())

        if gender=='':
            res2 = users.query.all()
        else:
            res2 = users.query.filter(users.gender == gender).all()
            res21 = users.query.filter(users.gender == 'All').all()
            res2 = res2 + res21
        res1=list(set(res1).intersection(res2))

        if inputState=='':
            res3 = users.query.all()
        else:
            res3 = users.query.filter(users.inputstate == inputState).all()
            res31 = users.query.filter(users.inputstate == 'All').all()
            res3 = res3 + res31
        res1=list(set(res1).intersection(res3))

        if inputcategory=='':
            res4 = users.query.all()
        else:
            res4 = users.query.filter(users.inputcategory == inputcategory).all()
            res41 = users.query.filter(users.inputcategory == 'All').all()
            res4 = res4 + res41
        res1=list(set(res1).intersection(res4))

        if income=='':
            res5 = users.query.all()
        else:
            res5 = users.query.filter(str(users.income) >= str(income)).all()
            res51 = users.query.filter(users.income == None).all()
            res5 = res5 + res51
        res1=list(set(res1).intersection(res5))

        if currentstudy=='':
            res6 = users.query.all()
        else:
            res6 = users.query.filter(users.currentstudy == currentstudy).all()
            res61 = users.query.filter(users.currentstudy == 'All').all()
            res6 = res6 + res61
        res1=list(set(res1).intersection(res6))

        if res1:
            msg = Message('Scholly - New Scholarship Unlocked', sender = app.config['MAIL_USERNAME'], recipients=[i.email for i in list(res1)])  
            msg.html = render_template('newscholarship.html')
            mails.send(msg)
        
        # msg = Message('Scholly - New Scholarship Unlocked', sender = app.config['MAIL_USERNAME'], recipients=[allemails])  
        # msg.html = render_template('newscholarship.html')
        # mails.send(msg)
        
        flash("Successfully Entered...")
        return redirect(url_for("addscholarships"))
    else:
        return render_template("addscholarships.html")
    

@app.route("/displayprof",methods=['GET' , 'POST'])
def displayprof():
        email = session["email"]
        password = session["password"]
        res = users.query.filter_by(email=email).all()
        # profile = users.query.get(res.id)
        # res.photo = base64.b64encode(res.photo).decode('utf-8')
        if res:
            return render_template("displayprof.html", values=res)
        else:
            flash("No data found!")
        return render_template("displayprof.html")

@app.route('/image/<int:image_id>')
def display_image(image_id):
    image = users.query.get(image_id)
    return Response(image.photo, mimetype='image/jpeg')


@app.route("/profile",methods=['GET' , 'POST'])
def profile():
        email = session["email"]
        password = session["password"]
        res = users.query.filter_by(email=email).all()
        if res:
            return render_template("profile.html", values=res)
        else:
            flash("No data found!")
        return render_template("profile.html")

@app.route("/removephoto")
def removephoto():
    email = session["email"]
    # print(email)
    temp = users.query.filter_by(email=email).first()
    # print(temp.name)
    setattr(temp,"photo",None)
    db.session.commit()
    return redirect(url_for("profile"))

@app.route("/update",methods=['GET' , 'POST'])
def update():
        email = session["email"]
        password = session["password"]
        name1 = request.form.get("name")
        gender1 = request.form.get("gender")
        dob1 = request.form.get("dob")
        inputstate1 = request.form.get("inputState")
        inputdistrict1 = request.form.get("inputDistrict")
        inputcategory1 = request.form.get("inputcategory")
        firstgraduate1 = request.form.get("firstgraduate")
        currentstudy1 = request.form.get("currentstudy")
        passedout1 = request.form.get("passedout")
        income1 = request.form.get("income")
        pic = request.files['pic']
        # profile = users(photo.read())
        # db.session.add(profile)
        # db.session.commit()
        if pic is not None:
            photo1=pic.read()
        name_to_update = users.query.filter_by(email=email).first()
        print(name_to_update)

        if name1 is not None:
            setattr(name_to_update,"name",name1)

        if gender1 is not None:
            setattr(name_to_update,"gender",gender1.lower())

        if dob1 is not None:
            setattr(name_to_update,"dob",dob1)

        if inputstate1 is not None:
            setattr(name_to_update,"inputstate",inputstate1)

        if inputdistrict1 is not None:
            setattr(name_to_update,"inputdistrict",inputdistrict1)

        if inputcategory1 is not None:
            setattr(name_to_update,"inputcategory",inputcategory1)

        if firstgraduate1 is not None:
            setattr(name_to_update,"firstgraduate",firstgraduate1)

        if currentstudy1 is not None:
            setattr(name_to_update,"currentstudy",currentstudy1)

        if passedout1 is not None:
            setattr(name_to_update,"passedout",passedout1)

        if income1 is not None:
            setattr(name_to_update,"income",income1)
        
        if not pic:
            setattr(name_to_update,"photo",name_to_update.photo)
        else:
            setattr(name_to_update,"photo",photo1)


        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return redirect(url_for("displayprof"))
        except:
            flash("Looks Like there was a problem!")
            return redirect(url_for("displayprof"))


@app.route("/search_forme", methods = ["POST",  "GET"])
def search_forme():
    if request.method =="POST":
        email = session["email"]
        password = session["password"]
        person = users.query.filter_by(email=email).first()
        Gender = person.gender
        State = person.inputstate
        Category = person.inputcategory
        minigrad = person.currentstudy
        Income = person.income
        
        res7 = scholarships.query.all()
        # for i in res7:
        #         if i.Name=='aaa':
        #             print("YES MAMA")
        #             if i.gender=='':
        #                 print(i.gender,type(i.gender))
        if Gender!='':
            res2 = scholarships.query.filter(scholarships.gender == Gender).all()
            res21 = scholarships.query.filter(scholarships.gender == 'All').all()
            res22 = scholarships.query.filter(scholarships.gender == '').all()
            res2 = res2 + res21 + res22
            res7=list(set(res7).intersection(res2))
            # for i in res7:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in gender")
        else:
            res7 = res7
            # for i in res7:
            #     if i.Name=='aaa':
            #         print("nanan YES MAMA")
            print(1111)
            
            # print(res7)

        if State!='':
            res3 = scholarships.query.filter(scholarships.state == State).all()
            res31 = scholarships.query.filter(scholarships.state == 'All').all()
            res32 = scholarships.query.filter(scholarships.state == '').all()
            res3 = res3 + res31 + res32
            res7=list(set(res7).intersection(res3))
            # for i in res7:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in state")
        else:
            # print('s')
            res7 = res7
            # print(res7)

        if Category!='':
            res4 = scholarships.query.filter(scholarships.category == Category).all()
            # print(res4)
            res41 = scholarships.query.filter(scholarships.category == 'All').all()
            res42 = scholarships.query.filter(scholarships.category == '').all()
            res4 = res4 + res41 + res42
            res7=list(set(res7).intersection(res4))
            # for i in res7:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in cat")

        else:
            # print('c')
            res7 = res7
            # print(res4)
            # print(res7)

        if Income!='':
            
            res5 = scholarships.query.filter(scholarships.income <= Income).all()
            # for i in res5:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in res5")
            res51 = scholarships.query.filter(scholarships.income == None).all()
            res52 = scholarships.query.filter(scholarships.income == '').all()
            res5 = res5 + res51 + res52
            res7=list(set(res7).intersection(res5))
            # for i in res7:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in inc")
        else:
            # print('i')
            res7 = res7

        if minigrad!='':
            res6 = scholarships.query.filter(scholarships.minimumGraduation == minigrad).all()
            res61 = scholarships.query.filter(scholarships.minimumGraduation == 'All').all()
            res62 = scholarships.query.filter(scholarships.minimumGraduation == '').all()
            res6 = res6 + res61 + res62
            res7=list(set(res7).intersection(res6))
            # for i in res7:
            #     if i.Name=='hhh':
            #         print("YES hhh i am in mini")
        else:
            print('m')
            res7 = res7
        # for i in res7:
        #         if i.Name=='aaa':
        #             print("nanan YES MAMA")

        i = 0
        j = i+1
        while(i<len(res7)-1):
            if res7[i].Name == res7[j].Name:
                res7.pop(j)
            else:
                j = j+1

            if j==len(res7):
                i = i+1
                j = i+1
        if res7:
            print(res7)
            for i in res7:
                print(i.LastDate)
            # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
            # msg.body =  "hello"
            # mail.send(msg)
        
            month1 = {	'Jan':'01',
            'Feb':'02',
            'Mar':'03',
            'Apr':'04',
            'May':'05',
            'Jun':'06',
            'Jul':'07',
            'Aug':'08',
            'Sep':'09',
            'Oct':'10',
            'Nov':'11',
            'Dec':'12'		}
            newsch = []
            now = datetime.now()
            b1 = int(now.strftime("%m"))
            print(b1)
            for i in res7:
                strin = i.timestampString.strip('"')
                print(strin)
                parsed_timestamp = datetime.strptime(strin, '%a, %d %b %Y %H:%M:%S %Z')
                month_string = parsed_timestamp.strftime('%b')
                month_new = month1[month_string]
                print(int(month_new))
                if b1==int(month_new):
                    newsch.append(i)
                    res7.remove(i)
            return render_template("scholar.html", values=res7,values2 = newsch)
        
        else:
            flash("No data Found!")
            flash("Displaying all")
            # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
            # msg.body =  "hello"
            # mail.send(msg)
            return render_template("scholar.html", values=scholarships.query.all())
        
    return render_template("search_forme.html")


@app.route("/search", methods = ["POST",  "GET"])
def search():
    
    email = session["email"]
    if request.method == "POST":
        Name = request.form["firstname"]
        Gender = request.form["gender"]
        State = request.form["inputState"]
        Category = request.form["inputcategory"]
        Income = request.form["income"]
        minigrad = request.form["currentstudy"]
        search = "%{}%".format(Name)
        res = scholarships.query.all()
        res7 =''
        if Name!='':
            res1 = scholarships.query.filter(scholarships.Name.like(search)).all()
            res7=list(set(res).intersection(res1))
        else:
            # res1 = scholarships.query.all()
            # res7=list(set(res).intersection(res1))
            res7 = list(res)

        if Gender!='':
            res2 = scholarships.query.filter(scholarships.gender == Gender).all()
            res21 = scholarships.query.filter(scholarships.gender == 'All').all()
            res2 = res2 + res21
            res7=list(set(res7).intersection(res2))
            # print(res7)

        # else:
        #     res2 = scholarships.query.all()

    
        if State!='':
            res3 = scholarships.query.filter(scholarships.state == State).all()
            res31 = scholarships.query.filter(scholarships.state == 'All').all()
            res3 = res3 + res31
            res7=list(set(res7).intersection(res3))
            # print(res7)

        # else:
        #     res3 = scholarships.query.all()

        if Category!='':
            res4 = scholarships.query.filter(scholarships.category == Category).all()
            # print(res4)
            res41 = scholarships.query.filter(scholarships.category == 'All').all()
            res4 = res4 + res41
            res7=list(set(res7).intersection(res4))
            # print(res4)
            # print(res7)
        # else:
            # res4 = scholarships.query.all()

        if Income!='':
            res5 = scholarships.query.filter(scholarships.income >= Income).all()
            res51 = scholarships.query.filter(scholarships.income == None).all()
            res5 = res5 + res51
            res7=list(set(res7).intersection(res5))
        # else: 
        if minigrad!='':
            res6 = scholarships.query.filter(scholarships.minimumGraduation == minigrad).all()
            res61 = scholarships.query.filter(scholarships.minimumGraduation == 'All').all()
            res6 = res6 + res61
            res7=list(set(res7).intersection(res6))

        # else:
        #     res6 = scholarships.query.all()
        # print(res7)
        i = 0
        j = i+1
        while(i<len(res7)-1):
            if res7[i].Name == res7[j].Name:
                res7.pop(j)
            else:
                j = j+1

            if j==len(res7):
                i = i+1
                j = i+1
        
        if res7:
            print(res7)
            # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
            # msg.body = "hello"
            # mail.send(msg)
            return render_template("scholar.html", values=res7)
          
        elif res1:
            if (Name == ''):
                flash("No data Found!")
                flash("Displaying all")
                #return render_template("scholar.html")
            # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
            # msg.body = "hello"
            # mail.send(msg)
            return render_template("scholar.html", values=res1)
        
        else:
            flash("No data Found!")
            flash("Displaying all")
            # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
            # msg.body =  "hello"
            # mail.send(msg)
            return render_template("scholar.html", values=scholarships.query.all())
    else:
        # msg = Message('Scholarships applicable for you', sender = app.config['MAIL_USERNAME'], recipients=[email])  
        # msg.body =  "hello"
        # mail.send(msg)
        print("hai")
        return render_template("search.html")
    
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


    
@app.route("/logout")
def logout():
    if "email" in session:
        flash("You have been logged out successfully!", "info")
        session.pop("email", None)
        session.pop("password", None)
    return redirect(url_for("home"))

@app.route("/thankyou")
def thankyou():
    
    return render_template("thankyou.html")

# schedule.every().minute.do(dailymsg)

# if __name__ == '__main__':
#     # Start the scheduling loop
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
