from app import *
def dailymsg():
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
            if a>d:
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
        for i in users.query.all():
            if i.email==x:
                nam2 = i.name
                break
        msg = Message('Scholly - Scholarship About to End', sender = app.config['MAIL_USERNAME'], recipients=[x])  
        msg.html = render_template('endscholarship.html',values = y,values2 = nam2)
        mails.send(msg)


schedule.every(1).seconds.do(dailymsg)
while True:
    time.sleep(60)