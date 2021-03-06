import codecs
from collections import Counter
from flask import Flask, render_template, jsonify, json, request
# from flask.sessions import SecureCookieSessionInterface
# from flask_session import Session
# import redis
# from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS, cross_origin
import pyquran as q
import random
from tajweed import Tajweed
import matplotlib.pyplot as plt
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, TajweedRules, Practice, Test, Student, UserWork, UserWorkStats
import os
import glob
from flask_bcrypt import Bcrypt

# import "../Tajweed Apis/tajweed.ghunnah.json"


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "kelly-af-01221990")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///tajweed')
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)
connect_db(app)


# db = SQLAlchemy()
# sess = Session()
# sess.init_app(app)

CORS(app)
# session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)

wordDict = Counter()

tajweedJSON = {}
idghaamNoGhunnahJSON = {}

# @app.after_request
# def cookies(response):
#     same_cookie = session_cookie
#     response.headers.add("Set-Cookie", "my_cookie={same_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
#     return response

@app.route('/')
def start():
    return render_template('home.html')


@app.route("/api/get_explanation", methods=["POST"])
def get_expl():
    rule = request.json["ruleChosen"]
    explanationObj = Tajweed.getExplanation(rule)
    print(explanationObj)

    return ( jsonify(explanationObj=explanationObj), 200 )


@app.route("/api/generate_ayat", methods=["POST"])
def generate_ayat():

    text = []
    f = open(r'/app/quran-uthmani.txt', encoding='utf-8')
    # f = open(r'C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\quran-uthmani.txt', encoding='utf-8')
    for line in f:
        text.append(line)
    
    data = json.loads(request.data)

    activity = data["activity"]
    rule =data["ruleChosen"]
    print('**************rule', rule)

    ruleDetails = Tajweed.Select_dict_path(rule)[0]
    beg = Tajweed.Select_dict_path(rule)[1]
    end = Tajweed.Select_dict_path(rule)[2]

    ayatRange = int(data["range"])
    ayat = []

    # if rule != "idghaam_no_ghunnah" and rule != "iqlab" and rule != "idghaam_mutaqaribayn" and rule != "idghaam_mutajanisayn" and rule != 'idghaam_shafawi' and rule != 'ghunnah' and activity != "learn":
    #     surahNumber = random.randint(beg, end)

    #     fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=False)

    #     while len(fullSurah) < ayatRange:
    #         surahNumber = random.randint(beg, end)
    #         fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=True)

    #     if len(fullSurah) > ayatRange:
    #         firstAyat = random.randint(1, (len(fullSurah) - ayatRange))

    #         surahName = q.quran.get_sura_name(surahNumber)
    #         for n in range(firstAyat, firstAyat+ayatRange):   
    #             target = [line for line in text if f"{surahNumber}|{n}|" in line]
    #             lineArr = target[0].split('|')
    #             test_ayat = lineArr[2]

    #             ayatData = {
    #                 "test_ayat" : test_ayat
    #             }
    #             ruleMarker = []
    #             for item in ruleDetails:
    #                 if item["surah"] == surahNumber and item["ayah"] == n:
    #                     ruleMarker.append(item)

    #             ayatData["rule"] = ruleMarker
    #             ayatData["surahNumber"] = surahNumber
    #             ayatData["ayahNumber"] = n
                
    #             ayat.append(ayatData)
    
    # elif activity == "learn" or rule == "idghaam_no_ghunnah" or rule == "iqlab" or rule == "idghaam_mutaqaribayn" or rule == "idghaam_mutajanisayn" or rule == 'idghaam_shafawi' or rule == 'ghunnah': 
    firstAyat = random.randint(1, (len(ruleDetails) - ayatRange))

    while len(ayat) < ayatRange:
        surahNumber = ruleDetails[firstAyat]["surah"]
        # surahNumber = 16
        surahName = q.quran.get_sura_name(surahNumber)
        ayatNumber = ruleDetails[firstAyat]["ayah"]
        # ayatNumber = 2
        target = [line for line in text if f"{surahNumber}|{ayatNumber}|" in line]
        lineArr = target[0].split('|')
        test_ayat = lineArr[2]

        ayatData = {
            "test_ayat" : test_ayat
        }

        ruleMarker = []
        for item in ruleDetails:
            if item["surah"] == surahNumber and item["ayah"] == ayatNumber:
                ruleMarker.append(item)

        ayatData["rule"] = ruleMarker
        ayatData["surahNumber"] = surahNumber
        ayatData["ayahNumber"] = ayatNumber

        ayat.append(ayatData)

        firstAyat = firstAyat + 1

        if ruleDetails[firstAyat]["surah"] == surahNumber:
            while ruleDetails[firstAyat]["ayah"] == ayatNumber:
                firstAyat = firstAyat + 1

    return ( jsonify(rule=rule, ayatRange=ayatRange, ayat=ayat), 200 )



