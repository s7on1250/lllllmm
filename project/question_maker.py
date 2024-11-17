import json

import requests
from bs4 import BeautifulSoup
import time
import openai
import os
import pickle

# Read the HTML file
with open("project/matched_content.html", "r", encoding="utf-8") as file:
    content = file.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Get all text content and split it into sections by "Задача"
sections = soup.get_text().split("Задача")

# Dictionary to store problems and solutions
problems_solutions = {}

for i, section in enumerate(sections[1:], start=1):  # Skipping the first split part if it's before the first problem
    # Split the section by "Решение"
    problem_part, _, solution_part = section.partition("Решение")
    problems_solutions[f"Problem {i}"] = {
        "Problem": problem_part.strip(),
        "Solution": solution_part.strip()
    }

token = "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"
url = "https://openrouter.ai/api/v1/chat/completions"


def reform_q(content):
    client = openai.OpenAI(
        api_key="2212f4cc-8565-4bdd-9030-9102ccc7bff1",
        base_url="https://api.sambanova.ai/v1",
    )

    while True:
        try:
            response = client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[{"role": "system",
                           "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Твоя задача сделать экзамен"},
                          {"role": "user",
                           "content": f"Оставь текст как он был убрав лишь вопросы или задачи в конце текста: '{content}'"}],
                temperature=0.1,
                top_p=0.1
            )
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

    return response.choices[0].message.content


def create_q_a(content):
    client = openai.OpenAI(
        api_key="2212f4cc-8565-4bdd-9030-9102ccc7bff1",
        base_url="https://api.sambanova.ai/v1",
    )

    while True:
        try:
            response = client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[{"role": "system",
                           "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Твоя задача сделать экзамен"},
                          {"role": "user",
                           "content": f"У тебя есть задача и решение. Сделай из этого вопрос по задаче с 4 вариантами ответов. ОБЯЗАТЕЛЬНО НАПИШИ ПРАВИЛЬНЫЙ ОТВЕТ В ВИДЕ ОДНОЙ БУКВЫ. Пример: Задача. a) первый ответ b) второй ответ и тп. Правильный ответ: a) '{content['Problem']}' '{content['Solution']}'"}],
                temperature=0.1,
                top_p=0.1
            )
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

    return response.choices[0].message.content


# Display or save the separated problems and solutions
problems = []
for prob_num, content in problems_solutions.items():
    print(prob_num)
    p = reform_q(content['Problem'])
    q = create_q_a(content)
    p_q = p + '\n\n' + q
    problems.append(p_q)

with open('project/bench.pkl', 'wb') as f:
    pickle.dump(problems, f)
