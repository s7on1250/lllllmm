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

token = "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"
url = "https://openrouter.ai/api/v1/chat/completions"


def llm(text):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "model": "meta-llama/llama-3.2-90b-vision-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "Ты профессиональный юрист и хорошо понимаешь суть текста."
            },
            {
                "role": "user",
                "content": f"Сделай синонимичное краткое содержание текста. ОТВЕЧАТЬ ТОЛЬКО СОДЕРЖАНИЕМ. '{text}'"
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    reply = response.json()['choices'][0]['message']['content']
    return reply


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
            """
            while True:
                try:
                    synonym = llm(s[1])
                    laws_dict[synonym] = c
                    break
                except:
                    time.sleep(10)
            """
        summ = summary(c)[0]['summary_text']
        laws_dict[summ] = c
    return laws_dict


df = pd.read_csv('project/laws_data.csv')
df = df.dropna()
d = db_dict(df)
with open('project/dict_db_2.pkl', 'wb') as f:
    pickle.dump(d, f)
