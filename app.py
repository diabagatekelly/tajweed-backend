import codecs
from collections import Counter
from flask import Flask, render_template, jsonify, json, request, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_cors import CORS, cross_origin
import pyquran as q
import random
from tajweed import Tajweed
import matplotlib.pyplot as plt
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, TajweedRules, UserTajweedStats, Practice, Test
import os

# import "../Tajweed Apis/tajweed.ghunnah.json"


app = Flask(__name__)
app.config["SECRET_KEY"] = "kelly-af-01221990"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///tajweed')
# app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)

wordDict = Counter()

tajweedJSON = {}
idghaamNoGhunnahJSON = {}

Rules = ["ghunnah", "hamzatWasl", "idghaamGhunnah", "idghaamNoGhunnah", "ikhfa", "iqlab", "madd", "madd246", "qalqalah"]

# Get Original JSON File
@app.before_request
def fetch_tajweed():
    with open("Tajweed Apis/tajweed.hafs.uthmani-pause-sajdah.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        tajweedJSON["data"] = jsonObject
        jsonFile.close()

@app.route("/buildApis")
def tajweed():
    annotation = tajweedJSON["data"]
    return json.dumps(annotation)


# My JSON Files' Builder Routes
@app.route("/write_ghunnah", methods=["POST"])
def ghunnah():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.ghunnah.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_idghaamGhunnah", methods=["POST"])
def idghaamGhunnah():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.idghaamGhunnah.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_idghaamNoGhunnah", methods=["POST"])
def idghaamNoGhunnah():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.idghaamNoGhunnah.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_ikhfa", methods=["POST"])
def ikhfa():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.ikhfa.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_iqlab", methods=["POST"])
def iqlab():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.iqlab.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_madd246", methods=["POST"])
def madd246():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.madd246.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_maddMuttasil", methods=["POST"])
def maddMuttasil():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.maddMuttasil.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_maddMunfasil", methods=["POST"])
def maddMunfasil():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.maddMunfasil.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_madd6", methods=["POST"])
def madd6():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.madd6.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_qalqalah", methods=["POST"])
def qalqalah():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.qalqalah.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )

@app.route("/write_hamzatWasl", methods=["POST"])
def hamzatWasl():
    data = request.json["data"]
    with open("Tajweed Apis/tajweed.hamzatWasl.json", "w") as outfile:
        json.dump(data, outfile) 
    return ( jsonify(data), 200 )



@app.route("/")
def home():
    print('loading home', session)
    text = ''
    f = open(r'C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\quran-uthmani.txt', encoding='utf-8')
    text = f.read()

    portion = '1|1|'

    if portion in text:
        ayat = portion
        return render_template('home.html', text = text, portion = portion)
    else:
        portion = 'NOne'
        return render_template("home.html", text=text, portion=portion)


# @app.route("/pypi")
# def pypi_func():
#     test_ayat = q.quran.get_verse(114, 1, with_tashkeel=True)
#     # readFile = json.loads("../Tajweed Apis/tajweed.ghunnah.json")
#     # json.loads("../")
#     # rules = readFile["ghunnah"]

#     # for item in rules:
#     #     if item["surah"] == 112:
#     #         print(item)

#     rule = test_ayat[23:24]

#     string = q.quran.get_verse(2, 3, with_tashkeel=True)
#     index = q.search_sequence(sequancesList=['قْ'], chapterNum=2, verseNum=3, mode=1)

#     return render_template("pypi.html", test_ayat=test_ayat, rule=rule)


# @app.route("/analysis", methods=["POST"])
# def dataAnalysis():
#     rule = request.json["ruleChosen"]

#     ruleDetails = Tajweed.Select_dict_path(rule)
#     surahData = {}

#     for n in range(1, 115):
#         occ = sum(item['surah'] == n for item in ruleDetails)
#         surahData[n] = occ
    
#     Tajweed.Analysis_path({f"{rule}": surahData})
    

#     return (jsonify(rule=rule, surahData=surahData))

# @app.route("/view-graphs", methods=["GET", "POST"])
# def viewGraphs():
#     rule = request.form.get('selectedRule')
#     sortedRule={}
   
#     if rule != None:
#         with open("Tajweed Apis/analysis.json") as jsonFile:
#             jsonObject = json.load(jsonFile)
#             jsonFile.close()
#             sortedRule = jsonObject[rule]
#     # plt.bar(*zip(*ruleData.items()))

#             fig = plt.figure()

#             plt.bar(range(len(sortedRule)), list(sortedRule.values()), align='center')
#             plt.xticks(range(len(sortedRule)), list(sortedRule.keys()))
#             plt.locator_params(axis='x', nbins=20)

#             fig.suptitle(f"{rule}", fontsize=20)
#             plt.xlabel('Surah #', fontsize=14)
#             plt.ylabel('# of rules', fontsize=14)


