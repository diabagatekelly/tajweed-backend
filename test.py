import codecs


def printLetterIdx():
    print('running')
    dest = open(r'C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\test_result.txt', "a")
    f = open(r'C:\Users\kelly\Documents\Development Related\Portfolio Projects\islamic ed suite (angular + python + sql)\Tajweed app python backend\fatiha.txt', encoding='cp1252')
    for line in f:
        line = line.split("|")
        dest.write(line)
        dest.close()

printLetterIdx()        
