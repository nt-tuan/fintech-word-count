import os
from read import readBankFiles
from PyPDF2 import PdfReader
from underthesea import word_tokenize
import pytesseract
from pytesseract import Output, TesseractError
import pdf2image
import pandas as pd

def count_keywords_v2(pdf_file, keywords):
    keyword_count = {keyword: 0 for keyword in keywords}
    images = pdf2image.convert_from_path(pdf_file)
    for image in images:
        ocr_dict = pytesseract.image_to_data(image, lang='eng', output_type=Output.DICT)
        text = " ".join(ocr_dict['text'])
        for keyword in keywords:
            keyword_count[keyword] += text.lower().count(keyword.lower())
    return keyword_count

def count_total():
  bankFiles = readBankFiles()
  years = bankFiles['years']
  banks = bankFiles['banks']
  columns = ['bank', 'year', 'segments_count']
  for bank in ["STB"]:
    df = pd.DataFrame(columns=columns)
    for year in ["2013.pdf"]:
      try:
        print("counting word " + bank + " " + year)
        total = 0
        filePath = "./data/banks/" + bank + "/" + year
        if not os.path.isfile(filePath):
          print(filePath + " not existed")
          continue
        # pdf_reader = PdfReader(filePath)
        # for page in pdf_reader.pages:
        #   page_text = page.extract_text()
        #   segmented_text = word_tokenize(page_text.lower())
        #   total += len(segmented_text)
        images = pdf2image.convert_from_path(filePath)
        for image in images:
          ocr_dict = pytesseract.image_to_data(image, lang='eng', output_type=Output.DICT)
          text = " ".join(ocr_dict['text'])
          segmented_text = word_tokenize(text.lower())
          total += len(segmented_text)
          
        nextRow = pd.DataFrame([[bank, year.replace(".pdf", ""),total]], columns=columns)
        df = pd.concat([df, nextRow])
      except:
        print("error")
    df.to_csv("./out/segments_count/" + bank + ".csv", columns=columns)
      
count_total()