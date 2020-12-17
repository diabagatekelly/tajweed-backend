from flask import json

class Tajweed():

    def __init__(self):
        self
        

    def Select_dict_path(rule):
        dict_path = ''
        beg = 0
        end = 0
        if rule == 'ghunnah':
            dict_path = "Tajweed Apis/tajweed.ghunnah.json"
            beg = 2
            end = 114
        elif rule == 'hamzatWasl':
            dict_path = "Tajweed Apis/tajweed.hamzatWasl.json"
            beg = 1
            end = 114
        elif rule == 'idghaamGhunnah':
            dict_path = "Tajweed Apis/tajweed.idghaamGhunnah.json"
            beg = 2
            end = 114
        elif rule == 'idghaamNoGhunnah':
            dict_path = "Tajweed Apis/tajweed.idghaamNoGhunnah.json"
            beg = 2
            end = 10
        elif rule == 'ikhfa':
            dict_path = "Tajweed Apis/tajweed.ikhfa.json"
            beg = 2
            end = 80
        elif rule == 'iqlab':
            # needs to be revised
            dict_path = "Tajweed Apis/tajweed.iqlab.json"
            beg = 2
            end = 10
        elif rule == 'madd246':
            dict_path = "Tajweed Apis/tajweed.madd246.json"
            beg = 2
            end = 40
        elif rule == 'madd':
            # combined all madd except 246
            dict_path = "Tajweed Apis/tajweed.madd.json"
            beg = 1
            end = 114
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
            