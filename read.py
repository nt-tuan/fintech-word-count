import re
import os
import pandas as pd

def isBankName(bank):
    return re.match("\w+.pdf", bank)

def readBankFiles():
    dirs = os.listdir("./data/banks")
    files = []
    for dir in dirs:
        filesInDir = os.listdir("./data/banks/" + dir)
        files.extend(filesInDir)
    return {"years": list(filter(isBankName, list(dict.fromkeys(files)))), "banks": dirs }

def readKeywords():
    df = pd.read_csv('./data/keywords.csv')
    keywordMap = {}
    for index, row in df.iterrows():
        segment = row['segment']
        keyword = row['keyword']
        keywordMap[keyword]= segment
    return {
        "keywords": list(df['keyword']),
        "keywordMap": keywordMap
    }