@app.route("/api/auth", methods=["POST"])
def auth():
    data = json.loads(request.data)

    userData = json.loads(data["data"])
    mode = json.loads(data["mode"])
    allTajArr = []

    if mode == 'register':
    
        try:
            user = User.register(
                first_name = userData["first_name"], 
                last_name = userData["last_name"], 
                email = userData["email"], 
                username = userData["username"],
                password = userData["password"],
                account_type = userData["account_type"])

            db.session.commit()

            if user:
                isAuthenticated = True

                userObj = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "account_type": user.account_type,
                    "students": []
                }

                rules = TajweedRules.query.all()

                ruleList = [{'code': r.code, 'name': r.name} for r in tajweed_rules]

                for r in rules:
                    user_work = UserWork(rule=r.code, practice_ayah_count=0, test_ayah_count=0, total_correct=0, total_out_of=0)
                    db.session.add(user_work)
                    db.session.commit()
                    
                    user_work_stats = UserWorkStats(user_id=user.id, work_id=user_work.id)
                    db.session.add(user_work_stats)
                    db.session.commit()

                allWork = user.work

                for i in allWork:  
                                
                    allTajObj = {
                        "code" : i.rule,
                        "practice_ayah_count": 0,
                        "test_ayah_count": 0,
                        "total_correct": 0,
                        "total_out_of": 0
                    }

                    practice = []
                    test = []

                    for r in i.practice:
                        p_stats = {
                            'practice_date': r.practice_date,
                            'ayah_count': r.ayah_count
                        }
        
                        practice.insert(0, p_stats)  

                    for t in i.test:
                        t_stats = {
                            'test_date': t.test_date,
                            'test_ayah_count': t.test_ayah_count,
                            'test_score_correct': t.test_score_correct,
                            'test_out_of_count': t.test_out_of_count,
                            'test_score_composite': t.test_score_composite
                        }
        
                        test.insert(0, t_stats) 
                        
        
                    allTajObj['practice'] = practice  
                    allTajObj['test'] = test
                    

                    allTajArr.append(allTajObj)

                return (jsonify(isAuthenticated=isAuthenticated, user=userObj, tajweed=allTajArr, rules=ruleList), 200 )
            else:
                isAuthenticated = False
                message = 'Oops! This user might already exist. We could not create your account. Please try again.'
                return (jsonify(isAuthenticated=isAuthenticated, message=message), 400 )

        except IntegrityError:
            isAuthenticated = False
            message = 'Oops! This user might already exist. We could not create your account. Please try again.'
            return (jsonify(isAuthenticated=isAuthenticated, message=message), 500 )

    elif mode == 'login':
        try:
            user = User.authenticate(
            username = userData["username"], 
            password = userData["password"])

            db.session.commit()

            if user:
                isAuthenticated = True

                tajweed_rules = TajweedRules.query.all()
                ruleList = [{'code': r.code, 'name': r.name} for r in tajweed_rules]

                userObj = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "account_type": user.account_type,
                    "students": []
                }

                
                students = []
                for i in user.students:
                    students.append(
                        {"first_name": i.student_firstName,
                        "last_name": i.student_lastName,
                        "username": i.student_username,
                        "email": i.student_email}
                        )
                
                userObj["students"] = students

                allTaj = user.work

                for i in allTaj:
                    allTajObj = {
                        "code" : i.rule,
                        "practice_ayah_count": i.practice_ayah_count,
                        "test_ayah_count": i.test_ayah_count,
                        "total_correct": i.total_correct,
                        "total_out_of": i.total_out_of
                    }

                    practice = []
                    test = []

                    for r in i.practice:
                        p_stats = {
                            'practice_date': r.practice_date,
                            'ayah_count': r.ayah_count
                        }
        
                        practice.insert(0, p_stats)  

                    for t in i.test:
                        t_stats = {
                            'test_date': t.test_date,
                            'test_ayah_count': t.test_ayah_count,
                            'test_score_correct': t.test_score_correct,
                            'test_out_of_count': t.test_out_of_count,
                            'test_score_composite': t.test_score_composite
                        }
        
                        test.insert(0, t_stats) 
                    
        
                    allTajObj['practice'] = practice  
                    allTajObj['test'] = test
                    

                    allTajArr.append(allTajObj)

            
                return (jsonify(isAuthenticated=isAuthenticated, user=userObj, tajweed=allTajArr, rules=ruleList), 200 )
            else:
                isAuthenticated = False
                message = 'Oops! Wrong username or password. Please try again.'
                return (jsonify(isAuthenticated=isAuthenticated, message=message), 401 )
            
        except IntegrityError:
            isAuthenticated = False
            message = 'Oops! Wrong username or password. Please try again.'
            return (jsonify(isAuthenticated=isAuthenticated, message=message), 500 )
    

