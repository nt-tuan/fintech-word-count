import sys
from read import readKeywords
from extractor import count_keywords_in_image_pdf
import pandas as pd

keywordResult = readKeywords()
keywords_to_count = keywordResult['keywords']
keywordMap = keywordResult['keywordMap']

file_path = sys.argv[1]
print(file_path)

[count_result, total] = count_keywords_in_image_pdf(file_path, keywords_to_count)
columns = ['keyword', 'segment', 'count', 'total']
df = pd.DataFrame(columns=columns)
for x, y in count_result.items():
  nextRow = pd.DataFrame([[x, keywordMap[x], y, total]], columns=columns)
df.to_csv(file_path.replace(".pdf", "_out.csv"))