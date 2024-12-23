import json
import pickle
import time

import requests
import openai
from llm import llm, llm2, llm3, laws_for_text

api_key="API_KEY",
base_url="SAMBANOVA",


def check(true, pred):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    while True:
        try:
            response = client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[{"role": "system",
                           "content": "Ты профессиональный экзаменатор. Проверь ответы"},
                          {"role": "user",
                           "content": f"Проверь ответы. Правильный ответ {true}. Как ответил ученик {pred}. Проверь на соответсвие на суть. Пример ответа: 'Праавильно', 'Неправильно"}],
                temperature=0.1,
                top_p=0.1
            )
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

    return response.choices[0].message.content


with open('project/data/bench.pkl', 'rb') as f:
    d = pickle.load(f)

q = []
a = []
for obj in d:
    problem = obj.split('Правильный ответ: ')
    if len(problem[1]) <= 2:
        q.append(problem[0])
        a.append(problem[1])

correct = 0
all = 0

for i, task in enumerate(q):
    while True:
        try:
            chunks = llm(task).split('*')
            chunks.append(llm2(task))
            laws = laws_for_text(chunks)
            answer = llm3(task, laws)
            answer_exam = check(a[i], answer)
            print(answer_exam)
            if answer_exam == 'Правильно.':
                correct += 1
            all += 1
            if all > 0:
                print(correct / all)
            break
        except Exception as e:
            if 'maximum' in str(e).split(' '):
                break

            time.sleep(10)
            pass