@app.route('/api/logout')
def logout():
    isAuthenticated = False

    return (jsonify(response=isAuthenticated), 200 )

@app.route('/api/reset_practice', methods=["POST"])
def reset_practice():
    username = request.json['username'] 
    stats = request.json['stats']

    user = User.query.filter_by(username=username).first()

    for r in stats:
        print('rule', r.split('-')[0])
        user_rule = [c for c in user.work if c.rule == r.split("-")[0]]
        print(user_rule)
        user_rule[0].practice_ayah_count = 0

        practice_stats = user_rule[0].practice

        for p in practice_stats:
            removedP = Practice.query.filter_by(id=p.id).delete()

            db.session.commit()

        db.session.commit()

        practice_stats = user_rule[0].practice
        print('practice array after reseting practice', practice_stats)
    
    allTaj = user.work

    allTajArr = []

    for i in allTaj:
        allTajObj = {
            "code" : i.rule,
            "practice_ayah_count": i.practice_ayah_count,
            "test_ayah_count": i.test_ayah_count,
            "total_correct": i.total_correct,
            "total_out_of": i.total_out_of
        }

        practice = []
        test = []

        for r in i.practice:
            p_stats = {
                'practice_date': r.practice_date,
                'ayah_count': r.ayah_count
            }

            practice.insert(0, p_stats)  

        for t in i.test:
            t_stats = {
                'test_date': t.test_date,
                'test_ayah_count': t.test_ayah_count,
                'test_score_correct': t.test_score_correct,
                'test_out_of_count': t.test_out_of_count,
                'test_score_composite': t.test_score_composite
            }

            test.insert(0, t_stats) 
        

        allTajObj['practice'] = practice  
        allTajObj['test'] = test
        

        allTajArr.append(allTajObj)

    if request.json['account'] == 'self':
    
        return (jsonify(allTajArr=allTajArr), 200)
    elif request.json['account'] == 'student':
        my_student = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "account_type": user.account_type,
                    "tajweed": allTajArr
                }
        return (jsonify(my_student=my_student), 200)



