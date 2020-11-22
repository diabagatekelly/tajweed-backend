import codecs
from collections import Counter
from flask import Flask, render_template, jsonify, json, request
import pyquran as q
import output
import random
from tajweed import Tajweed
# import "../Tajweed Apis/tajweed.ghunnah.json"


app = Flask(__name__)
app.config["SECRET_KEY"] = "kelly-01221990"


wordDict = Counter()

tajweedJSON = {}
idghaamNoGhunnahJSON = {}

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
    text = ''
    f = open(r'C:\Users\kelly\OneDrive\Desktop\Islamic Web Dev Projects\Tajweed app python\quran-uthmani.txt', encoding='utf-8')
    text = f.read()

    portion = '1|1|'

    if portion in text:
        ayat = portion
        return render_template('home.html', text = text, portion = portion)
    else:
        portion = 'NOne'
        return render_template("home.html", text=text, portion=portion)


@app.route("/pypi")
def pypi_func():
    test_ayat = q.quran.get_verse(114, 1, with_tashkeel=True)
    # readFile = json.loads("../Tajweed Apis/tajweed.ghunnah.json")
    # json.loads("../")
    # rules = readFile["ghunnah"]

    # for item in rules:
    #     if item["surah"] == 112:
    #         print(item)

    rule = test_ayat[23:24]

    string = q.quran.get_verse(2, 3, with_tashkeel=True)
    index = q.search_sequence(sequancesList=['قْ'], chapterNum=2, verseNum=3, mode=1)

    return render_template("pypi.html", test_ayat=test_ayat, rule=rule)


@app.route("/generate_ayat", methods=["POST"])
def generate_ayat():
    # my_file = 'quran-uthmani.txt'
    text = []
    f = open(r'C:\Users\kelly\OneDrive\Desktop\Islamic Web Dev Projects\Tajweed app python\quran-uthmani.txt', encoding='utf-8')
    for line in f:
        text.append(line)

    rule = request.json["ruleChosen"]
    ruleDetails = Tajweed.Select_dict_path(rule)

    ayatRange = int(request.json["range"])
    ayat = []
    surahNumber = random.randint(1, 114)
    fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=False)

    while len(fullSurah) < ayatRange:
        surahNumber = random.randint(1, 114)
        fullSurah = q.quran.get_sura(surahNumber, with_tashkeel=True)

    if len(fullSurah) > ayatRange:
        firstAyat = random.randint(1, (len(fullSurah) - ayatRange))
        surahName = q.quran.get_sura_name(surahNumber)
        for n in range(firstAyat, firstAyat+ayatRange):   
            target = [line for line in text if f"{surahNumber}|{n}|" in line]
            lineArr = target[0].split('|')
            test_ayat = lineArr[2]
            # test_ayat = q.quran.get_verse(surahNumber, n, with_tashkeel=False)
    
            ayatData = {
                "test_ayat" : test_ayat
            }
            ruleMarker = []
            for item in ruleDetails:
                if item["surah"] == surahNumber and item["ayah"] == n:
                    ruleMarker.append(item)

            ayatData["rule"] = ruleMarker
            
            ayat.append(ayatData)
             

    
    return ( jsonify(rule=rule, ayatRange=ayatRange, ayat=ayat, surahNumber=surahNumber, surahName=surahName, firstAyat=firstAyat), 200 )



@app.route("/test")
def test_rdg():
    """On the front end, make a form that will collect rule to practice, and number of questions. Then, make call to this route, which will open the correct file (maybe put that in a separate function which switch cases). It will also collect the selected number of ayats within the appropriate number range. The random numbers in this range will be the ayat indices to use """
    ayatforsurat = []
    ayatDataArr = []    
    ayatArr = Tajweed.Select_dict_path("ghunnah")
    for item in ayatArr:
        if item["surah"] == 114:
            ayatforsurat.append(item)

    for ayat in ayatforsurat:
        test_ayat = q.quran.get_verse(ayat["surah"], ayat["ayah"], with_tashkeel=True)
        rule = test_ayat[ayat["start"]:ayat["start"]+1]
        ayatData = {
            "test_ayat" : test_ayat,
            "rule" : rule
        }

        ayatDataArr.append(ayatData)

    print(ayatDataArr)

    # with open("Tajweed Apis/tajweed.idghaamNoGhunnah.json") as jsonFile:
    #     jsonObject = json.load(jsonFile)
    #     idghaamNoGhunnahJSON["data"] = jsonObject
    #     jsonFile.close()
        
    #     print(len(idghaamNoGhunnahJSON["data"]["idghaamNoGhunnah"]))
    #     specified = idghaamNoGhunnahJSON["data"]["idghaamNoGhunnah"][5]
        # for item in idghaamNoGhunnahJSON["data"]["idghaamNoGhunnah"]:
        #     portion.append(item)

    return render_template("output.html", ayat=ayatforsurat, ayatDataArr=ayatDataArr)