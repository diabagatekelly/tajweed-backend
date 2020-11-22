from flask import json

class Tajweed():

    def __init__(self):
        self
        

    def Select_dict_path(rule):
        dict_path = ''
        if rule == 'ghunnah':
            dict_path = "Tajweed Apis/tajweed.ghunnah.json"
        elif rule == 'hamzatWasl':
            dict_path = "Tajweed Apis/tajweed.hamzatWasl.json"
        elif rule == 'idghaamGhunnah':
            dict_path = "Tajweed Apis/tajweed.idghaamGhunnah.json"
        elif rule == 'idghaamNoGhunnah':
            dict_path = "Tajweed Apis/tajweed.idghaamNoGhunnah.json"
        elif rule == 'ikhfa':
            dict_path = "Tajweed Apis/tajweed.ikhfa.json"
        elif rule == 'iqlab':
            dict_path = "Tajweed Apis/tajweed.iqlab.json"
        elif rule == 'madd246':
            dict_path = "Tajweed Apis/tajweed.madd246.json"
        elif rule == 'maddMuttasil':
            dict_path = "Tajweed Apis/tajweed.maddMuttasil.json"
        elif rule == 'maddMunfasil':
            dict_path = "Tajweed Apis/tajweed.maddMunfasil.json"
        elif rule == 'madd6':
            dict_path = "Tajweed Apis/tajweed.madd6.json"
        elif rule == 'qalqalah':
            dict_path = "Tajweed Apis/tajweed.qalqalah.json"

        """Read and return all words in dictionary."""

        with open(dict_path) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            return jsonObject[rule]