@app.route('/api/reset_test', methods=["POST"])
def reset_test():
    username = request.json['username'] 
    stats = request.json['stats']

    user = User.query.filter_by(username=username).first()

    for r in stats:
        print('rule', r.split('-')[0])
        user_rule = [c for c in user.work if c.rule == r.split("-")[0]]
        user_rule[0].test_ayah_count = 0
        user_rule[0].total_correct = 0
        user_rule[0].total_out_of = 0

        test_stats = user_rule[0].test

        for t in test_stats:
            removedT = Test.query.filter_by(id=t.id).delete()

            db.session.commit()

        db.session.commit()

        test_stats = user_rule[0].test
        print('test arry after resettng tests', test_stats)

    allTaj = user.work

    allTajArr = []

    for i in allTaj:
        allTajObj = {
            "code" : i.rule,
            "practice_ayah_count": i.practice_ayah_count,
            "test_ayah_count": i.test_ayah_count,
            "total_correct": i.total_correct,
            "total_out_of": i.total_out_of
        }

        practice = []
        test = []

        for r in i.practice:
            p_stats = {
                'practice_date': r.practice_date,
                'ayah_count': r.ayah_count
            }

            practice.insert(0, p_stats)  

        for t in i.test:
            t_stats = {
                'test_date': t.test_date,
                'test_ayah_count': t.test_ayah_count,
                'test_score_correct': t.test_score_correct,
                'test_out_of_count': t.test_out_of_count,
                'test_score_composite': t.test_score_composite
            }

            test.insert(0, t_stats) 
        

        allTajObj['practice'] = practice  
        allTajObj['test'] = test
        

        allTajArr.append(allTajObj)

    if request.json['account'] == 'self':
    
        return (jsonify(allTajArr=allTajArr), 200)
    elif request.json['account'] == 'student':
        my_student = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "account_type": user.account_type,
                    "tajweed": allTajArr
                }
        return (jsonify(my_student=my_student), 200)


@app.route('/api/update_practice', methods=['POST'])
def update_practice():
    username = request.json["username"]
    stats = request.json["stats"]

    allTajArr = []

    user = User.query.filter_by(username=username).first()
    user_rule = [c for c in user.work if c.rule == stats['rule']]

    
    practice = Practice(practice_date=db.func.now(), ayah_count=stats['ayah_count'], rule_id=user_rule[0].id, user=user.id)

    db.session.add(practice)
    db.session.commit()  

    user_rule[0].practice_ayah_count = user_rule[0].practice_ayah_count + stats['ayah_count']

    db.session.commit()

    allTaj = user.work

    userObj = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "account_type": user.account_type
    }

    for i in allTaj:
        allTajObj = {
        "code" : i.rule,
        "practice_ayah_count": i.practice_ayah_count,
        "test_ayah_count": i.test_ayah_count,
        "total_correct": i.total_correct,
        "total_out_of": i.total_out_of
        }

        practice = []

        for r in i.practice:
            p_stats = {
                'practice_date': r.practice_date,
                'ayah_count': r.ayah_count
            }
            
            practice.insert(0, p_stats)  
            
        allTajObj['practice'] = practice  

        test = [p['test'] for p in session['tajweed'] if p['code'] == i.rule]
        
        for t in test:
            allTajObj['test'] = t

        
        allTajArr.append(allTajObj)
    
    return (jsonify(userObj=userObj, allTajArr=allTajArr), 200)


