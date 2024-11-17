import time

import requests
import sys
import vector_db
import json
import openai

db = vector_db.load_vector_db()


def laws_for_text(chunk):
    laws_set = set()
    for obj in chunk:
        if len(obj) > 0:
            laws = vector_db.query_vector_db(obj, db, vector_db.model, 2)[0]
            for law in laws:
                laws_set.add(law)
    return laws_set


token = "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"
url = "https://openrouter.ai/api/v1/chat/completions"


def llm(text):
    client = openai.OpenAI(
        api_key="2212f4cc-8565-4bdd-9030-9102ccc7bff1",
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
            model='Meta-Llama-3.1-405B-Instruct',
            messages=[{"role": "system",
                       "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Ты НЕ пишешь статьи кодекса, ЕСЛИ эти статьи не упомянены напрямую в задаче"},
                      {"role": "user",
                       "content": f"Напиши список преступлений, которые могут привлекаться по статьям УК РФ. НИ В КОЕМ СЛУЧАЙ НЕ ОТВЕЧАЙ КАКИЕ ЭТО СТАТЬИ. Формат ответа: * Пункт1\n * Пункт2\n. '{text}'"}],
            temperature=0.1,
            top_p=0.1
        )

    return response.choices[0].message.content


def llm2(text):
    client = openai.OpenAI(
        api_key="2212f4cc-8565-4bdd-9030-9102ccc7bff1",
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[{"role": "system",
                       "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Ты НЕ пишешь статьи кодекса, ЕСЛИ эти статьи не упомянены напрямую в задаче"},
                      {"role": "user",
                       "content": f"Напиши краткое содержание этого текста с главным смыслом. НИ В КОЕМ СЛУЧАЙ НЕ ОТВЕЧАЙ КАКИЕ ЭТО СТАТЬИ.'{text}'"}],
            temperature=0.1,
            top_p=0.1
        )


    return response.choices[0].message.content


def llm3(text, rag_list):
    client = openai.OpenAI(
        api_key="2212f4cc-8565-4bdd-9030-9102ccc7bff1",
        base_url="https://api.sambanova.ai/v1",
    )
    response = client.chat.completions.create(
            model='Meta-Llama-3.1-405B-Instruct',
            messages=[{"role": "system",
                       "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Для решения задачи возможно подойдут эти материалы:"
                                  f"{rag_list}"},
                      {"role": "user",
                       "content": f"{text}"}],
            temperature=0.1,
            top_p=0.1
        )

    return response.choices[0].message.content


def main():
    while True:
        print("Enter your text (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break

        problem = "\n".join(lines)
        chunks = llm(problem).split('*')
        chunks.append(llm2(problem))
        laws = laws_for_text(chunks)
        print(laws)
        print(llm3(problem, laws))


if __name__ == '__main__':
    main()
