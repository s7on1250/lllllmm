import re
import pandas as pd
from transformers import GPT2Tokenizer, T5ForConditionalGeneration
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import pipeline
import pickle
import requests
import json
import time

pipe = pipeline('summarization', model='d0rj/rut5-base-summ')

token = "TOKEN"
url = "openrouter_model"

def summary(text):
    return pipe(text)


def db_dict(df):
    pattern = r"((?:Статья\s*)?\d+\.\d*)\s(.*?)(?=\s(?:Статья\s*)?\d+\.\d*|$)"
    laws_dict = dict()
    for i, c in enumerate(df['content'].to_list()):
        print(i)
        sentences = re.findall(pattern, c)
        for s in sentences:
            laws_dict[s[0] + ' ' + s[1]] = c
            summ_s = summary(s[1])[0]['summary_text']
            laws_dict[summ_s] = c
        summ = summary(c)[0]['summary_text']
        laws_dict[summ] = c
    return laws_dict


df = pd.read_csv('project/laws_data.csv')
df = df.dropna()
d = db_dict(df)
with open('project/dict_db_2.pkl', 'wb') as f:
    pickle.dump(d, f)