@app.route('/api/update_test', methods=['POST'])
def update_test():
    username = request.json["username"]
    stats = request.json["stats"]

    allTajArr = []

    user = User.query.filter_by(username=username).first()
    user_rule = [c for c in user.work if c.rule == stats['rule']]
    
    test = Test(test_date=db.func.now(), test_ayah_count=stats['ayah_count'], test_score_correct=stats['correct'], test_out_of_count=stats['out_of'], test_score_composite=stats['score'], rule_id=user_rule[0].id, user=user.id)

    db.session.add(test)
    db.session.commit()  

    user_rule[0].test_ayah_count = user_rule[0].test_ayah_count + stats['ayah_count']
    user_rule[0].total_correct = user_rule[0].total_correct + stats['correct']
    user_rule[0].total_out_of = user_rule[0].total_out_of + stats['out_of']

    db.session.commit()

    allTaj = user.work

    userObj = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "account_type": user.account_type
    }

    for i in allTaj:
        allTajObj = {
        "code" : i.rule,
        "practice_ayah_count": i.practice_ayah_count,
        "test_ayah_count": i.test_ayah_count,
        "total_correct": i.total_correct,
        "total_out_of": i.total_out_of
        }

        test = []

        for t in i.test:
            t_stats = {
                'test_date': t.test_date,
                'test_ayah_count': t.test_ayah_count,
                'test_score_correct': t.test_score_correct,
                'test_out_of_count': t.test_out_of_count,
                'test_score_composite': t.test_score_composite
            }

            test.insert(0, t_stats)

        allTajObj['test'] = test  

        practice = [p['practice'] for p in session['tajweed'] if p['code'] == i.rule]
        
        for p in practice:
            allTajObj['practice'] = p

        allTajArr.append(allTajObj)

    return (jsonify(userObj=userObj, allTajArr=allTajArr), 200)

  
@app.route('/api/update_user', methods=['POST'])
def update_user():
    userData = request.json["user"]

    user = User.query.filter_by(username=userData['username']).first()

    if (user["username"] == userData["username"]):
        user.first_name = userData["first_name"]
        user.last_name = userData["last_name"]
        user.email = userData["email"]

        db.session.add(user)
        db.session.commit()

    return (jsonify(user=userData), 200)

@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    userPassword = request.json["data"]
  
    new_pass = User.reset_pass(username=userPassword["username"], current_password=userPassword["current"], new_password=userPassword['new'])

    return (jsonify(response='success'), 200)

@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    data = request.json["data"]

    user = User.query.filter_by(username=data['username']).first()

    if data['username'] == user['username']:
        deleteStat = User.delete_user(username=data['username'], password=data['password'])

        if deleteStat != False:
            isAuthenticated = False
            return (jsonify(response='deleted', isAuthenticated=isAuthenticated), 200)
        else:
            return (jsonify(response='failed'), 200)
            
@app.route('/api/add_student', methods=['POST'])
def add_student():
    student = request.json["data"]
    teacher = request.json['username']

    teacher_info = User.query.filter_by(username=teacher).first()

    if teacher_info:

        student = User.query.filter_by(username=student['student_username']).first()

        if student:
            student_list = [
                {"username": s.student_username,
                "first_name": s.student_firstName,
                "last_name": s.student_lastName,
                "email": s.student_email} for s in teacher_info.students if s.teacher == teacher_info.username]

            if not student.username in [s["username"] for s in student_list]:
                student_info = Student(student_username=student.username, teacher=teacher_info.username, student_email=student.email, student_firstName=student.first_name, student_lastName=student.last_name)

                db.session.add(student_info)
                db.session.commit()
            
            student_list = [
                {"username": s.student_username,
                "first_name": s.student_firstName,
                "last_name": s.student_lastName,
                "email": s.student_email} for s in teacher_info.students if s.teacher == teacher_info.username]
            
            print('in add student after added', student_list)

            userObj = {
                "username": teacher_info.username,
                "first_name": teacher_info.first_name,
                "last_name": teacher_info.last_name,
                "email": teacher_info.email,
                "account_type": teacher_info.account_type,
                "students": []
                }
            
            userObj['students'] = student_list
            
            return (jsonify(user=userObj), 200)
    else:
        return (jsonify(response='failed'), 200)


