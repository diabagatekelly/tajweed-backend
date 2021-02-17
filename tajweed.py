from flask import json

class Tajweed():

    def __init__(self):
        self

    def create_file(rule):
        print(rule)
        dest = open(r"C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\Tajweed Apis\tajweed.{rule}.json", "a")
        
    def Select_dict_path(rule):
        dict_path = ''
        beg = 0
        end = 0
        
        if rule == 'ghunnah':
            dict_path = "Tajweed Apis/tajweed.ghunnah.json"
            beg = 2
            end = 114
        elif rule == 'idghaam_ghunnah':
            dict_path = "Tajweed Apis/tajweed.idghaam_ghunnah.json"
            beg = 2
            end = 75
        elif rule == "idghaam_mutajanisayn":
            dict_path = "Tajweed Apis/tajweed.idghaam_mutajanisayn.json"
            beg = 2
            end = 7
        elif rule == "idghaam_mutaqaribayn":
            dict_path = "Tajweed Apis/tajweed.idghaam_mutaqaribayn.json"
            #need to cycle through all rule instances
            beg = 2
            end = 45
        elif rule == 'idghaam_no_ghunnah':
            # needs to be revised
            dict_path = "Tajweed Apis/tajweed.idghaam_no_ghunnah.json"
            beg = 2
            end = 60
        elif rule == 'idghaam_shafawi':
            dict_path = "Tajweed Apis/tajweed.idghaam_shafawi.json"
            beg = 2
            end = 13
        elif rule == 'ikhfa':
            dict_path = "Tajweed Apis/tajweed.ikhfa.json"
            beg = 2
            end = 80
        elif rule == 'ikhfa_shafawi':
            dict_path = "Tajweed Apis/tajweed.ikhfa_shafawi.json"
            beg = 2
            end = 43
        elif rule == 'idhaar':
            dict_path = "Tajweed Apis/tajweed.idhaar.json"
            beg = 2
            end = 50
        elif rule == 'idhaar_shafawi':
            dict_path = "Tajweed Apis/tajweed.idhaar_shafawi.json"
            beg = 2
            end = 50
        elif rule == 'iqlab':
            # needs to be revised
            dict_path = "Tajweed Apis/tajweed.iqlab.json"
            beg = 2
            end = 43
        elif rule == 'madd_246':
            dict_path = "Tajweed Apis/tajweed.madd_246.json"
            beg = 2
            end = 15
        elif rule == 'madd_6':
            # map indiv
            dict_path = "Tajweed Apis/tajweed.madd_6.json"
            beg = 1
            end = 15
        elif rule == 'madd_muttasil':
            # combined all madd except 246
            dict_path = "Tajweed Apis/tajweed.madd_muttasil.json"
            beg = 2
            end = 60
        elif rule == 'madd_munfasil':
            # combined all madd except 246
            dict_path = "Tajweed Apis/tajweed.madd_munfasil.json"
            beg = 1
            end = 43
        elif rule == 'qalqalah':
            dict_path = "Tajweed Apis/tajweed.qalqalah.json"
            beg = 2
            end = 100

        """Read and return all words in dictionary."""

        with open(dict_path) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            return [jsonObject[rule], beg, end]

    def Analysis_path(data):
        with open("Tajweed Apis/analysis.json", "a") as outfile:
            json.dump(data, outfile) 

    def getExplanation(rule):
        """Will finish this function with the rest of the rule's explanations"""
        if rule == 'ghunnah':
            dict_path = "Tajweed Apis/explanation.json"

        with open(dict_path) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            return jsonObject[rule]



            