#             plt.show()
#     return render_template("output.html", rule=rule, sortedRule=sortedRule)


@app.route("/api/get_explanation", methods=["POST"])
def get_expl():
    rule = request.json["ruleChosen"]
    explanationObj = Tajweed.getExplanation(rule)
    print(explanationObj)

    return ( jsonify(explanationObj=explanationObj), 200 )


@app.route("/api/generate_ayat", methods=["POST"])
def generate_ayat():
    text = []
    f = open(r'C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\quran-uthmani.txt', encoding='utf-8')
    for line in f:
        text.append(line)

    activity = request.json["activity"]
    rule = request.json["ruleChosen"]
    ruleDetails = Tajweed.Select_dict_path(rule)[0]
    beg = Tajweed.Select_dict_path(rule)[1]
    end = Tajweed.Select_dict_path(rule)[2]

    ayatRange = int(request.json["range"])
    ayat = []

    if rule != "idghaamNoGhunnah" and rule != "iqlab" and activity != "learn":
        surahNumber = random.randint(beg, end)

        fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=False)

        while len(fullSurah) < ayatRange:
            surahNumber = random.randint(beg, end)
            fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=True)

        if len(fullSurah) > ayatRange:
            firstAyat = random.randint(1, (len(fullSurah) - ayatRange))

            surahName = q.quran.get_sura_name(surahNumber)
            for n in range(firstAyat, firstAyat+ayatRange):   
                target = [line for line in text if f"{surahNumber}|{n}|" in line]
                lineArr = target[0].split('|')
                test_ayat = lineArr[2]

                ayatData = {
                    "test_ayat" : test_ayat
                }
                ruleMarker = []
                for item in ruleDetails:
                    if item["surah"] == surahNumber and item["ayah"] == n:
                        ruleMarker.append(item)

                ayatData["rule"] = ruleMarker
                ayatData["surahNumber"] = surahNumber
                ayatData["ayahNumber"] = n
                
                ayat.append(ayatData)
    
    elif activity == "learn" or rule == "idghaamNoGhunnah" or rule == "iqlab": 
        firstAyat = random.randint(1, (len(ruleDetails) - ayatRange))

        while len(ayat) < ayatRange:
            surahNumber = ruleDetails[firstAyat]["surah"]
            surahName = q.quran.get_sura_name(surahNumber)
            ayatNumber = ruleDetails[firstAyat]["ayah"]
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
    print('firing auth', session)

    userData = request.json["data"]
    mode = request.json["mode"]
    allTajArr = []

    print('calling auth', mode)

    if mode == 'register':
        try:
            user = User.register(
                first_name = userData["firstName"], 
                last_name = userData["lastName"], 
                email = userData["email"], 
                username = userData["username"], 
                password = userData["password"])

            db.session.commit()

            if user:
                isAuthenticated = True
                session["isAuthenticated"] = user.username
                session["user"] = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username
                }

                for r in Rules:
                    rules = TajweedRules(code=r)
                    db.session.add(rules)
                    db.session.commit()

                    user_tajweed = UserTajweedStats(user_id=user.id, rule_id=rules.id)
                    db.session.add(user_tajweed)
                    db.session.commit()


                allTaj = user.tajweed_rule
                
                for i in allTaj:
                    allTajObj = {
                        "code" : i.code,
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
        
                        # practice.append(p_stats)  
                        practice.insert(0, p_stats)  

                    for t in i.test:
                        t_stats = {
                            'test_date': t.test_date,
                            'test_ayah_count': t.test_ayah_count,
                            'test_score_correct': t.test_score_correct,
                            'test_out_of_count': t.test_out_of_count,
                            'test_score_composite': t.test_score_composite
                        }
        
                        # test.append(t_stats)  
                        test.insert(0, t_stats) 
                        
        
                    allTajObj['practice'] = practice  
                    allTajObj['test'] = test
                    

                    allTajArr.append(allTajObj)

                session["tajweed"] = allTajArr                

                return (jsonify(isAuthenticated=isAuthenticated), 200 )
            else:
                isAuthenticated = False
                message = 'Error registering user'
                return (jsonify(isAuthenticated=isAuthenticated, message=message), 400 )

            
        except IntegrityError:
            isAuthenticated = False
            message = 'Error registering user'
            return (jsonify(isAuthenticated=isAuthenticated, message=message), 500 )

    elif mode == 'login':
        if 'user' in session and session['user']["first_name"] == userData["username"]:
            return (jsonify(isAuthenticated=isAuthenticated), 200 )
        else:
            try:
                user = User.authenticate(
                username = userData["username"], 
                password = userData["password"])

                db.session.commit()

                if user:
                    isAuthenticated = True
                    session["isAuthenticated"] = user.username
                    session["user"] = {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "username": user.username
                    }

                    allTaj = user.tajweed_rule


                    for i in allTaj:
                        allTajObj = {
                            "code" : i.code,
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
            
                            # practice.append(p_stats)  
                            practice.insert(0, p_stats)  

                        for t in i.test:
                            t_stats = {
                                'test_date': t.test_date,
                                'test_ayah_count': t.test_ayah_count,
                                'test_score_correct': t.test_score_correct,
                                'test_out_of_count': t.test_out_of_count,
                                'test_score_composite': t.test_score_composite
                            }
            
                            # test.append(t_stats)  
                            test.insert(0, t_stats) 
                         
            
                        allTajObj['practice'] = practice  
                        allTajObj['test'] = test
                        

                        allTajArr.append(allTajObj)

                    session["tajweed"] = allTajArr
                
                    return (jsonify(isAuthenticated=isAuthenticated), 200 )
                else:
                    isAuthenticated = False
                    message = 'Error logging in user'
                    return (jsonify(isAuthenticated=isAuthenticated, message=message), 401 )
                
            except IntegrityError:
                isAuthenticated = False
                message = 'Error logging in user'
                return (jsonify(isAuthenticated=isAuthenticated, message=message), 500 )

    else:
        print('no mode at all')        

@app.route('/api/verify_auth')
def verify_auth():
    print('in verify_auth', session)
    if "isAuthenticated" in session:
        isAuthenticated = True
        saved_user = session["user"]
        tajweed = session["tajweed"]
        
        user = {
            "username": saved_user["username"],
            "firstName": saved_user["first_name"],
            "lastName": saved_user["last_name"]
        }

            
        print('in verify auth and isauthenticated found in session', isAuthenticated)

        return (jsonify(response=isAuthenticated, user=user, tajweed=tajweed), 200 )

    elif not "isAuthenticated" in session:
        isAuthenticated = False
        print('in verify auth and isauthenticated NOT found in session', isAuthenticated)
        return (jsonify(response=isAuthenticated), 200 )

@app.route('/api/logout')
def logout():
    print('in logout', session)
    session.pop('isAuthenticated', None)
    session.pop('user', None)
    session.pop('tajweed', None)
    isAuthenticated = False

    return (jsonify(response=isAuthenticated), 200 )

@app.route('/api/update_practice', methods=['POST'])
def update_practice():
    username = request.json["username"]
    stats = request.json["stats"]

    allTajArr = []

    user = User.query.filter_by(username=username).first()
    user_rule = [c for c in user.tajweed_rule if c.code == stats['rule']]
    
    
    practice = Practice(practice_date=db.func.now(), ayah_count=stats['ayah_count'], rule_id=user_rule[0].id)

    db.session.add(practice)
    db.session.commit()  

    user_rule[0].practice_ayah_count = user_rule[0].practice_ayah_count + stats['ayah_count']

    db.session.commit()

    allTaj = user.tajweed_rule

    userObj = {
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name
    }

    for i in allTaj:
        allTajObj = {
        "code" : i.code,
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
            
            # practice.append(p_stats)  
            practice.insert(0, p_stats)  
            
        allTajObj['practice'] = practice  

        test = [p['test'] for p in session['tajweed'] if p['code'] == i.code]
        
        for t in test:
            allTajObj['test'] = t

        
        allTajArr.append(allTajObj)
    
    session['tajweed'] = allTajArr

    return (jsonify(userObj=userObj, allTajArr=allTajArr), 200)


@app.route('/api/update_test', methods=['POST'])
def update_test():
    username = request.json["username"]
    stats = request.json["stats"]

    allTajArr = []

    user = User.query.filter_by(username=username).first()
    user_rule = [c for c in user.tajweed_rule if c.code == stats['rule']]
    
    test = Test(test_date=db.func.now(), test_ayah_count=stats['ayah_count'], test_score_correct=stats['correct'], test_out_of_count=stats['out_of'], test_score_composite=stats['score'], rule_id=user_rule[0].id)

    db.session.add(test)
    db.session.commit()  

    user_rule[0].test_ayah_count = user_rule[0].test_ayah_count + stats['ayah_count']
    user_rule[0].total_correct = user_rule[0].total_correct + stats['correct']
    user_rule[0].total_out_of = user_rule[0].total_out_of + stats['out_of']

    db.session.commit()

    allTaj = user.tajweed_rule

    userObj = {
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name
    }

    for i in allTaj:
        allTajObj = {
        "code" : i.code,
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

            # test.append(t_stats)  
            test.insert(0, t_stats)

        allTajObj['test'] = test  

        practice = [p['practice'] for p in session['tajweed'] if p['code'] == i.code]
        
        for p in practice:
            allTajObj['practice'] = p

    
        allTajArr.append(allTajObj)

    session["tajweed"] = allTajArr

    return (jsonify(userObj=userObj, allTajArr=allTajArr), 200)

  
    