@app.route('/api/fetch_student', methods=["POST"])
def fetch_student():
    teacher = request.json['teacher']
    student = request.json['student']

    teacher_info = User.query.filter_by(username=teacher).first()


    if teacher_info:
    
        student = User.query.filter_by(username=student).first()

        if student:
            
            student_list = [
                {"username": s.student_username,
                "first_name": s.student_firstName,
                "last_name": s.student_lastName,
                "email": s.student_email} for s in teacher_info.students if s.teacher == teacher_info.username]

            if not student.username in [s["username"] for s in student_list]:
                message = 'Oops, this is not one of your students!'
                return (jsonify(message=message), 200 )
            else:

                my_student = {
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "email": student.email,
                    "username": student.username,
                    "account_type": student.account_type
                }


                allTaj = student.work

                allTajArr = []

                for i in allTaj:
                    allTajObj = {
                        "code" : i.rule,
                        "practice_ayah_count": i.practice_ayah_count,
                        "test_ayah_count": i.test_ayah_count,
                        "total_correct": i.total_correct,
                        "total_out_of": i.total_out_of
                    }

                    practice = []
                    test = []

                    for r in i.practice:
                        p_stats = {
                            'practice_date': r.practice_date,
                            'ayah_count': r.ayah_count
                        }
    
                        practice.insert(0, p_stats)  

                    for t in i.test:
                        t_stats = {
                            'test_date': t.test_date,
                            'test_ayah_count': t.test_ayah_count,
                            'test_score_correct': t.test_score_correct,
                            'test_out_of_count': t.test_out_of_count,
                            'test_score_composite': t.test_score_composite
                        }
    
                        test.insert(0, t_stats) 
                
    
                    allTajObj['practice'] = practice  
                    allTajObj['test'] = test
                

                    allTajArr.append(allTajObj)

                my_student["tajweed"] = allTajArr
                
                return (jsonify(my_student=my_student), 200 )

@app.route('/api/remove_student', methods=["POST"])
def remove_student():
    teacher = request.json['teacher']
    student = request.json['student']

    teacher_info = User.query.filter_by(username=teacher).first()

    if teacher_info:
    
        my_student = User.query.filter_by(username=student).first()

        if my_student:
            
            student_list = [
                {"username": s.student_username,
                "first_name": s.student_firstName,
                "last_name": s.student_lastName,
                "email": s.student_email} for s in teacher_info.students if s.teacher == teacher_info.username]
            
            print('before', student_list)

            if my_student.username in [s["username"] for s in student_list]:
                print('student found', my_student)
                removed = Student.query.filter_by(student_username=student).delete()
                db.session.commit()
                
            student_list = [
                {"username": s.student_username,
                "first_name": s.student_firstName,
                "last_name": s.student_lastName,
                "email": s.student_email} for s in teacher_info.students if s.teacher == teacher_info.username]
            
            userObj = {
                "username": teacher_info.username,
                "first_name": teacher_info.first_name,
                "last_name": teacher_info.last_name,
                "email": teacher_info.email,
                "account_type": teacher_info.account_type,
                "students": []
                }

            userObj['students'] = student_list
            
            return (jsonify(user=userObj), 200)


@app.route('/api/fetch_rules')
def fetch_rules():
    tajweed_rules = TajweedRules.query.all()
    rules = [{'code': r.code, 'name': r.name} for r in tajweed_rules]

    return (jsonify(rules=rules), 200)

@app.route('/api/fetch_single_rule', methods=['POST'])
def fetch_rule():
    user = User.query.filter_by(username=request.json['user']).first()
    code = request.json['code']

    if user and user.account_type == 'admin':
        tajweed_rule = TajweedRules.query.filter_by(code=code).first()

        rule = {
            "code": tajweed_rule.code,
            "name": tajweed_rule.name,
            "summary": tajweed_rule.summary,
            "details": tajweed_rule.details,
            "example": tajweed_rule.example,
            "audio": tajweed_rule.audio,
            "with_exercise": tajweed_rule.with_exercise
        }

        return (jsonify(rule=rule), 200)

