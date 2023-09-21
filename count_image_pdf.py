from extractor import count_keywords_in_image_pdf
from read import readBankFiles, readKeywords
import os
import pandas as pd

bank_data = readBankFiles()
banks = bank_data['banks']
years = bank_data['years']

keywordResult = readKeywords()
keywords_to_count = keywordResult['keywords']
keywordMap = keywordResult['keywordMap']

columns = ['bank', 'year', 'keyword', 'segment', 'count', 'total']

for bank in banks:
  df = pd.DataFrame(columns=columns)
  for year in years:
    filePath = "./data/banks/" + bank + "/" + year
    if not os.path.isfile(filePath):
      print(filePath + " not existed")
      continue;
    print("counting keywords in " + filePath + " ...")
    [count_result, total] = count_keywords_in_image_pdf(filePath, keywords_to_count)
    print("writing result, there are " + str(total))
    for x, y in count_result.items():
      nextRow = pd.DataFrame([[bank, year.replace(".pdf", ""),x, keywordMap[x], y, total]], columns=columns)
      df = pd.concat([df, nextRow])
  df.to_csv("./out_v3/" + bank + ".csv", columns=columns)