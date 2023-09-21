# -*- coding: utf-8 -*-
"""Count Keywords.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RRgY8qHdsgKWfxPPRHtx-iy6Z_gZm-F2
"""

import re
import os
from PyPDF2 import PdfReader
import pandas as pd
import pytesseract
from pytesseract import Output, TesseractError
import pdf2image
from unidecode import unidecode
from underthesea import word_tokenize

import numpy

def isBankName(bank):
    return re.match("\w+.pdf", bank)

def readBankFiles():
    dirs = os.listdir("./data/banks")
    files = []
    for dir in dirs:
        filesInDir = os.listdir("./data/banks/" + dir)
        files.extend(filesInDir)
    return {"years": list(filter(isBankName, list(dict.fromkeys(files)))), "banks": dirs }

def count_words(page_text, keyword):
    normalized_text = unidecode(page_text.lower())
    normalized_keyword = unidecode(keyword.lower())
    return normalized_text.count(normalized_keyword)

def count_total_words(page_text):
    normalized_text = unidecode(page_text.lower())
    return len(word_tokenize(normalized_text))

def readKeywords():
    df = pd.read_csv('./data/keywords.csv')
    keywordMap = {}
    for index, row in df.iterrows():
        segment = row['segment']
        keyword = row['keyword']
        keywordMap[keyword] = segment
    return {
        "keywords": list(df['keyword']),
        "keywordMap": keywordMap
    }
    
def count_keywords_with_pypdf2(pdf_file, keywords):
    keyword_count = {keyword: 0 for keyword in keywords}
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        for keyword in keywords:
            keyword_count[keyword] += count_words(page_text, keyword)
    return keyword_count



def count_keywords_in_image_pdf(pdf_file, keywords):
    keyword_count = {keyword: 0 for keyword in keywords}
    images = pdf2image.convert_from_path(pdf_file)
    total = 0
    index = 0
    for image in images:
        print("progress " + str(index + 1) + "/" + str(len(images)))
        index+=1
        ocr_dict = pytesseract.image_to_data(image, lang='vie', output_type=Output.DICT)
        text = " ".join(ocr_dict['text'])
        total += count_total_words(text)
        for keyword in keywords:
            keyword_count[keyword] += count_words(text, keyword)
            
    return [keyword_count,total]