@app.route('/api/add_edit_rule', methods=['POST'])
def add_edit_rule():
    user = User.query.filter_by(username=request.json['user']).first()
    ruleData = request.json['ruleData']
    mode = request.json['mode']
    allTajArr = []

    if user and user.account_type == 'admin':
        if mode == 'add':

            new_rule = TajweedRules(code=ruleData['rule_code'], name=ruleData['rule_name'], summary=ruleData['rule_summary'], details=ruleData['rule_details'], example=ruleData['rule_example'], audio=ruleData['rule_audio'], with_exercise=ruleData['rule_with_exercise'])
            db.session.add(new_rule)
            db.session.commit()

            allUsers = User.query.all()

            for u in allUsers:
                user_work = UserWork(rule=new_rule.code, practice_ayah_count=0, test_ayah_count=0, total_correct=0, total_out_of=0)
                db.session.add(user_work)
                db.session.commit()

                user_work_stats = UserWorkStats(user_id=u.id, work_id=user_work.id)
                db.session.add(user_work_stats)
                db.session.commit()
            
            allWork = user.work

            for i in allWork:  
                            
                allTajObj = {
                    "code" : i.rule,
                    "practice_ayah_count": i.practice_ayah_count,
                    "test_ayah_count": i.test_ayah_count,
                    "total_correct": i.total_correct,
                    "total_out_of": i.total_out_of
                }

                practice = []
                test = []

                for r in i.practice:
                    p_stats = {
                        'practice_date': r.practice_date,
                        'ayah_count': r.ayah_count
                    }
    
                    practice.insert(0, p_stats)  

                for t in i.test:
                    t_stats = {
                        'test_date': t.test_date,
                        'test_ayah_count': t.test_ayah_count,
                        'test_score_correct': t.test_score_correct,
                        'test_out_of_count': t.test_out_of_count,
                        'test_score_composite': t.test_score_composite
                    }
    
                    test.insert(0, t_stats) 
                    
    
                allTajObj['practice'] = practice  
                allTajObj['test'] = test
                

                allTajArr.append(allTajObj)

            return (jsonify(result='success', tajweed=allTajArr), 200)
        
        elif mode == 'edit':
            existing_rule = TajweedRules.query.filter_by(code=ruleData['rule_code']).first()
            
            existing_rule.name=ruleData['rule_name']
            existing_rule.summary=ruleData['rule_summary']
            existing_rule.details=ruleData['rule_details']
            existing_rule.example=ruleData['rule_example']
            existing_rule.audio=ruleData['rule_audio']
            existing_rule.with_exercise=ruleData['rule_with_exercise']

            db.session.add(existing_rule)
            db.session.commit()

            return (jsonify(result='success'), 200)

@app.route('/api/delete_rule', methods=['POST'])
def delete_rule():
    user = User.query.filter_by(username=request.json['user']).first()
    code = request.json['code']
    allTajArr = []

    if user and user.account_type == 'admin':

        deletedRule = TajweedRules.query.filter_by(code=code).delete()
        db.session.commit()
        
        ruleWork = UserWork.query.filter_by(rule=code)

        for r in ruleWork:

            deletedUserWork = UserWork.query.filter_by(id=r.id).delete()

            deletedStats = UserWorkStats.query.filter_by(work_id=r.id).delete()
            db.session.commit()
        
        allWork = user.work

        for i in allWork:  
                        
            allTajObj = {
                "code" : i.rule,
                "practice_ayah_count": i.practice_ayah_count,
                "test_ayah_count": i.test_ayah_count,
                "total_correct": i.total_correct,
                "total_out_of": i.total_out_of
            }

            practice = []
            test = []

            for r in i.practice:
                p_stats = {
                    'practice_date': r.practice_date,
                    'ayah_count': r.ayah_count
                }

                practice.insert(0, p_stats)  

            for t in i.test:
                t_stats = {
                    'test_date': t.test_date,
                    'test_ayah_count': t.test_ayah_count,
                    'test_score_correct': t.test_score_correct,
                    'test_out_of_count': t.test_out_of_count,
                    'test_score_composite': t.test_score_composite
                }

                test.insert(0, t_stats) 
                

            allTajObj['practice'] = practice  
            allTajObj['test'] = test
            

            allTajArr.append(allTajObj)

        return (jsonify(result='deleted', tajweed=allTajArr), 200)


